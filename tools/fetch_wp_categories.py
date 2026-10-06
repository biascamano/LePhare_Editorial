#!/usr/bin/env python3
"""Fetch all WordPress categories from the public REST API (no auth)."""
from __future__ import annotations

import argparse
import csv
import json
import sys
import urllib.request
from html import unescape


def fetch_all_categories(site_url: str) -> list[dict]:
    base = site_url.rstrip("/") + "/wp-json/wp/v2/categories"
    out: list[dict] = []
    page = 1
    headers = {"User-Agent": "LePhareEditorial-fetch_wp_categories/1"}
    while True:
        url = f"{base}?per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            batch = json.loads(response.read().decode("utf-8"))
        if not batch:
            break
        out.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return out


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="List WordPress categories via REST API.")
    parser.add_argument(
        "--site-url",
        default="https://le-phare.info",
        help="WordPress site root URL",
    )
    parser.add_argument(
        "--json-out",
        metavar="FILE",
        help="Write full JSON array to this path",
    )
    parser.add_argument(
        "--csv-out",
        metavar="FILE",
        help="Write id,count,parent,slug,name to CSV",
    )
    args = parser.parse_args()
    try:
        cats = fetch_all_categories(args.site_url)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    cats.sort(key=lambda c: int(c.get("id", 0)))
    print(f"total_categories\t{len(cats)}")
    for c in cats:
        pid = int(c.get("parent") or 0)
        print(f"{c['id']}\t{c.get('count', 0)}\t{pid}\t{c.get('slug', '')}\t{unescape(c.get('name', '') or '')}")
    if args.json_out:
        Path = __import__("pathlib").Path
        Path(args.json_out).write_text(json.dumps(cats, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.csv_out:
        Path = __import__("pathlib").Path
        with Path(args.csv_out).open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["id", "count", "parent", "slug", "name"])
            for c in cats:
                w.writerow(
                    [
                        c["id"],
                        c.get("count", 0),
                        int(c.get("parent") or 0),
                        c.get("slug", ""),
                        unescape(c.get("name", "") or ""),
                    ]
                )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
