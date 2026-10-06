#!/usr/bin/env python3
"""Print ID, Statut, URL_WordPress and Slug_WordPress of index_editorial.csv rows.

Usage: python tools/index_lookup.py 2026-555 2026-556
"""

from __future__ import annotations

import sys
from pathlib import Path

from index_editorial_utils import read_index, safe_str

INDEX_PATH = Path(__file__).resolve().parent.parent / "index_editorial.csv"


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ids = set(sys.argv[1:])
    if not ids:
        print(__doc__)
        return 2
    found = set()
    _, rows = read_index(INDEX_PATH)
    for row in rows:
        row_id = safe_str(row.get("ID"))
        if row_id in ids:
            found.add(row_id)
            print(row_id, safe_str(row.get("Statut")), safe_str(row.get("URL_WordPress")), safe_str(row.get("Slug_WordPress")))
    for missing in sorted(ids - found):
        print(missing, "absent de l'index")
    return 0 if found == ids else 1


if __name__ == "__main__":
    raise SystemExit(main())
