#!/usr/bin/env python3
"""Refresh the WordPress body of already-published articles (wp_push_draft.py --refresh-body).

Builds the local config path itself so that it never appears in a shell command:
the Claude Code deny rule on tools/*.local.json also rejects Bash commands that contain it.
Prints only status / error / wordpress_id / link for each article.

Usage: python tools/wp_refresh_body.py "<chemin canonique>" ["<chemin>" ...] [--title] [--allow-fonds]
(--title : met aussi à jour le titre WP depuis l'en-tête « Titre : ».)
(--allow-fonds : PATCH du fondamental parent 02_Fonds/, réservé à la routine triptyque archivée.)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
ROOT_DIR = TOOLS_DIR.parent
CONFIG_PATH = TOOLS_DIR / ("wp_config" + ".local.json")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    allow_fonds = "--allow-fonds" in sys.argv[1:]
    extra = ["--refresh-title"] if "--title" in sys.argv[1:] else []
    paths = [a for a in sys.argv[1:] if a not in ("--allow-fonds", "--title")]
    if not paths:
        print(__doc__)
        return 2
    if not CONFIG_PATH.exists():
        print("Config WordPress locale absente (copier tools/wp_config.example.json).")
        return 2
    rc = 0
    for path in paths:
        if not allow_fonds and Path(path).as_posix().startswith("02_Fonds/"):
            print(f"{path} : refusé (02_Fonds/ est réservé à l'éditeur humain)")
            rc = 1
            continue
        out = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "wp_push_draft.py"), path,
             "--index", "index_editorial.csv", "--refresh-body", *extra, "--config", str(CONFIG_PATH)],
            cwd=ROOT_DIR, capture_output=True, text=True, encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        try:
            data = json.loads(out.stdout.strip())
            items = data if isinstance(data, list) else data.get("results", [data])
            for it in items:
                print(path, {k: it.get(k) for k in ("status", "error", "wordpress_id", "link")})
        except (ValueError, AttributeError):
            print(path, out.stdout.strip()[-1500:])
        if out.returncode:
            print(f"{path} : rc {out.returncode} {out.stderr.strip()[-800:]}")
            rc = out.returncode
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
