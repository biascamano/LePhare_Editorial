#!/usr/bin/env python3
"""Interroge index_editorial.csv sans le lire en entier.

Par IDs (ID, Statut, URL_WordPress, Slug_WordPress) :
    python tools/index_lookup.py 2026-555 2026-556
Par recherche (ID, Type, Theme, Statut, URL, Titre ; plus récents d'abord) :
    python tools/index_lookup.py --search "indicateur" [--type ACTU] [--theme SCIENCE] [--dossier 2026-559] [--limit 20]

--search : mot-clé dans le titre, les mots-clés ou les tags (sans casse).
--type : code d'index (ACTU, TF, SENTIER, DOSSIER, SYNTHESE, FOND) ou tag de type (question, actualite, application).
--dossier : ID ou nom de dossier, cherché dans l'en-tête « Dossier : » de l'article et dans son chemin.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from index_editorial_utils import read_index, safe_str

ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT / "index_editorial.csv"


def by_ids(rows: list[dict[str, str]], ids: set[str]) -> int:
    found = set()
    for row in rows:
        row_id = safe_str(row.get("ID"))
        if row_id in ids:
            found.add(row_id)
            print(row_id, safe_str(row.get("Statut")), safe_str(row.get("URL_WordPress")), safe_str(row.get("Slug_WordPress")))
    for missing in sorted(ids - found):
        print(missing, "absent de l'index")
    return 0 if found == ids else 1


def header_dossier(row: dict[str, str]) -> str:
    path = ROOT / safe_str(row.get("Chemin_dossier")) / safe_str(row.get("Nom_fichier"))
    if not path.is_file():
        return ""
    with path.open(encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if line.startswith("---"):
                break
            if line.startswith("Dossier :"):
                return line.split(":", 1)[1].strip()
    return ""


def matches(row: dict[str, str], a: argparse.Namespace) -> bool:
    if a.search:
        hay = " ".join(safe_str(row.get(k)) for k in ("Titre", "Mots_cles", "Tags_WP")).lower()
        if a.search.lower() not in hay:
            return False
    if a.type:
        t = a.type.lower()
        if safe_str(row.get("Type")).lower() != t and f"type-{t}" not in safe_str(row.get("Tags_WP")).lower():
            return False
    if a.theme and safe_str(row.get("Theme")).lower() != a.theme.lower():
        return False
    if a.dossier:
        d = a.dossier.lower()
        if d not in safe_str(row.get("Chemin_dossier")).lower() and d not in header_dossier(row).lower():
            return False
    return True


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(usage=__doc__)
    ap.add_argument("ids", nargs="*")
    ap.add_argument("--search")
    ap.add_argument("--type")
    ap.add_argument("--theme")
    ap.add_argument("--dossier")
    ap.add_argument("--limit", type=int, default=20)
    a = ap.parse_args()
    _, rows = read_index(INDEX_PATH)
    if a.ids:
        return by_ids(rows, set(a.ids))
    if not (a.search or a.type or a.theme or a.dossier):
        print(__doc__)
        return 2
    hits = sorted((r for r in rows if matches(r, a)), key=lambda r: safe_str(r.get("ID")), reverse=True)
    for r in hits[: a.limit]:
        print(r["ID"], r["Type"], r["Theme"], r["Statut"], safe_str(r.get("URL_WordPress")) or "—", safe_str(r.get("Titre"))[:100])
    if len(hits) > a.limit:
        print(f"… {len(hits) - a.limit} autres (--limit)")
    return 0 if hits else 1


if __name__ == "__main__":
    raise SystemExit(main())
