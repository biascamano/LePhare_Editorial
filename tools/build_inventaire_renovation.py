#!/usr/bin/env python3
"""Génère 00_Systeme/Inventaire_renovation.md : le classement des anciens articles pour la rénovation.

Usage : python tools/build_inventaire_renovation.py [--offline]

Pour chaque article hors format actuel (hors `02_Fonds/` et wiki) : famille, liens entrants
(depuis les articles au format actuel / depuis les autres / références Radar, mémoire, dossiers),
mots locaux et WordPress, constats, action proposée :
- Refaire : article encore utile (lié par un article récent, cité au Radar ou dans la mémoire,
  ou texte fondateur lié) → réécriture au format actuel, même ID et même URL ;
- Remettre à niveau : navigation finale, titre, liens — sans réécriture ;
- Trier : même URL qu'un fondamental, brouillon jamais publié, doublon possible, page rubrique,
  post introuvable → décision humaine.
« Copie locale tronquée » (WordPress nettement plus long que le markdown) : resynchroniser depuis
WordPress avant toute retouche, sinon un refresh écraserait l'article en ligne.
Lecture seule sur les articles et WordPress (GET).
"""
from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib import parse

import verify_publication as vp
from wp_push_draft import load_config, wordpress_request_json

ROOT = vp.ROOT
OUT = ROOT / "00_Systeme" / "Inventaire_renovation.md"
REF_FILES = [ROOT / "00_Systeme" / "Radar_editorial.md", ROOT / "00_Systeme" / "Memoire_editoriale.md"]
EMOJI_RE = re.compile("[←-⯿☀-➿\U0001F000-\U0001FAFF️]")
ID_RE = re.compile(r"\b2026-\d{3}\b")
CURRENT_MARKERS = ("Routine quotidienne v3", "Routine hebdomadaire", "Routine mensuelle")
TRUNCATED_RATIO = 1.5


def words(text: str) -> int:
    return len(re.findall(r"\w+", text))


def article_body(text: str) -> str:
    """Corps sans en-tête ni bloc SEO, que le SEO soit avant (format triptyque) ou après le corps."""
    _, _, rest = text.partition("\n---\n")
    if rest.lstrip().startswith("# SEO"):
        _, _, rest = rest.partition("\n---\n")
    return rest.split("\n# SEO", 1)[0]


def family(row: dict[str, str]) -> str:
    rem = vp.safe_str(row.get("Remarques"))
    if "wiki-du-phare" in vp.safe_str(row.get("URL_WordPress")) or "epkb" in rem:
        return "wiki"
    if rem.startswith("Import auto"):
        return "import"
    if rem.startswith(CURRENT_MARKERS):
        return "actuel"
    return "triptyque"


def title_key(title: str) -> str:
    t = unicodedata.normalize("NFKD", EMOJI_RE.sub("", html.unescape(title))).encode("ascii", "ignore").decode().lower()
    return " ".join(re.findall(r"[a-z]{3,}", t)[:4])


def fetch_wp_words(rows: list[dict[str, str]]) -> dict[str, int]:
    config = load_config(str(vp.CONFIG_PATH))
    by_slug = {vp.safe_str(r.get("Slug_WordPress")): vp.safe_str(r.get("ID")) for r in rows if vp.safe_str(r.get("Slug_WordPress"))}
    out: dict[str, int] = {}
    slugs = list(by_slug)
    for i in range(0, len(slugs), 25):
        chunk = ",".join(parse.quote(s) for s in slugs[i:i + 25])
        items = wordpress_request_json(
            config, f"{config.site_url}/wp-json/wp/v2/posts?slug={chunk}&status=publish,draft&per_page=25&_fields=slug,content", "GET"
        )
        for item in items if isinstance(items, list) else []:
            if item.get("slug") in by_slug:
                text = re.sub(r"<[^>]+>", " ", html.unescape(item.get("content", {}).get("rendered", "")))
                out[by_slug[item["slug"]]] = words(text)
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("--offline", action="store_true", help="sans comptage des mots sur WordPress")
    a = ap.parse_args()

    _, rows = vp.read_index(vp.INDEX_PATH)
    by_url = {vp.norm_url(vp.safe_str(r.get("URL_WordPress"))): r for r in rows if vp.safe_str(r.get("URL_WordPress"))}
    by_post = {p: r for r in rows if (p := vp.wp_post_id(vp.safe_str(r.get("URL_WordPress"))))}

    bodies: dict[str, str] = {}
    current: set[str] = set()
    for r in rows:
        path = vp.article_path(r)
        if not path.is_file():
            continue
        body = article_body(path.read_text(encoding="utf-8"))
        rid = vp.safe_str(r.get("ID"))
        bodies[rid] = body
        if family(r) == "actuel" or all(vp.section(body, s) is not None for s in vp.SECTIONS):
            current.add(rid)

    inbound_current: dict[str, set[str]] = defaultdict(set)
    inbound_other: dict[str, set[str]] = defaultdict(set)
    for rid, body in bodies.items():
        for url in vp.INTERNAL_LINK_RE.findall(body):
            post = vp.wp_post_id(url)
            target = by_post.get(post) if post else by_url.get(vp.norm_url(url))
            tid = vp.safe_str(target.get("ID")) if target else ""
            if tid and tid != rid:
                (inbound_current if rid in current else inbound_other)[tid].add(rid)

    refs: dict[str, int] = defaultdict(int)
    ref_texts = [p.read_text(encoding="utf-8") for p in REF_FILES if p.is_file()]
    ref_texts += [p.read_text(encoding="utf-8") for p in (ROOT / "03_Dossiers").rglob("*.md")]
    in_manifest = set(ID_RE.findall(vp.MANIFEST_PATH.read_text(encoding="utf-8-sig")))
    out_of_scope_by_url = {vp.norm_url(vp.safe_str(r.get("URL_WordPress"))): r for r in rows
                           if (vp.is_fonds(r) or family(r) == "wiki") and vp.safe_str(r.get("URL_WordPress"))}
    for text in ref_texts:
        for rid in ID_RE.findall(text):
            refs[rid] += 1
        for url in re.findall(r"https?://(?:www\.)?le-phare\.info[^\s)\],;\"]*", text):
            target = by_url.get(vp.norm_url(url))
            if target:
                refs[vp.safe_str(target.get("ID"))] += 1

    scope = [r for r in rows if not vp.is_fonds(r) and family(r) != "wiki" and vp.safe_str(r.get("ID")) not in current]
    wp_words: dict[str, int] = {}
    if not a.offline and vp.CONFIG_PATH.exists():
        wp_words = fetch_wp_words([r for r in scope if vp.safe_str(r.get("Statut")) == "publie"])

    def score(r: dict[str, str]) -> int:
        rid = vp.safe_str(r.get("ID"))
        return 3 * len(inbound_current[rid]) + len(inbound_other[rid]) + 2 * refs[rid] + (2 if r.get("Type") == "TF" else 0)

    groups: dict[str, list[dict[str, str]]] = defaultdict(list)
    for r in scope:
        key = title_key(vp.safe_str(r.get("Titre")))
        if len(key.split()) >= 3:
            groups[key].append(r)
    dupe_of: dict[str, str] = {}
    for members in groups.values():
        if len(members) > 1:
            keep = max(members, key=lambda r: (score(r), vp.safe_str(r.get("Statut")) == "publie", vp.safe_str(r.get("ID"))))
            for r in members:
                if r is not keep:
                    dupe_of[vp.safe_str(r.get("ID"))] = vp.safe_str(keep.get("ID"))

    entries = []
    for r in scope:
        rid = vp.safe_str(r.get("ID"))
        title = html.unescape(vp.safe_str(r.get("Titre")))
        body = bodies.get(rid)
        local = words(body) if body is not None else 0
        wp = wp_words.get(rid)
        notes = []
        if body is None:
            notes.append("fichier absent")
        else:
            missing = [s for s in vp.SECTIONS if vp.section(body, s) is None]
            if missing:
                notes.append("navigation incomplète")
            if "Dans ce triptyque" in body:
                notes.append("« Dans ce triptyque »")
            if vp.P_LINK_RE.search(body):
                notes.append("liens ?p=")
        if EMOJI_RE.search(title):
            notes.append("emoji dans le titre")
        if wp and wp > TRUNCATED_RATIO * max(local, 1):
            notes.append("**copie locale tronquée**")
        if rid in in_manifest:
            notes.append("rattaché à un fondamental")
        twin = out_of_scope_by_url.get(vp.norm_url(vp.safe_str(r.get("URL_WordPress"))))

        published = vp.safe_str(r.get("Statut")) == "publie"
        if twin:
            where = "`02_Fonds/`" if vp.is_fonds(twin) else "wiki"
            tier, action = "Trier", f"ligne d'index en double de {vp.safe_str(twin.get('ID'))} ({where}, même URL) : retirer ce doublon ?"
        elif not published:
            tier, action = "Trier", "brouillon jamais publié : archiver ou supprimer"
        elif rid in dupe_of:
            tier, action = "Trier", f"doublon possible de {dupe_of[rid]} : fusionner ou dépublier"
        elif len(title_key(title).split()) <= 2 and EMOJI_RE.search(title):
            tier, action = "Trier", "page rubrique : garder hors flux (retirer a-la-une ?)"
        elif not a.offline and wp_words and wp is None:
            tier, action = "Trier", "post introuvable sur WordPress"
        elif inbound_current[rid] or refs[rid] or (r.get("Type") == "TF" and score(r) >= 3):
            tier, action = "Refaire", "réécriture au format actuel (même ID, même URL)"
        else:
            tier, action = "Remettre à niveau", "navigation finale + titre, sans réécriture"
        entries.append((tier, score(r), rid, title, r, local, wp, notes, action))

    order = {"Refaire": 0, "Remettre à niveau": 1, "Trier": 2}
    entries.sort(key=lambda e: (order[e[0]], -e[1], e[2]))

    n_fonds = sum(1 for r in rows if vp.is_fonds(r))
    n_wiki = sum(1 for r in rows if not vp.is_fonds(r) and family(r) == "wiki")
    counts = defaultdict(int)
    for e in entries:
        counts[e[0]] += 1

    lines = [
        "# Inventaire de rénovation",
        "",
        f"> Généré par `tools/build_inventaire_renovation.py` le {date.today().isoformat()} — ne pas éditer à la main.",
        "> Plan d'action : `plan.md` §19.",
        "",
        "| Catégorie | Articles |",
        "|---|---|",
        f"| Format actuel (rien à faire) | {len(current)} |",
        f"| **Refaire** | {counts['Refaire']} |",
        f"| **Remettre à niveau** | {counts['Remettre à niveau']} |",
        f"| **Trier** (décision humaine) | {counts['Trier']} |",
        f"| Hors périmètre : fondamentaux `02_Fonds/` (éditeur humain) | {n_fonds} |",
        f"| Hors périmètre : wiki du Phare (`Sentier_dedoublonnage_wiki.md`) | {n_wiki} |",
        "",
        "Liens entrants : `récents/autres/réf.` = articles au format actuel / autres articles / mentions Radar, mémoire, dossiers.",
        "Mots : markdown local / WordPress (`?` = non mesuré).",
    ]
    for tier in order:
        lines += ["", f"## {tier}", "", "| ID | Titre | Type | Famille | Liens entrants | Mots | Constats | Action |", "|---|---|---|---|---|---|---|---|"]
        for t, _, rid, title, r, local, wp, notes, action in entries:
            if t != tier:
                continue
            link = f"[{vp.safe_str(r.get('Type'))}]({vp.safe_str(r.get('URL_WordPress'))})" if vp.safe_str(r.get("URL_WordPress")) else vp.safe_str(r.get("Type"))
            title_cell = title.replace("|", "/")
            title_cell = title_cell if len(title_cell) <= 70 else title_cell[:69].rstrip() + "…"
            lines.append(
                f"| {rid} | {title_cell} | {link} | {family(r)} | "
                f"{len(inbound_current[rid])}/{len(inbound_other[rid])}/{refs[rid]} | {local}/{wp if wp is not None else '?'} | "
                f"{', '.join(notes)} | {action} |"
            )
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: {OUT.relative_to(ROOT)} — Refaire {counts['Refaire']}, Remettre à niveau {counts['Remettre à niveau']}, "
          f"Trier {counts['Trier']}, format actuel {len(current)}, hors périmètre {n_fonds + n_wiki}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
