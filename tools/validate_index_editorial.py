#!/usr/bin/env python3
"""Scan index_editorial.csv for misaligned columns (prevents WP duplicate posts on retry).

With --ids: deep v3 checks (type/path/category, tags, header, navigation, links) on given articles."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent

from index_editorial_utils import INDEX_COLUMNS, read_index, scan_index_issues  # noqa: E402

MAX_TAGS = 8
THEME_DIRS = {"MONDE": "Politique_Societe", "POL": "Politique_Societe", "ECON": "Economie_Finance", "TECH": "Technologie_IA", "CLIMAT": "Climat_Transition", "SCIENCE": "Science_Sante", "CULTURE": "Culture"}
THEME_TAGS = {"MONDE": "monde", "POL": "politique-societe", "ECON": "economie-finance", "TECH": "technologie-ia", "CLIMAT": "environnement-climat", "SCIENCE": "science-sante", "CULTURE": "culture-philosophie"}
TYPE_CATEGORY = {"ACTU": "actualites", "TF": "textes-fondateurs", "SYNTHESE": "syntheses", "DOSSIER": "dossier-hebdomadaire", "SENTIER": "sentier-du-savoir"}
V3_HEADER_KEYS = ("Type article", "Question du Phare", "Dossier", "Article precedent (ID)", "Prolongement envisage")
NAV_MARKERS = ("**Repères de sources**", "**La question suivante**", "**Pour aller plus loin**", "**Sur le Sentier du Savoir**")
PLACEHOLDER = "[Corps de l'article à rédiger]"
META_RE = re.compile(r"^(?P<key>[^:\n]+?)\s*:\s*(?P<value>.*)$")
INTERNAL_LINK_RE = re.compile(r"\]\((https?://(?:www\.)?le-phare\.info/[^)\s]*)\)")
MD_LINK_RE = re.compile(r"\]\([^)]*\)")


def expected_path_ok(type_code: str, theme: str, folder: str) -> bool:
    theme_dir = THEME_DIRS.get(theme, "")
    if type_code == "ACTU":
        return folder == f"01_Actualites/{theme_dir}"
    if type_code == "TF":
        return folder == "04_Textes_fondateurs/Auteurs"
    if type_code == "SYNTHESE":
        return folder in ("06_Syntheses/Fil_du_Phare", "06_Syntheses/Mensuelles")
    if type_code == "DOSSIER":
        return folder.startswith(f"03_Dossiers/{theme_dir}/")
    if type_code == "SENTIER":
        return re.fullmatch(r"05_Sentier/Etape_\d{2}_[^/]+", folder) is not None
    return False


def normalize_url(url: str) -> str:
    return url.strip().lower().replace("://www.", "://").rstrip("/")


def known_internal_urls(rows: list[dict[str, str]], root: Path) -> set[str]:
    urls = {normalize_url(r.get("URL_WordPress") or "") for r in rows}
    sentier_csv = root / "00_Systeme" / "Manifests" / "sentier_fondamentaux.csv"
    if sentier_csv.exists():
        with sentier_csv.open(encoding="utf-8-sig", newline="") as handle:
            urls |= {normalize_url(r.get("url_canonique") or "") for r in csv.DictReader(handle)}
    urls.discard("")
    return urls


def check_article(row: dict[str, str], rows: list[dict[str, str]], root: Path = ROOT_DIR) -> list[str]:
    errors: list[str] = []
    type_code, theme = row["Type"].strip(), row["Theme"].strip()
    folder = row["Chemin_dossier"].strip().replace("\\", "/")

    if theme not in THEME_DIRS:
        errors.append(f"thème inconnu : {theme}")
    if type_code not in TYPE_CATEGORY:
        errors.append(f"type inconnu : {type_code}")
    elif not expected_path_ok(type_code, theme, folder):
        errors.append(f"chemin {folder!r} incohérent avec {type_code}/{theme}")
    categories = [c.strip() for c in row["Categorie_WP"].split(";") if c.strip()]
    if type_code in TYPE_CATEGORY and categories != [TYPE_CATEGORY[type_code]]:
        errors.append(f"Categorie_WP {row['Categorie_WP']!r} ≠ {TYPE_CATEGORY[type_code]}")
    tags = [t.strip() for t in row["Tags_WP"].split(";") if t.strip()]
    if len(tags) > MAX_TAGS:
        errors.append(f"{len(tags)} tags > {MAX_TAGS}")
    if theme in THEME_TAGS and THEME_TAGS[theme] not in tags:
        errors.append(f"tag de thème {THEME_TAGS[theme]} absent")
    if "atelier-sentier" in tags and not any(t.startswith("fondamental-") for t in tags):
        errors.append("atelier sans tag fondamental-<ID>")

    known_ids = {(r.get("ID") or "").strip() for r in rows}
    for ref in [i.strip() for i in row["Articles_lies"].split(";") if i.strip()]:
        if ref not in known_ids:
            errors.append(f"Articles_lies : {ref} absent de l'index")

    path = root / folder / row["Nom_fichier"].strip()
    if not path.exists():
        return errors + [f"fichier introuvable : {folder}/{row['Nom_fichier']}"]
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    header_text, _, body = text.partition("\n---\n")
    header = {m["key"].strip().lstrip("﻿"): m["value"].strip() for m in map(META_RE.match, header_text.splitlines()) if m}

    if header.get("ID article") != row["ID"].strip():
        errors.append(f"ID article de l'en-tête ({header.get('ID article')}) ≠ index")
    for key in V3_HEADER_KEYS:
        if key not in header:
            errors.append(f"en-tête : champ « {key} » absent")
    if header.get("Type Sentier") == "atelier" and not header.get("Fondamental lie (ID)"):
        errors.append("atelier sans « Fondamental lie (ID) »")
    previous = header.get("Article precedent (ID)", "")
    if previous and previous not in known_ids:
        errors.append(f"Article precedent {previous} absent de l'index")
    if PLACEHOLDER in body:
        errors.append("corps non rédigé (placeholder présent)")
    for marker in NAV_MARKERS:
        if marker not in body:
            errors.append(f"navigation : {marker.strip('*')} absent")
    slug_match = re.search(r"^Slug propose\s*:\s*(\S+)", body, re.M)
    if not slug_match:
        errors.append("Slug propose absent")
    elif slug_match.group(1) != row["Slug_WordPress"].strip():
        errors.append(f"Slug propose {slug_match.group(1)} ≠ Slug_WordPress {row['Slug_WordPress']}")
    if not re.search(r"^Meta description\s*:[ \t]*\S", body, re.M):
        errors.append("Meta description vide")

    sources = body.split("**Repères de sources**", 1)[1].split("\n**", 1)[0] if "**Repères de sources**" in body else ""
    for line in sources.splitlines():
        if "http" in MD_LINK_RE.sub("", line):
            errors.append(f"URL nue dans Repères de sources : {line.strip()[:80]}")

    known_urls = known_internal_urls(rows, root)
    for url in INTERNAL_LINK_RE.findall(body):
        norm = normalize_url(url)
        if "?p=" in norm or "/category/" in norm or "/tag/" in norm:
            continue
        if norm not in known_urls:
            errors.append(f"lien interne inconnu : {url}")
    return errors


def check_ids(index_path: Path, ids: list[str], root: Path = ROOT_DIR) -> int:
    _, rows = read_index(index_path)
    by_id = {(r.get("ID") or "").strip(): r for r in rows}
    failed = 0
    for article_id in ids:
        row = by_id.get(article_id)
        errors = ["absent de l'index"] if row is None else check_article(row, rows, root)
        if errors:
            failed += 1
            print(f"KO {article_id}:")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK {article_id}")
    return 1 if failed else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate index_editorial.csv column alignment.")
    parser.add_argument(
        "--index",
        default=str(ROOT_DIR / "index_editorial.csv"),
        help="Path to index_editorial.csv",
    )
    parser.add_argument("--root", default=str(ROOT_DIR), help="Racine du projet (tests)")
    parser.add_argument("--ids", nargs="+", help="Contrôles v3 approfondis sur ces IDs")
    args = parser.parse_args()
    index_path = Path(args.index)
    if args.ids:
        return check_ids(index_path, args.ids, Path(args.root))
    issues = scan_index_issues(index_path)
    if not issues:
        print(f"OK: {index_path} ({len(INDEX_COLUMNS)} columns, no alignment issues detected).")
        return 0
    print(f"Issues in {index_path}:")
    for article_id, problems in issues:
        print(f"  {article_id}: {'; '.join(problems)}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
