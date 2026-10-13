#!/usr/bin/env python3
"""Outils de l'atelier du livre (import, mesures, export).

    python tools/livre.py import "<livre>/V3/<complet>.docx" "<livre>/atelier/manuscrit"
    python tools/livre.py stats "<livre>/atelier/manuscrit" [--out "<livre>/atelier/mesures/vN.md"]
    python tools/livre.py export "<livre>/atelier/manuscrit" "<livre>/V4/<titre> — V4 complet.docx" --title "<titre>"
    python tools/livre.py snapshot "<livre>/atelier/manuscrit" "<livre>/atelier/versions/v4"

Le manuscrit de travail est un dossier de fichiers Markdown, un par chapitre, triés par nom
(000_prologue.md, 001_le-merle.md…). Les .docx ne sont jamais modifiés : import les lit, export en crée un nouveau.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

DEFAULT_PANDOC = Path("D:/Logiciel/pandoc-3.9.0.2-windows-x86_64/pandoc-3.9.0.2/pandoc.exe")
CHAPTER_RE = re.compile(r"^# (PROLOGUE|ÉPILOGUE|EPILOGUE|Chapitre\s+\d+)\s*$", re.IGNORECASE)
WORD_RE = re.compile(r"[\wÀ-ÿ’'-]+", re.UNICODE)
SHORT_PARAGRAPH = 6
WORDS_PER_PAGE = 250


def pandoc() -> str:
    exe = os.environ.get("PANDOC") or shutil.which("pandoc")
    if exe:
        return exe
    if DEFAULT_PANDOC.is_file():
        return str(DEFAULT_PANDOC)
    sys.exit("pandoc introuvable (variable PANDOC, PATH ou " + str(DEFAULT_PANDOC) + ")")


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:50] or "sans-titre"


def chapter_files(folder: Path) -> list[Path]:
    return sorted(p for p in folder.glob("*.md") if p.is_file())


def cmd_import(a: argparse.Namespace) -> int:
    src, dest = Path(a.docx), Path(a.dest)
    if dest.exists() and any(dest.glob("*.md")) and not a.force:
        sys.exit(f"{dest} contient déjà des chapitres (--force pour écraser)")
    dest.mkdir(parents=True, exist_ok=True)
    md = subprocess.run([pandoc(), str(src), "-t", "gfm", "--wrap=none"], capture_output=True, check=True).stdout.decode("utf-8")

    chunks: list[list[str]] = []
    pending: list[str] = []
    for line in md.splitlines():
        if CHAPTER_RE.match(line):
            chunks.append(pending + [line])
            pending = []
        elif line.startswith("# ") and chunks:
            pending.append(line)
            pending.append("")
        elif chunks:
            (pending if pending else chunks[-1]).append(line)
        else:
            pending.append(line)

    for i, chunk in enumerate(chunks):
        title = next((l[3:].strip() for l in chunk if l.startswith("## ")), "")
        head = next(l for l in chunk if CHAPTER_RE.match(l))[2:].strip()
        name = f"{i:03d}_{slugify(title or head)}.md"
        (dest / name).write_text("\n".join(chunk).strip() + "\n", encoding="utf-8")
    print(f"{len(chunks)} chapitres écrits dans {dest}")
    return 0


def paragraphs(text: str) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text)]
    return [b for b in blocks if b and not b.startswith("#")]


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def cmd_stats(a: argparse.Namespace) -> int:
    files = chapter_files(Path(a.manuscrit))
    if not files:
        sys.exit("aucun chapitre")
    rows = []
    ngram_chapters: dict[tuple[str, ...], set[int]] = defaultdict(set)
    total_words = total_par = total_short = ends_q = 0
    for idx, f in enumerate(files):
        text = f.read_text(encoding="utf-8")
        pars = paragraphs(text)
        w = words(text)
        short = [len(words(p)) <= SHORT_PARAGRAPH for p in pars]
        run = best = 0
        for s in short:
            run = run + 1 if s else 0
            best = max(best, run)
        last = pars[-1] if pars else ""
        q = last.rstrip(" *_»").endswith("?")
        ends_q += q
        total_words += len(w)
        total_par += len(pars)
        total_short += sum(short)
        for i in range(len(w) - 3):
            ngram_chapters[tuple(w[i:i + 4])].add(idx)
        rows.append((f.stem, len(w), len(pars), 100 * sum(short) // max(len(pars), 1), best, "oui" if q else ""))

    out = [f"# Mesures — {Path(a.manuscrit)}", ""]
    out.append(f"- Chapitres : {len(files)}")
    out.append(f"- Mots : {total_words} (≈ {total_words // WORDS_PER_PAGE} pages à {WORDS_PER_PAGE} mots ; davantage en style très aéré)")
    out.append(f"- Paragraphes courts (≤ {SHORT_PARAGRAPH} mots) : {100 * total_short // max(total_par, 1)} %")
    out.append(f"- Chapitres finissant sur une question : {ends_q} / {len(files)}")
    out.append("")
    out.append("## Formules récurrentes (4 mots, présentes dans au moins 5 chapitres)")
    out.append("")
    recurrent = sorted(((len(c), " ".join(g)) for g, c in ngram_chapters.items() if len(c) >= 5), reverse=True)
    for n, g in recurrent[: a.top]:
        out.append(f"- « {g} » : {n} chapitres")
    if not recurrent:
        out.append("- aucune")
    out.append("")
    out.append("## Par chapitre")
    out.append("")
    out.append("| Fichier | Mots | Paragraphes | % courts | Plus longue suite de courts | Finit sur ? |")
    out.append("|---|---:|---:|---:|---:|---|")
    out.extend(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} | {r[5]} |" for r in rows)
    report = "\n".join(out) + "\n"
    if a.out:
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(report, encoding="utf-8")
        print(f"Mesures écrites dans {a.out}")
        print("\n".join(out[2:6]))
    else:
        sys.stdout.write(report)
    return 0


def cmd_export(a: argparse.Namespace) -> int:
    files = chapter_files(Path(a.manuscrit))
    if not files:
        sys.exit("aucun chapitre")
    out = Path(a.out)
    if out.exists() and not a.force:
        sys.exit(f"{out} existe déjà (--force pour écraser)")
    out.parent.mkdir(parents=True, exist_ok=True)
    cmd = [pandoc(), *map(str, files), "-f", "markdown", "-t", "docx", "-o", str(out), "--metadata", f"title={a.title}"]
    if a.toc:
        cmd.append("--toc")
    if a.reference:
        cmd += ["--reference-doc", a.reference]
    subprocess.run(cmd, check=True)
    print(f"Export : {out}")
    return 0


def cmd_snapshot(a: argparse.Namespace) -> int:
    src, dest = Path(a.manuscrit), Path(a.dest)
    if dest.exists():
        sys.exit(f"{dest} existe déjà : une version figée ne se réécrit pas")
    shutil.copytree(src, dest)
    print(f"Version figée : {dest} ({len(chapter_files(dest))} chapitres)")
    return 0


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(usage=__doc__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("import")
    p.add_argument("docx")
    p.add_argument("dest")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("stats")
    p.add_argument("manuscrit")
    p.add_argument("--out")
    p.add_argument("--top", type=int, default=15)
    p = sub.add_parser("export")
    p.add_argument("manuscrit")
    p.add_argument("out")
    p.add_argument("--title", required=True)
    p.add_argument("--reference")
    p.add_argument("--toc", action="store_true")
    p.add_argument("--force", action="store_true")
    p = sub.add_parser("snapshot")
    p.add_argument("manuscrit")
    p.add_argument("dest")
    a = ap.parse_args()
    return {"import": cmd_import, "stats": cmd_stats, "export": cmd_export, "snapshot": cmd_snapshot}[a.cmd](a)


if __name__ == "__main__":
    raise SystemExit(main())
