#!/usr/bin/env python3
"""Resynchronise le corps local d'un article depuis WordPress (rénovation, plan.md D17 / B18).

Remplace uniquement le corps : l'en-tête, le titre `# …` et le bloc `# SEO` (avant ou après le corps)
sont conservés. Le HTML WordPress est converti dans le Markdown que relit `wp_push_draft.py`
(titres ##/###, listes `-`, `**gras**`, liens `[libellé](url)`) : l'italique, les images, les
iframes et les tableaux sont perdus et signalés.

Contrôle d'aller-retour : le Markdown produit est re-rendu par `wp_push_draft.markdown_like_to_html` ;
le nombre de mots doit rester proche de la version WP (colonne `retour`).

Usage :
    python tools/wp_pull_body.py <ID> [<ID> …]            # à blanc : écarts de mots, pertes
    python tools/wp_pull_body.py <ID> [<ID> …] --apply    # écrit les fichiers canoniques

Refuse `02_Fonds/` (éditeur humain). Lecture seule côté WordPress (GET).
"""

from __future__ import annotations

import argparse
import html as html_module
import re
import sys
from pathlib import Path
from urllib import parse

from index_editorial_utils import read_index, safe_str
from verify_publication import CONFIG_PATH, INDEX_PATH, article_path, is_fonds, wp_post_id
from wp_push_draft import Config, load_config, markdown_like_to_html, wordpress_request_json

LOSSY_TAGS = {"img": "image", "iframe": "iframe", "table": "tableau", "em": "italique", "video": "vidéo"}


def words(text: str) -> int:
    return len(re.findall(r"\w+", text))


def html_words(html: str) -> int:
    return words(html_module.unescape(re.sub(r"<[^>]+>", " ", html)))


def inline_text(fragment: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", fragment)).strip()


def html_to_markdown(html: str) -> str:
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>|<!--.*?-->", "", html)
    text = re.sub(r"(?is)<(figure|iframe|video|table)[^>]*>.*?</\1>", "", text)

    def link(m: re.Match[str]) -> str:
        label = inline_text(m.group(2)).replace("[", "(").replace("]", ")")
        return f"[{label or m.group(1)}]({m.group(1)})"

    text = re.sub(r"(?is)<a\s[^>]*?href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", link, text)
    text = re.sub(r"(?is)</?(strong|b)(\s[^>]*)?>", "**", text)
    text = re.sub(r"(?is)\*\*(\s*)\*\*", r"\1", text)
    text = re.sub(r"(?is)<h[12][^>]*>(.*?)</h[12]>", lambda m: f"\n\n## {inline_text(m.group(1))}\n\n", text)
    text = re.sub(r"(?is)<h[3-6][^>]*>(.*?)</h[3-6]>", lambda m: f"\n\n### {inline_text(m.group(1))}\n\n", text)
    text = re.sub(r"(?is)<li[^>]*>(.*?)</li>", lambda m: f"\n- {inline_text(m.group(1))}\n", text)
    text = re.sub(r"(?is)</?(ul|ol)[^>]*>", "\n\n", text)
    text = re.sub(r"(?is)<br\s*/?>", " ", text)
    text = re.sub(r"(?is)</?(p|div|blockquote|section)[^>]*>", "\n\n", text)
    text = html_module.unescape(re.sub(r"<[^>]+>", "", text))
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    out = "\n".join(lines)
    out = re.sub(r"\n{3,}", "\n\n", out)
    # Puces consécutives : une seule liste (une ligne vide la couperait en deux <ul>).
    out = re.sub(r"(?m)^(- .*)\n\n(?=- )", r"\1\n", out)
    return out.strip()


def lossy(html: str) -> list[str]:
    found = []
    for tag, label in LOSSY_TAGS.items():
        n = len(re.findall(rf"(?i)<{tag}[\s>]", html))
        if n:
            found.append(f"{n} {label}")
    return found


def split_local(text: str) -> tuple[str, str, str]:
    """(préfixe conservé, corps remplaçable, suffixe conservé)."""
    head, sep, rest = text.partition("\n---\n")
    if not sep:
        raise ValueError("séparateur d'en-tête `---` introuvable")
    prefix = head + sep
    lead = rest.lstrip("\n")
    if lead.startswith("# SEO"):
        seo, sep2, rest = lead.partition("\n---\n")
        prefix += "\n" + seo + sep2
    body, seo_sep, seo_tail = rest.partition("\n# SEO")
    suffix = ""
    if seo_sep:
        # Garder la ligne `---` qui précède le bloc SEO final.
        m = re.search(r"\n---\s*$", body)
        if m:
            suffix, body = body[m.start():] + seo_sep + seo_tail, body[:m.start()]
        else:
            suffix = seo_sep + seo_tail
    m = re.match(r"\s*(# [^\n]*\n)", body)
    if m:
        prefix += "\n" + m.group(1)
        body = body[m.end():]
    return prefix, body, suffix


def fetch_post(config: Config, row: dict[str, str]) -> dict | None:
    base = f"{config.site_url}/wp-json/wp/v2/posts"
    fields = "_fields=id,slug,status,content"
    post_id = wp_post_id(safe_str(row.get("URL_WordPress")))
    if post_id:
        item = wordpress_request_json(config, f"{base}/{post_id}?context=edit&{fields}", "GET")
        return item if isinstance(item, dict) else None
    slug = safe_str(row.get("Slug_WordPress"))
    if not slug:
        return None
    items = wordpress_request_json(
        config, f"{base}?slug={parse.quote(slug)}&status=publish,draft,pending,private&context=edit&{fields}", "GET"
    )
    return items[0] if isinstance(items, list) and items else None


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("ids", nargs="+")
    parser.add_argument("--apply", action="store_true", help="écrire les fichiers (sinon à blanc)")
    args = parser.parse_args()

    if not CONFIG_PATH.exists():
        print("Config WordPress locale absente (copier tools/wp_config.example.json).")
        return 2
    config = load_config(str(CONFIG_PATH))
    _, rows = read_index(INDEX_PATH)
    by_id = {safe_str(r.get("ID")): r for r in rows}

    rc = 0
    print("ID | local | WP | retour | pertes | résultat")
    for rid in args.ids:
        row = by_id.get(rid)
        if row is None:
            print(f"{rid} | | | | | ID absent de l'index")
            rc = 1
            continue
        if is_fonds(row):
            print(f"{rid} | | | | | refusé : 02_Fonds/ est réservé à l'éditeur humain")
            rc = 1
            continue
        path = article_path(row)
        if not path.exists():
            print(f"{rid} | | | | | fichier absent : {path.relative_to(INDEX_PATH.parent)}")
            rc = 1
            continue
        post = fetch_post(config, row)
        content = post.get("content", {}) if post else {}
        html = (content.get("raw") or content.get("rendered") or "") if isinstance(content, dict) else ""
        if not html.strip():
            print(f"{rid} | | | | | post WP introuvable ou vide")
            rc = 1
            continue
        text = path.read_text(encoding="utf-8")
        try:
            prefix, body, suffix = split_local(text)
        except ValueError as exc:
            print(f"{rid} | | | | | {exc}")
            rc = 1
            continue
        markdown = html_to_markdown(html)
        wp_n, back_n = html_words(html), html_words(markdown_like_to_html(markdown))
        losses = ", ".join(lossy(html)) or "-"
        result = "à blanc"
        if args.apply:
            new_text = prefix + "\n" + markdown + "\n" + (suffix if suffix else "")
            path.write_text(new_text.rstrip("\n") + "\n", encoding="utf-8")
            result = "écrit"
        print(f"{rid} | {words(body)} | {wp_n} | {back_n} | {losses} | {result}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
