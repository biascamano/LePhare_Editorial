#!/usr/bin/env python3
"""
Import WordPress posts into the Le Phare Editorial repo layout.

- Authenticated REST API (application password) to read all statuses.
- Resolves Type / Theme / target folder from WP categories (see ROUTING_* maps).
- Converts HTML body to a simplified Markdown (recovery-oriented).
- Appends new rows to index_editorial.csv for posts not yet indexed (by slug).

Safety defaults:
  Dry-run unless --apply.
  Skips posts whose Slug_WordPress already exists in index (--force-new still assigns new IDs only for unknown slugs).

Usage:
  python tools/import_wp_posts.py --dry-run
  python tools/import_wp_posts.py --apply --limit 50
  python tools/import_wp_posts.py --apply --refresh-existing
"""
from __future__ import annotations

import argparse
import csv
import html as html_module
import re
import sys
from datetime import date, datetime
from pathlib import Path
from urllib import parse

ROOT_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = Path(__file__).resolve().parent
INDEX_DEFAULT = ROOT_DIR / "index_editorial.csv"
CONFIG_DEFAULT = TOOLS_DIR / "wp_config.local.json"

sys.path.insert(0, str(TOOLS_DIR))
from wp_push_draft import Config, load_config, wordpress_request_json  # noqa: E402

THEME_FROM_CAT_SLUG: dict[str, str] = {
    "economie-finance": "ECON",
    "geopolitique-relations-internationales": "MONDE",
    "politique-societe": "POL",
    "technologie-intelligence-artificielle": "TECH",
    "environnement-climat": "CLIMAT",
    "science-sante": "SCIENCE",
    "economie": "ECON",
    "monde": "MONDE",
    "geopolitique": "MONDE",
    "diplomatie": "MONDE",
    "actualites-politique-societe": "POL",
    "01-actualites-politique-societe": "POL",
}

THEME_FROM_TAG_SLUG: dict[str, str] = {
    "economie-finance": "ECON",
    "economie": "ECON",
    "crise-energetique": "ECON",
    "geopolitique": "MONDE",
    "politique-societe": "POL",
    "sentier": "CULTURE",
}

ACTU_SUBDIR: dict[str, str] = {
    "ECON": "01_Actualites/Economie_Finance",
    "MONDE": "01_Actualites/Politique_Societe",
    "POL": "01_Actualites/Politique_Societe",
    "TECH": "01_Actualites/Politique_Societe",
    "CLIMAT": "01_Actualites/Politique_Societe",
    "SCIENCE": "01_Actualites/Politique_Societe",
    "CULTURE": "01_Actualites/Politique_Societe",
}

SKIP_CATEGORY_SLUGS = frozenset({"non-classe", "uncategorized", "description-categories", "all"})


def crude_html_to_markdown(html: str) -> str:
    if not html:
        return ""
    text = html
    text = re.sub(r"(?is)<script[^>]*>.*?</script>", "", text)
    text = re.sub(r"(?is)<style[^>]*>.*?</style>", "", text)
    text = re.sub(r"(?is)<!--.*?-->", "", text)
    block_pairs = [
        (r"(?is)<h1[^>]*>", "\n\n# "),
        (r"</h1>", "\n"),
        (r"(?is)<h2[^>]*>", "\n\n## "),
        (r"</h2>", "\n"),
        (r"(?is)<h3[^>]*>", "\n\n### "),
        (r"</h3>", "\n"),
        (r"(?is)<h4[^>]*>", "\n\n#### "),
        (r"</h4>", "\n"),
        (r"(?is)<li[^>]*>", "\n- "),
        (r"(?is)</li>", ""),
        (r"(?is)<p[^>]*>", "\n\n"),
        (r"(?is)</p>", "\n"),
        (r"(?is)<br\s*/?>", "\n"),
        (r"(?is)<blockquote[^>]*>", "\n\n> "),
        (r"(?is)</blockquote>", "\n"),
    ]
    for pat, repl in block_pairs:
        text = re.sub(pat, repl, text)
    text = re.sub(r"(?is)<a[^>]*href=[\"']([^\"']+)[\"'][^>]*>", r"[\1](\1) ", text)
    text = re.sub(r"</a>", "", text)
    text = re.sub(r"(?is)<strong[^>]*>|</strong>|<b[^>]*>|</b>", "**", text)
    text = re.sub(r"(?is)<em[^>]*>|</em>|<i[^>]*>|</i>", "*", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = html_module.unescape(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_html(inner: str) -> str:
    if not inner:
        return ""
    t = re.sub(r"<[^>]+>", " ", inner)
    return html_module.unescape(re.sub(r"\s+", " ", t)).strip()


def post_rendered(field: object) -> str:
    if isinstance(field, dict):
        return str(field.get("rendered") or "")
    return ""


def extract_terms_embedded(post: dict) -> tuple[list[dict], list[dict]]:
    cats: list[dict] = []
    tags: list[dict] = []
    embedded = post.get("_embedded") or {}
    terms = embedded.get("wp:term") or []
    for group in terms:
        if not isinstance(group, list):
            continue
        for term in group:
            if not isinstance(term, dict):
                continue
            tax = term.get("taxonomy")
            if tax == "category":
                cats.append(term)
            elif tax == "post_tag":
                tags.append(term)
    return cats, tags


def category_slugs(cats: list[dict]) -> list[str]:
    return [str(c.get("slug") or "").strip().lower() for c in cats if c.get("slug")]


def tag_slugs(tags: list[dict]) -> list[str]:
    return [str(t.get("slug") or "").strip().lower() for t in tags if t.get("slug")]


def infer_theme(cat_slugs: list[str], tag_sl_l: list[str]) -> str:
    for s in cat_slugs:
        if s in THEME_FROM_CAT_SLUG:
            return THEME_FROM_CAT_SLUG[s]
    for s in tag_sl_l:
        if s in THEME_FROM_TAG_SLUG:
            return THEME_FROM_TAG_SLUG[s]
    return "CULTURE"


def resolve_routing(cat_slugs: set[str]) -> tuple[str, str, str]:
    """
    Returns (Type, Theme_code, Chemin_dossier relative to ROOT).
    """
    # Textes fondateurs (memoire hub or explicit slugs)
    if {"textes-fondateurs", "textes-fondateurs-auteurs", "04-textes-fondateurs-auteurs"} & cat_slugs:
        theme = infer_theme(list(cat_slugs), [])
        return "TF", theme, "04_Textes_fondateurs/Auteurs"

    # Sentier (flat or subtree markers)
    sentier_markers = {
        "sentier",
        "sentier-du-savoir",
        "05-sentier-etape-06-methode-scientifique",
        "05-sentier-etape-08-rlier-savoirs-et-experience",
        "step-08-relier-savoirs-et-experience",
        "lire-un-choc-energetique",
    }
    if cat_slugs & sentier_markers:
        theme = infer_theme(list(cat_slugs), [])
        # Etape folders when slug hints step
        if "05-sentier-etape-08-rlier-savoirs-et-experience" in cat_slugs or "step-08-relier-savoirs-et-experience" in cat_slugs:
            sub = "05_Sentier/Etape_08_Relier_savoirs_et_experience"
        elif "05-sentier-etape-06-methode-scientifique" in cat_slugs:
            sub = "05_Sentier/Etape_06_Methode_scientifique"
        else:
            sub = "05_Sentier/Culture"
        return "SENTIER", theme, sub

    # Cycle postures (homepage methodology) -> fond / archival lecture path
    cycle_slugs = {"observer", "comprendre", "relier", "mettre-a-distance", "transmettre", "architecture"}
    if "cycle" in cat_slugs or cat_slugs & cycle_slugs:
        theme = infer_theme(list(cat_slugs), [])
        return "FOND", theme, "02_Fonds/Culture"

    # Memoire hub (non-TF)
    if "memoire" in cat_slugs or "cycles-aboutis" in cat_slugs or "articles-de-fond" in cat_slugs:
        theme = infer_theme(list(cat_slugs), [])
        return "FOND", theme, "02_Fonds/Culture"

    # Actualités WP slug + thematic mains under "all"
    actu_family = {
        "actualites",
        "economie-finance",
        "geopolitique-relations-internationales",
        "politique-societe",
        "technologie-intelligence-artificielle",
        "environnement-climat",
        "science-sante",
        "actualites-politique-societe",
        "01-actualites-politique-societe",
        "economie",
        "monde",
        "geopolitique",
        "diplomatie",
        "dossier-hebdomadaire",
    }
    if cat_slugs & actu_family:
        theme = infer_theme(list(cat_slugs), [])
        sub = ACTU_SUBDIR.get(theme, "01_Actualites/Politique_Societe")
        return "ACTU", theme, sub

    # Fallback institutional / pages-like
    if cat_slugs & {"home", "le-phare-info", "projet"}:
        return "FOND", "CULTURE", "02_Fonds/Culture"

    theme = infer_theme(list(cat_slugs), [])
    return "FOND", theme, "02_Fonds/Culture"


def fetch_posts_page(config: Config, *, page: int, statuses: str) -> list[dict]:
    qs = parse.urlencode(
        {
            "per_page": 100,
            "page": page,
            "status": statuses,
            "_embed": "1",
            "context": "edit",
        }
    )
    endpoint = f"{config.site_url}/wp-json/wp/v2/posts?{qs}"
    result = wordpress_request_json(config, endpoint, method="GET")
    if not isinstance(result, list):
        raise RuntimeError(f"Unexpected posts payload: {type(result)}")
    return result


def load_index(path: Path) -> tuple[list[str], list[dict]]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


def max_numeric_suffix(rows: list[dict]) -> int:
    best = 0
    for r in rows:
        rid = (r.get("ID") or "").strip()
        if not rid.startswith("2026-"):
            continue
        try:
            best = max(best, int(rid.split("-", 1)[1]))
        except ValueError:
            continue
    return best


def slug_index_maps(rows: list[dict]) -> tuple[dict[str, dict], dict[int, dict]]:
    by_slug: dict[str, dict] = {}
    by_wp_id: dict[int, dict] = {}
    for r in rows:
        s = (r.get("Slug_WordPress") or "").strip().lower()
        if s:
            by_slug[s] = r
        url = r.get("URL_WordPress") or ""
        m = re.search(r"[?&]p=(\d+)", url)
        if m:
            by_wp_id[int(m.group(1))] = r
    return by_slug, by_wp_id


def find_existing_row(
    by_slug: dict[str, dict],
    by_wp_id: dict[int, dict],
    *,
    slug: str,
    wp_post_id: int,
) -> dict | None:
    s = slug.lower().strip()
    candidates = [s]
    base_match = re.search(r"-(\d+)$", s)
    if base_match:
        base = s[: base_match.start()]
        candidates.extend([base, base + "-2"])
    else:
        candidates.append(s + "-2")
    seen: set[str] = set()
    for c in candidates:
        if c in seen:
            continue
        seen.add(c)
        row = by_slug.get(c)
        if row:
            return row
    return by_wp_id.get(wp_post_id)


def categorie_wp_field(cat_terms: list[dict]) -> str:
    names = []
    for c in cat_terms:
        name = (c.get("name") or "").strip()
        slug = (c.get("slug") or "").strip()
        if slug.lower() in SKIP_CATEGORY_SLUGS:
            continue
        names.append(name or slug)
    return ";".join(names[:4])


def tags_wp_field(tag_terms: list[dict]) -> str:
    slugs = [str(t.get("slug") or "").strip() for t in tag_terms if t.get("slug")]
    return ";".join(slugs[:12])


def build_markdown_frontmatter(
    *,
    article_id: str,
    title: str,
    type_: str,
    theme: str,
    statut_wp: str,
    excerpt_plain: str,
    wp_link: str,
    cats: list[dict],
    tags: list[dict],
) -> str:
    statut = "publie" if statut_wp == "publish" else ("brouillon" if statut_wp == "draft" else statut_wp)
    resume = excerpt_plain[:500] if excerpt_plain else ""
    mc = ", ".join(str(t.get("name") or t.get("slug")) for t in tags[:8])
    lines = [
        f"ID article : {article_id}",
        f"Titre : {title}",
        f"Type : {type_}",
        f"Theme : {theme}",
        f"Statut : {statut}",
        "Version : V1",
        f"Date de creation : {date.today().isoformat()}",
        f"Date de derniere mise a jour : {date.today().isoformat()}",
        "Auteur : Le Phare Info",
        "Etape du Sentier liee : ",
        "Articles lies (IDs) : ",
        f"Mots-cles : {mc}",
        f"Resume court (500 caracteres max) : {resume}",
        "Objectif de l'article : ",
        "Sources principales : Import WordPress REST API",
        f"URL WordPress (si publie) : {wp_link}",
        "---",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Import WP posts into repo folders + index.")
    parser.add_argument("--config", default=str(CONFIG_DEFAULT), help="wp_config.local.json path")
    parser.add_argument("--index", default=str(INDEX_DEFAULT), help="index_editorial.csv path")
    parser.add_argument(
        "--statuses",
        default="publish,draft,future,pending,private",
        help="Comma-separated WP post statuses to fetch",
    )
    parser.add_argument("--dry-run", action="store_true", help="Plan only (default if neither apply)")
    parser.add_argument("--apply", action="store_true", help="Write files and update index")
    parser.add_argument("--limit", type=int, default=0, help="Max posts to process (0=all)")
    parser.add_argument(
        "--refresh-existing",
        action="store_true",
        help="Rewrite markdown for posts already in index (matched by slug or ?p=id)",
    )
    parser.add_argument(
        "--include-skipped-categories",
        action="store_true",
        help="Still import posts only classified as Non classe / Uncategorized (noisy)",
    )
    args = parser.parse_args()

    do_apply = args.apply
    if not args.apply and not args.dry_run:
        print("No --apply: running dry-run. Pass --apply to write.", file=sys.stderr)
        do_apply = False

    config = load_config(args.config)
    index_path = Path(args.index)
    fieldnames, rows = load_index(index_path)
    by_slug, by_wp_id = slug_index_maps(rows)
    next_num = max_numeric_suffix(rows) + 1

    page = 1
    total_seen = 0
    planned_new = 0
    planned_refresh = 0
    skipped = 0
    new_rows: list[dict] = []

    while True:
        batch = fetch_posts_page(config, page=page, statuses=args.statuses)
        if not batch:
            break
        for post in batch:
            if args.limit and total_seen >= args.limit:
                batch = []
                break
            total_seen += 1
            pid = int(post.get("id") or 0)
            slug = str(post.get("slug") or "").strip().lower()
            title_raw = post_rendered(post.get("title"))
            title = html_module.unescape(strip_html(title_raw) or slug)
            status = str(post.get("status") or "")
            link = str(post.get("link") or "").strip()
            content_html = post_rendered(post.get("content"))
            excerpt_html = post_rendered(post.get("excerpt"))

            cats, tags = extract_terms_embedded(post)
            cat_sl = category_slugs(cats)
            tag_sl = tag_slugs(tags)
            cat_set = set(cat_sl)

            noise_only = bool(cat_sl) and cat_set <= SKIP_CATEGORY_SLUGS and not tags
            if noise_only and not args.include_skipped_categories:
                skipped += 1
                continue

            type_, _, rel_dir = resolve_routing(cat_set)
            theme = infer_theme(cat_sl, tag_sl)

            excerpt_plain = strip_html(excerpt_html)
            body_md = crude_html_to_markdown(content_html)

            existing = find_existing_row(by_slug, by_wp_id, slug=slug, wp_post_id=pid)
            if existing and not args.refresh_existing:
                skipped += 1
                continue
            if existing and args.refresh_existing:
                article_id = existing["ID"]
                nom = existing.get("Nom_fichier") or f"{article_id}_{type_}_{theme}_{slug}_V1.md"
                chemin = existing.get("Chemin_dossier") or rel_dir.replace("/", "\\")
                planned_refresh += 1
                action_idx = planned_refresh
            else:
                article_id = f"2026-{next_num:03d}"
                next_num += 1
                slug_safe = re.sub(r"[^a-zA-Z0-9_-]+", "_", slug)[:80]
                nom = f"{article_id}_{type_}_{theme}_{slug_safe}_V1.md"
                chemin = rel_dir
                planned_new += 1
                action_idx = planned_new

            front = build_markdown_frontmatter(
                article_id=article_id,
                title=title,
                type_=type_,
                theme=theme,
                statut_wp=status,
                excerpt_plain=excerpt_plain,
                wp_link=link,
                cats=cats,
                tags=tags,
            )
            full_md = front + "\n" + body_md + "\n"

            target_path = ROOT_DIR / Path((chemin or rel_dir).replace("\\", "/")) / nom

            if existing and args.refresh_existing:
                target_path = ROOT_DIR / Path(existing["Chemin_dossier"].replace("\\", "/")) / existing["Nom_fichier"]

            print(f"{action_idx:>4}  wp_id={pid}  {type_:8}  {theme:8}  {target_path.relative_to(ROOT_DIR)}")

            if do_apply:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(full_md, encoding="utf-8")

            if not existing:
                pub_date = (post.get("date") or "")[:10]
                row = {k: "" for k in fieldnames}
                row.update(
                    {
                        "ID": article_id,
                        "Titre": title,
                        "Type": type_,
                        "Theme": theme,
                        "Statut": "publie" if status == "publish" else "brouillon",
                        "Version": "V1",
                        "Date_creation": pub_date or date.today().isoformat(),
                        "Date_derniere_maj": date.today().isoformat(),
                        "Auteur": "Le Phare Info",
                        "Etape_sentier": "",
                        "Articles_lies": "",
                        "Mots_cles": ",".join(str(t.get("name") or "") for t in tags[:12]),
                        "Resume_court": excerpt_plain[:500],
                        "Objectif": "",
                        "Nom_fichier": nom,
                        "Chemin_dossier": str(target_path.parent.relative_to(ROOT_DIR)).replace("/", "\\"),
                        "Date_publication_WP": pub_date,
                        "URL_WordPress": link,
                        "Slug_WordPress": slug,
                        "Categorie_WP": categorie_wp_field(cats),
                        "Tags_WP": tags_wp_field(tags),
                        "Remarques": "Import tools/import_wp_posts.py",
                    }
                )
                # Normalize keys to fieldnames order
                ordered = {fn: row.get(fn, "") for fn in fieldnames}
                new_rows.append(ordered)
                by_slug[(ordered.get("Slug_WordPress") or "").strip().lower()] = ordered

        if not batch or (args.limit and total_seen >= args.limit):
            break
        page += 1

    print(f"\nSummary: fetched_batches_done pages={page} posts_seen={total_seen}", file=sys.stderr)
    print(f"planned_new={planned_new} refresh={planned_refresh} skipped_existing_or_noise={skipped}", file=sys.stderr)

    if do_apply and new_rows:
        backup = index_path.with_suffix(".csv.bak_import_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
        backup.write_text(index_path.read_text(encoding="utf-8-sig"), encoding="utf-8-sig")
        rows.extend(new_rows)
        with index_path.open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(rows)
        print(f"Index updated (+{len(new_rows)} rows). Backup: {backup}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
