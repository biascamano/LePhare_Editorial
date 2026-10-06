#!/usr/bin/env python3
"""Merge fragment rows into index_editorial.csv (in-place or alternate output path)."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index_editorial.csv"
FRAGMENT = ROOT / "00_Systeme/index_APPEND_triptyque_science_sante_2026-05-06.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append science triptyque rows from fragment CSV into index.")
    parser.add_argument(
        "--out",
        type=Path,
        metavar="PATH",
        help="Write merged CSV here instead of modifying index_editorial.csv (use when index file is locked).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
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

    from index_editorial_utils import append_rows_to_index, normalize_row, safe_str

    to_append: list[dict[str, str]] = []
    for row in new_rows:
        aid = safe_str(row.get("ID"))
        if not aid or aid in ids_existing:
            continue
        to_append.append(normalize_row(row, fieldnames))
        ids_existing.add(aid)

    if to_append and args.out is None:
        appended = append_rows_to_index(INDEX, to_append)
        print(f"Updated {INDEX}: +{appended} rows via index_editorial_utils.")
        return 0

    appended = len(to_append)
    for row in to_append:
        existing.append(row)

    if args.out:
        target = args.out.expanduser()
        if not target.is_absolute():
            target = ROOT / target
    else:
        target = INDEX

    if appended == 0 and args.out is None:
        print("Nothing to append.")
        return 0

    with target.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing)

    if args.out:
        print(f"Wrote merged index ({len(existing)} data rows, +{appended} from fragment) -> {target}")
    else:
        print(f"Updated {target}: +{appended} rows ({len(existing)} total data rows).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
