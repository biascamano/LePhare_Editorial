"""Ajoute la ligne d'un article au §1 (journal) de 00_Systeme/Memoire_editoriale.md.

Usage : python tools/memoire_append.py <ID> [--penseur "…"] [--type-label "…"] [--sentier <ID fondamental>] [--date YYYY-MM-DD] [--dry-run]

Sources : en-tête de l'article (question, dossier, article précédent, prolongement,
fondamental lié), index (titre, URL, catégorie, thème), manifeste Sentier (étape).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from index_editorial_utils import read_index, safe_str  # noqa: E402

INDEX = ROOT / "index_editorial.csv"
MANIFEST = ROOT / "00_Systeme" / "Manifests" / "sentier_fondamentaux.csv"
MEMOIRE = ROOT / "00_Systeme" / "Memoire_editoriale.md"

TYPE_LABELS = {
    "Actualite": "Actualité",
    "Question": "Question",
    "Application": "Application",
    "Texte fondateur": "Texte fondateur",
    "Fil du Phare": "Fil du Phare",
    "Synthese mensuelle": "Synthèse mensuelle",
    "Dossier": "Dossier (mensuelle)",
    "Atelier Sentier": "Atelier Sentier (mensuelle)",
}


def cell(s: str) -> str:
    s = " ".join((s or "").split()).replace("|", "/")
    return s or "—"


def header(text: str) -> dict[str, str]:
    head = text.split("\n---", 1)[0]
    out = {}
    for line in head.splitlines():
        if " : " in line:
            k, v = line.split(" : ", 1)
            out[k.strip()] = v.strip()
        elif line.rstrip().endswith(" :"):
            out[line.rstrip()[:-2].strip()] = ""
    return out


def sentier(fond_id: str) -> str:
    if not fond_id:
        return "—"
    for m in csv.DictReader(open(MANIFEST, encoding="utf-8-sig")):
        if m["fondamental_id"] == fond_id:
            label = f"Etape {int(m['etape_num']):02d} — {m['titre']}"
            return f"[{label}]({m['url_canonique']}) ({fond_id})" if m["url_canonique"] else f"{label} ({fond_id})"
    return f"— ({fond_id} absent du manifeste)"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("id")
    ap.add_argument("--penseur", default="")
    ap.add_argument("--type-label", default="")
    ap.add_argument("--sentier", default="", help="ID du fondamental (sinon en-tête « Fondamental lie (ID) »)")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--dry-run", action="store_true", help="affiche la ligne sans écrire")
    a = ap.parse_args()

    _, rows = read_index(INDEX)
    row = next((r for r in rows if safe_str(r.get("ID")) == a.id), None)
    if row is None:
        raise SystemExit(f"KO: {a.id} absent de l'index")
    path = ROOT / row["Chemin_dossier"] / row["Nom_fichier"]
    if not path.exists():
        raise SystemExit(f"KO: fichier introuvable {path.relative_to(ROOT)}")
    h = header(path.read_text(encoding="utf-8"))

    text = MEMOIRE.read_text(encoding="utf-8")
    lines = text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("## 1."))
    end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
    table = [i for i in range(start, end) if lines[i].startswith("|")]
    if not table:
        raise SystemExit("KO: tableau du §1 introuvable")
    if any(f"| {a.id} |" in lines[i] for i in table) and not a.dry_run:
        raise SystemExit(f"KO: {a.id} déjà présent au §1")

    title = cell(row["Titre"])
    url = safe_str(row.get("URL_WordPress"))
    type_label = a.type_label or TYPE_LABELS.get(h.get("Type article", ""), h.get("Type article", "") or row["Type"])
    categorie = f"{safe_str(row.get('Categorie_WP')).lower() or '—'} / {row['Theme']}"
    fields = [
        a.date,
        a.id,
        f"[{title}]({url})" if url else title,
        type_label,
        categorie,
        cell(h.get("Question du Phare", "")),
        cell(h.get("Dossier", "")),
        cell(a.penseur),
        sentier(a.sentier or h.get("Fondamental lie (ID)", "")) if (a.sentier or h.get("Fondamental lie (ID)")) else cell(h.get("Etape du Sentier liee", "")),
        cell(h.get("Article precedent (ID)", "")),
        cell(h.get("Prolongement envisage", "")),
    ]
    new_line = "| " + " | ".join(fields) + " |"
    if a.dry_run:
        print(new_line)
        return
    lines.insert(table[-1] + 1, new_line)
    MEMOIRE.write_bytes("\n".join(lines).encode("utf-8"))
    print(f"OK: {a.id} ajouté au §1 ({type_label}{'' if url else ', sans URL WordPress'})")


if __name__ == "__main__":
    main()
