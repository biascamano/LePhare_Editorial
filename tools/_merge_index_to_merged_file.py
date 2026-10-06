#!/usr/bin/env python3
"""Merge fragment into index; write index_editorial.merged.csv (does not touch locked index)."""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index_editorial.csv"
FRAGMENT = ROOT / "00_Systeme/index_APPEND_triptyque_science_sante_2026-05-06.csv"
OUT = ROOT / "index_editorial.merged.csv"


def main() -> int:
    if not FRAGMENT.is_file():
        print(f"Missing {FRAGMENT}", file=sys.stderr)
        return 1

    with INDEX.open("r", encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        existing = list(reader)

    ids_existing = {row.get("ID", "").strip() for row in existing}

    with FRAGMENT.open("r", encoding="utf-8-sig", newline="") as fh:
        new_rows = list(csv.DictReader(fh))

    appended = 0
    for row in new_rows:
        aid = row.get("ID", "").strip()
        if not aid or aid in ids_existing:
            continue
        existing.append({fn: row.get(fn, "") for fn in fieldnames})
        ids_existing.add(aid)
        appended += 1

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)

    print(f"Wrote {OUT} ({len(existing)} rows, +{appended} from fragment). Replace index when unlocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
