"""Génère 00_Systeme/Etat_editorial_courant.md : la vue courte lue par la routine quotidienne.

Usage : python tools/build_etat_courant.py

Sources : mémoire éditoriale §1 (10 derniers articles), §2 (fils actifs), §3 (dernier
Fil du Phare), §4 (cap du mois) ; Radar éditorial (questions et candidats prioritaires).
Lecture seule sur les sources ; 50 lignes au plus.
"""
from __future__ import annotations

import datetime as dt
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MEMOIRE = ROOT / "00_Systeme" / "Memoire_editoriale.md"
RADAR = ROOT / "00_Systeme" / "Radar_editorial.md"
OUT = ROOT / "00_Systeme" / "Etat_editorial_courant.md"
MAX_LINES = 50

STATUT_ORDER = ("à échéance", "approfondir", "relier", "conserver")
CAP_KEYS = ("Mois", "Dossiers prioritaires", "Actualités à surveiller", "Catégories sous-représentées")


def cut(s: str, n: int) -> str:
    s = " ".join((s or "").split())
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


def unlink(s: str) -> str:
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s).replace("**", "")


def section(lines: list[str], prefix: str) -> list[str]:
    start = next((i for i, l in enumerate(lines) if l.startswith(prefix)), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    return lines[start + 1 : end]


def table_rows(lines: list[str]) -> list[list[str]]:
    rows = []
    for l in lines:
        if not l.startswith("|") or re.fullmatch(r"\|[\s\-|:]+\|?", l.strip()):
            continue
        rows.append([c.strip() for c in l.strip().strip("|").split("|")])
    return rows[1:] if rows else []


def derniers(mem: list[str]) -> list[str]:
    rows = [r for r in table_rows(section(mem, "## 1.")) if len(r) >= 11 and re.fullmatch(r"\d{4}-\d{3}", r[1])]
    out = []
    for r in rows[-10:][::-1]:
        date, aid, titre, typ, cat, question, _, penseur = r[:8]
        m = re.match(r"\[(.+)\]\((.+)\)$", titre)
        titre = f"[{cut(m.group(1), 90)}]({m.group(2)})" if m else cut(titre, 90)
        line = f"- {aid} · {date[5:]} · {typ} · {cat.split('/')[-1].strip()} — {titre}"
        if question not in ("", "—") and typ != "Question":
            line += f" · Q : {cut(question, 130)}"
        if penseur not in ("", "—"):
            line += f" · {cut(unlink(penseur), 60)}"
        out.append(line)
    return out


def fils(mem: list[str]) -> list[str]:
    sec = section(mem, "## 2.")
    start = next((i for i, l in enumerate(sec) if l.startswith("### Fils actifs")), None)
    if start is None:
        return []
    end = next((i for i in range(start + 1, len(sec)) if sec[i].startswith("### ")), len(sec))
    return [f"- {cut(r[0], 90)} ({r[2]}) → {cut(r[3], 140)}" for r in table_rows(sec[start:end])[:5] if len(r) >= 4]


def dernier_fil(mem: list[str]) -> str:
    for r in table_rows(section(mem, "## 3.")):
        if len(r) >= 3 and r[2] not in ("", "—"):
            return f"- **Dernier Fil du Phare** : {r[2]} — {cut(r[1], 120)}"
    return "- **Dernier Fil du Phare** : —"


def cap(mem: list[str]) -> list[str]:
    out = []
    for l in section(mem, "## 4."):
        m = re.match(r"- \*\*(.+?) ?(\(.*?\))? ?:\*\* ?(.*)", l)
        if m and any(m.group(1).startswith(k) for k in CAP_KEYS):
            out.append(f"- **{m.group(1)}** : {cut(unlink(m.group(3)), 320)}")
    return out


def radar() -> tuple[list[str], list[str]]:
    lines = RADAR.read_text(encoding="utf-8").splitlines()
    questions, candidats = [], []
    block = ""
    for i, l in enumerate(lines):
        if l.startswith("## "):
            block = l
            continue
        if block.startswith("## Archives") or not l.startswith("| P"):
            continue
        r = [c.strip() for c in l.strip().strip("|").split("|")]
        if len(r) < 5 or not re.fullmatch(r"P[123]", r[0]):
            continue
        rank = (r[0], next((k for k, s in enumerate(STATUT_ORDER) if r[4].startswith(s)), 9), i)
        if r[1] == "Question":
            questions.append((rank, f"- {r[0]} · {cut(r[2], 170)} — {cut(r[3], 50)}"))
        elif r[1] not in ("Dossier", "Atelier"):
            candidats.append((rank, f"- {r[0]} · {r[1]} · {cut(r[2], 130)} — {cut(r[3], 50)} · {r[4]}"))
    return [t for _, t in sorted(questions)[:5]], [t for _, t in sorted(candidats)[:5]]


def main() -> None:
    mem = MEMOIRE.read_text(encoding="utf-8").splitlines()
    questions, candidats = radar()
    L = [
        "# État éditorial courant — Le Phare",
        "",
        f"*Généré par `tools/build_etat_courant.py` le {dt.date.today().isoformat()} — ne pas éditer. "
        "Sources : `Memoire_editoriale.md` §1–§4, `Radar_editorial.md`.*",
        "",
        "## Derniers articles",
        "",
        *derniers(mem),
        "",
        "## Fils actifs",
        "",
        *fils(mem),
        "",
        "## Questions prioritaires (Radar)",
        "",
        *(questions or ["- aucune"]),
        "",
        "## Prochains candidats (Radar)",
        "",
        *(candidats or ["- aucun"]),
        "",
        "## Cap du mois",
        "",
        *cap(mem),
        dernier_fil(mem),
    ]
    OUT.write_bytes(("\n".join(L) + "\n").encode("utf-8"))
    status = "OK" if len(L) <= MAX_LINES else "ATTENTION"
    print(f"{status}: {OUT.relative_to(ROOT).as_posix()} ({len(L)} lignes, max {MAX_LINES})")


if __name__ == "__main__":
    main()
