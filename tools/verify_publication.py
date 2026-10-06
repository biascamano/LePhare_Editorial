#!/usr/bin/env python3
"""Vérification de fin de routine : liens, maillage interne, visibilité WordPress.

Contrôles (articles du périmètre) :
- fichier canonique présent ;
- liens internes : `?p=N` (permalien manquant), lien vers un brouillon, URL le-phare.info inconnue
  de l'index et du manifeste Sentier ;
- URL nue (non cliquable sur WordPress) ;
- maillage : sections « La question suivante », « Pour aller plus loin », « Sur le Sentier du Savoir » ;
  Question/Application → lien vers l'article d'origine ; origine → lien vers la Question qui la prolonge ;
  en-tête `Dossier :` → lien vers le dossier ;
- WordPress (sauf --offline) : statut réel du post et tag `a-la-une` (sans ce tag, l'article n'est pas
  visible sur le site) ; écart entre statut WP et index.

Usage :
    python tools/verify_publication.py [IDs…] [--days 7] [--offline]
    python tools/verify_publication.py --fix              # tag a-la-une manquant, liens ?p= → permaliens, refresh WP
    python tools/verify_publication.py --publish-drafts   # publie les brouillons sans erreur bloquante, puis --fix

Périmètre par défaut : articles créés depuis --days jours (hors 02_Fonds/). Les anciens brouillons
n'entrent que par leurs IDs : --publish-drafts ne publie donc jamais un vieux brouillon par accident.
Code de sortie : 0 si aucune erreur, 1 sinon (les avertissements ne bloquent pas).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from urllib import parse

from index_editorial_utils import read_index, safe_str, write_index
from wp_push_draft import Config, load_config, wordpress_request_json

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
INDEX_PATH = ROOT / "index_editorial.csv"
MANIFEST_PATH = ROOT / "00_Systeme" / "Manifests" / "sentier_fondamentaux.csv"
CONFIG_PATH = TOOLS_DIR / ("wp_config" + ".local.json")
SITE = "le-phare.info"
FRONT_TAG = "a-la-une"

INTERNAL_LINK_RE = re.compile(r"\]\((https?://(?:www\.)?le-phare\.info[^)\s]*)\)")
P_LINK_RE = re.compile(r"https?://(?:www\.)?le-phare\.info/\?p=(\d+)")
BARE_URL_RE = re.compile(r"(?<![(<\[])\bhttps?://[^\s)>\]]+")
SECTIONS = ("La question suivante", "Pour aller plus loin", "Sur le Sentier du Savoir")


@dataclass
class Report:
    article_id: str
    title: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def norm_url(url: str) -> str:
    url = safe_str(url).replace("://www.", "://")
    return url if "?p=" in url else url.rstrip("/") + "/"


def wp_post_id(url: str) -> int | None:
    raw = parse.parse_qs(parse.urlparse(url).query).get("p", [""])[0]
    return int(raw) if raw.isdigit() else None


def article_path(row: dict[str, str]) -> Path:
    return ROOT / safe_str(row.get("Chemin_dossier")) / safe_str(row.get("Nom_fichier"))


def is_fonds(row: dict[str, str]) -> bool:
    return safe_str(row.get("Chemin_dossier")).replace("\\", "/").startswith("02_Fonds")


def split_article(text: str) -> tuple[dict[str, str], str]:
    head, _, body = text.partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        if " : " in line or line.rstrip().endswith(" :"):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
    body = body.split("\n# SEO", 1)[0]
    return meta, body


def section(body: str, name: str) -> str | None:
    m = re.search(rf"^\*\*{re.escape(name)}\*\*\s*$(.*?)(?=^\*\*[^*\n]+\*\*\s*$|^# |\Z)", body, re.M | re.S)
    return m.group(1) if m else None


def load_manifest_urls() -> set[str]:
    import csv

    with MANIFEST_PATH.open(encoding="utf-8-sig", newline="") as fh:
        return {norm_url(r["url_canonique"]) for r in csv.DictReader(fh) if safe_str(r.get("url_canonique"))}


def select_scope(rows: list[dict[str, str]], ids: list[str], days: int) -> list[dict[str, str]]:
    if ids:
        wanted = set(ids)
        return [r for r in rows if safe_str(r.get("ID")) in wanted]
    since = (date.today() - timedelta(days=days)).isoformat()
    return [r for r in rows if not is_fonds(r) and safe_str(r.get("Date_creation")) >= since]


def check_local(
    row: dict[str, str],
    by_id: dict[str, dict[str, str]],
    by_url: dict[str, dict[str, str]],
    by_post: dict[int, dict[str, str]],
    manifest_urls: set[str],
    followers: dict[str, list[str]],
) -> Report:
    rid = safe_str(row.get("ID"))
    rep = Report(rid, safe_str(row.get("Titre")))
    path = article_path(row)
    if not path.is_file():
        rep.errors.append(f"fichier canonique absent : {path.relative_to(ROOT)}")
        return rep
    meta, body = split_article(path.read_text(encoding="utf-8"))

    for url in INTERNAL_LINK_RE.findall(body):
        post = wp_post_id(url)
        target = by_post.get(post) if post else by_url.get(norm_url(url))
        if target is None:
            if norm_url(url) not in manifest_urls:
                rep.warnings.append(f"lien interne inconnu de l'index : {url}")
            continue
        tid = safe_str(target.get("ID"))
        if safe_str(target.get("Statut")) != "publie":
            rep.warnings.append(f"lien vers un brouillon : {tid} ({url})")
        elif post:
            rep.warnings.append(f"lien ?p= à remplacer par le permalien : {tid}")

    for line in body.splitlines():
        for url in BARE_URL_RE.findall(line):
            if f"]({url}" not in line:
                rep.errors.append(f"URL nue : {url}")

    type_article = meta.get("Type article", "")
    if safe_str(row.get("Type")) in {"ACTU", "TF", "SYNTHESE"}:
        for name in SECTIONS:
            if section(body, name) is None:
                rep.warnings.append(f"section absente : {name}")
        sentier = section(body, "Sur le Sentier du Savoir")
        if sentier is not None and not INTERNAL_LINK_RE.search(sentier):
            rep.warnings.append("Sentier du Savoir sans lien")
        further = section(body, "Pour aller plus loin")
        if further is not None and not INTERNAL_LINK_RE.search(further):
            rep.warnings.append("Pour aller plus loin sans lien interne")

    links = {norm_url(u) for u in INTERNAL_LINK_RE.findall(body)}

    def links_to(target_id: str) -> bool:
        target = by_id.get(target_id)
        return bool(target) and norm_url(safe_str(target.get("URL_WordPress"))) in links

    prev = meta.get("Article precedent (ID)", "")
    if type_article in {"Question", "Application"} and prev and not links_to(prev):
        rep.warnings.append(f"pas de lien vers l'article d'origine {prev}")
    for follower in followers.get(rid, []):
        nxt = section(body, "La question suivante") or ""
        target = by_id.get(follower)
        if target and norm_url(safe_str(target.get("URL_WordPress"))) not in {norm_url(u) for u in INTERNAL_LINK_RE.findall(nxt)}:
            rep.warnings.append(f"« La question suivante » ne renvoie pas vers {follower}")
    dossier = meta.get("Dossier", "")
    if dossier and dossier != rid and safe_str(row.get("Type")) != "DOSSIER" and not links_to(dossier):
        rep.warnings.append(f"pas de lien vers le dossier {dossier}")
    return rep


def build_followers(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    """Origine → Questions/Applications qui la prolongent (lecture des en-têtes des 120 derniers articles)."""
    followers: dict[str, list[str]] = {}
    for row in sorted(rows, key=lambda r: safe_str(r.get("ID")))[-120:]:
        path = article_path(row)
        if not path.is_file():
            continue
        meta, _ = split_article(path.read_text(encoding="utf-8"))
        prev = meta.get("Article precedent (ID)", "")
        if meta.get("Type article") in {"Question", "Application"} and prev:
            followers.setdefault(prev, []).append(safe_str(row.get("ID")))
    return followers


def fetch_wp_posts(config: Config, scope: list[dict[str, str]]) -> dict[str, dict]:
    statuses = "publish,draft,pending,private,future"
    fields = "id,slug,status,link,tags"
    out: dict[str, dict] = {}
    by_post = {wp_post_id(safe_str(r.get("URL_WordPress"))): safe_str(r.get("ID")) for r in scope}
    ids = [str(p) for p in by_post if p]
    for i in range(0, len(ids), 50):
        chunk = ",".join(ids[i:i + 50])
        items = wordpress_request_json(
            config, f"{config.site_url}/wp-json/wp/v2/posts?include={chunk}&status={statuses}&per_page=50&_fields={fields}", "GET"
        )
        for item in items if isinstance(items, list) else []:
            out[by_post[item["id"]]] = item
    by_slug = {safe_str(r.get("Slug_WordPress")): safe_str(r.get("ID")) for r in scope
               if safe_str(r.get("ID")) not in out and safe_str(r.get("Slug_WordPress"))}
    slugs = list(by_slug)
    for i in range(0, len(slugs), 50):
        chunk = ",".join(parse.quote(s) for s in slugs[i:i + 50])
        items = wordpress_request_json(
            config, f"{config.site_url}/wp-json/wp/v2/posts?slug={chunk}&status={statuses}&per_page=50&_fields={fields}", "GET"
        )
        for item in items if isinstance(items, list) else []:
            if item.get("slug") in by_slug:
                out[by_slug[item["slug"]]] = item
    return out


def front_tag_id(config: Config) -> int:
    items = wordpress_request_json(config, f"{config.site_url}/wp-json/wp/v2/tags?slug={FRONT_TAG}", "GET")
    if not isinstance(items, list) or not items:
        raise RuntimeError(f"Tag WordPress « {FRONT_TAG} » introuvable")
    return int(items[0]["id"])


def check_wp(rep: Report, row: dict[str, str], post: dict | None, tag_id: int) -> None:
    if post is None:
        rep.errors.append("post WordPress introuvable")
        return
    status = post.get("status")
    if status == "publish":
        if safe_str(row.get("Statut")) != "publie":
            rep.warnings.append("publié sur WP mais `wp_draft` dans l'index")
        if tag_id not in post.get("tags", []):
            rep.errors.append(f"tag {FRONT_TAG} absent : article invisible sur le site")
    else:
        rep.warnings.append(f"statut WP : {status} (non publié)")


def mark_published(rows: list[dict[str, str]], rid: str, post: dict) -> None:
    today = date.today().isoformat()
    for row in rows:
        if safe_str(row.get("ID")) == rid:
            row["Statut"] = "publie"
            row["Date_publication_WP"] = row.get("Date_publication_WP") or today
            row["Date_derniere_maj"] = today
            if post.get("link"):
                row["URL_WordPress"] = post["link"]
            if post.get("slug"):
                row["Slug_WordPress"] = post["slug"]
            return


def rewrite_p_links(rows: list[dict[str, str]], by_post: dict[int, dict[str, str]]) -> list[dict[str, str]]:
    """Remplace `?p=N` par le permalien quand la cible est publiée ; renvoie les articles modifiés.

    `by_post` est construit avant `mark_published` : il garde le N d'origine alors que la ligne porte déjà le permalien.
    """
    changed = []
    for row in rows:
        path = article_path(row)
        if not path.is_file() or path.suffix != ".md":
            continue
        text = path.read_text(encoding="utf-8")
        if "?p=" not in text:
            continue

        def repl(m: re.Match) -> str:
            target = by_post.get(int(m.group(1)))
            url = safe_str(target.get("URL_WordPress")) if target else ""
            published = target is not None and safe_str(target.get("Statut")) == "publie"
            return url if published and url and "?p=" not in url else m.group(0)

        new = P_LINK_RE.sub(repl, text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed.append(row)
    return changed


def refresh(rows: list[dict[str, str]]) -> None:
    for row in rows:
        rel = (Path(safe_str(row.get("Chemin_dossier"))) / safe_str(row.get("Nom_fichier"))).as_posix()
        if is_fonds(row):
            print(f"  ! {row['ID']} : fondamental parent modifié en local, refresh WP manuel (éditeur)")
            continue
        if safe_str(row.get("Statut")) != "publie":
            continue
        out = subprocess.run([sys.executable, str(TOOLS_DIR / "wp_refresh_body.py"), rel], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8", errors="replace")
        print(f"  refresh {row['ID']} : {out.stdout.strip()[-300:]}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--offline", action="store_true", help="contrôles locaux seulement")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--publish-drafts", action="store_true")
    a = ap.parse_args()

    fieldnames, rows = read_index(INDEX_PATH)
    by_id = {safe_str(r.get("ID")): r for r in rows}
    by_url = {norm_url(safe_str(r.get("URL_WordPress"))): r for r in rows if safe_str(r.get("URL_WordPress"))}
    by_post = {p: r for r in rows if (p := wp_post_id(safe_str(r.get("URL_WordPress"))))}
    scope = select_scope(rows, a.ids, a.days)
    manifest_urls = load_manifest_urls()
    followers = build_followers(rows)
    reports = {safe_str(r.get("ID")): check_local(r, by_id, by_url, by_post, manifest_urls, followers) for r in scope}

    config = tag_id = None
    posts: dict[str, dict] = {}
    if not a.offline:
        if not CONFIG_PATH.exists():
            print("Config WordPress locale absente : contrôles WP ignorés (--offline).")
        else:
            config = load_config(str(CONFIG_PATH))
            tag_id = front_tag_id(config)
            posts = fetch_wp_posts(config, scope)
            for r in scope:
                check_wp(reports[safe_str(r.get("ID"))], r, posts.get(safe_str(r.get("ID"))), tag_id)

    if config and tag_id and (a.fix or a.publish_drafts):
        index_changed = False
        for r in scope:
            rid = safe_str(r.get("ID"))
            post = posts.get(rid)
            if post is None or is_fonds(r):
                continue
            rep = reports[rid]
            blocking = [e for e in rep.errors if not e.startswith(f"tag {FRONT_TAG}")]
            to_publish = a.publish_drafts and post.get("status") != "publish" and not blocking
            needs_tag = tag_id not in post.get("tags", []) and (post.get("status") == "publish" or to_publish)
            if not (to_publish or needs_tag or (post.get("status") == "publish" and safe_str(r.get("Statut")) != "publie")):
                continue
            payload: dict = {}
            if needs_tag:
                payload["tags"] = [*post.get("tags", []), tag_id]
            if to_publish:
                payload["status"] = "publish"
            if payload:
                post = wordpress_request_json(config, f"{config.site_url}/wp-json/wp/v2/posts/{post['id']}", "POST", payload)
                posts[rid] = post
            mark_published(rows, rid, post)
            index_changed = True
            rep.errors = [e for e in rep.errors if not e.startswith(f"tag {FRONT_TAG}")]
            rep.warnings = [w for w in rep.warnings if not w.startswith(("statut WP", "publié sur WP"))]
            print(f"{rid} : {'publié' if to_publish else 'mis à jour'}{' + ' + FRONT_TAG if needs_tag else ''} → {post.get('link')}")
        if index_changed:
            write_index(INDEX_PATH, fieldnames, rows)
        changed = rewrite_p_links(rows, by_post)
        if changed:
            print(f"Liens ?p= remplacés dans {len(changed)} article(s) : {', '.join(safe_str(r.get('ID')) for r in changed)}")
            refresh(changed)
        print("Relancer sans --fix pour le bilan à jour.")

    n_err = n_warn = 0
    for rid in sorted(reports):
        rep = reports[rid]
        if not (rep.errors or rep.warnings):
            continue
        print(f"\n{rid} — {rep.title[:80]}")
        rep.errors = list(dict.fromkeys(rep.errors))
        rep.warnings = list(dict.fromkeys(rep.warnings))
        for e in rep.errors:
            print(f"  ✗ {e}")
        for w in rep.warnings:
            print(f"  ! {w}")
        n_err += len(rep.errors)
        n_warn += len(rep.warnings)
    print(f"\nVérification : {len(reports)} article(s), {n_err} erreur(s), {n_warn} avertissement(s).")
    return 1 if n_err else 0


if __name__ == "__main__":
    raise SystemExit(main())
