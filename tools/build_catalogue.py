"""Génère 00_Systeme/Catalogue_editorial.md à partir de l'index (lecture seule).

Usage : python tools/build_catalogue.py
"""
from __future__ import annotations

import collections
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "index_editorial.csv"
MANIFEST = ROOT / "00_Systeme" / "Manifests" / "sentier_fondamentaux.csv"
MEMOIRE = ROOT / "00_Systeme" / "Memoire_editoriale.md"
OUT = ROOT / "00_Systeme" / "Catalogue_editorial.md"
SCAN_DIRS = ("01_Actualites", "03_Dossiers", "04_Textes_fondateurs", "05_Sentier", "06_Syntheses")

# Repères du socle (plan.md §5.8) et penseurs déjà mobilisés dans la mémoire.
PENSEURS = (
    "Simone Weil", "Hannah Arendt", "Jacques Ellul", "Albert Camus", "Hartmut Rosa",
    "Tocqueville", "Ivan Illich", "David Collingridge", "John Ruskin", "Thomas Schelling",
    "Pierre Bourdieu", "Bruno Latour", "Hans Jonas", "Donald T. Campbell",
)

LEVELS = (
    ("Actualités", lambda r: r["Type"] == "ACTU" and "type-question" not in r["Tags_WP"]),
    ("Questions du Phare", lambda r: r["Type"] == "ACTU" and "type-question" in r["Tags_WP"]),
    ("Textes fondateurs", lambda r: r["Type"] == "TF"),
    ("Synthèses et briefings", lambda r: r["Type"] in ("SYNTHESE", "BRIEFING")),
    ("Dossiers", lambda r: r["Type"] == "DOSSIER"),
    ("Sentier — ateliers et pages", lambda r: r["Type"] == "SENTIER"),
    ("Fonds — fondamentaux et notions", lambda r: r["Type"] == "FOND"),
)


def cell(s: str, n: int | None = None) -> str:
    s = " ".join((s or "").split()).replace("|", "/")
    return s if n is None or len(s) <= n else s[: n - 1].rstrip() + "…"


def link(r: dict) -> str:
    t = cell(r["Titre"], 110)
    return f"[{t}]({r['URL_WordPress']})" if r["URL_WordPress"] else t


def fond_usage(rows: list[dict]) -> collections.Counter:
    by_file = {r["Nom_fichier"]: r["ID"] for r in rows if r["Nom_fichier"]}
    use: collections.Counter = collections.Counter()
    pat = re.compile(r"^Fondamental lie \(ID\) : (2026-\d{3})", re.M)
    for d in SCAN_DIRS:
        for p in (ROOT / d).rglob("*.md"):
            if p.name not in by_file:
                continue
            m = pat.search(p.read_text(encoding="utf-8", errors="replace"))
            if m:
                use[m.group(1)] += 1
    return use


def prolongements() -> list[tuple[str, str]]:
    out = []
    for l in MEMOIRE.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in l.split("|")]
        if len(c) >= 12 and re.fullmatch(r"2026-\d{3}", c[2]) and c[11] not in ("", "—"):
            out.append((c[2], c[11]))
    return out


def main() -> None:
    rows = list(csv.DictReader(open(INDEX, encoding="utf-8-sig")))
    manifest = list(csv.DictReader(open(MANIFEST, encoding="utf-8-sig")))
    use = fond_usage(rows)
    tf_titles = [r["Titre"].lower() for r in rows if r["Type"] == "TF"]

    L = [
        "# Catalogue éditorial — Le Phare Info",
        "",
        "*Généré par `tools/build_catalogue.py` depuis `index_editorial.csv` — ne pas éditer à la main.*",
        "*Liste priorisée des articles à créer : `00_Systeme/Articles_a_creer.md`.*",
        "",
        "## Vue d'ensemble",
        "",
        f"- Articles indexés : {len(rows)}",
        f"- Publiés : {sum(r['Statut'] == 'publie' for r in rows)} ; brouillons WordPress : {sum(r['Statut'] == 'wp_draft' for r in rows)}",
        "",
        "| Niveau | Articles |",
        "|---|---|",
    ]
    groups = [(name, [r for r in rows if f(r)]) for name, f in LEVELS]
    L += [f"| {n} | {len(g)} |" for n, g in groups]
    L += ["", "| Thème | Total | Depuis 2026-05 |", "|---|---|---|"]
    tot = collections.Counter(r["Theme"] for r in rows)
    rec = collections.Counter(r["Theme"] for r in rows if r["Date_creation"] >= "2026-05")
    L += [f"| {t} | {n} | {rec[t]} |" for t, n in tot.most_common()]

    L += ["", "## Lacunes détectées", "", "### Penseurs du socle sans texte fondateur", ""]
    L += [f"- {p}" for p in PENSEURS if p.split()[-1].lower() not in " ".join(tf_titles)] or ["- aucun"]

    L += ["", "### Fondamentaux du Sentier sans article rattaché", "",
          "*Rattachement = en-tête « Fondamental lie (ID) » d'une actualité, question, TF ou atelier.*", ""]
    by_step: dict[str, list[str]] = collections.defaultdict(list)
    for m in manifest:
        if m["fondamental_num"] != "0" and use[m["fondamental_id"]] == 0:
            by_step[f"Étape {m['etape_num']} — {m['etape_nom']}"].append(f"{m['fondamental_id']} {cell(m['titre'], 80)}")
    for step, items in by_step.items():
        L.append(f"- **{step}** ({len(items)}) : " + " ; ".join(items))

    L += ["", "### Prolongements envisagés (mémoire §1)", ""]
    L += [f"- {i} — {cell(p, 220)}" for i, p in prolongements()] or ["- aucun"]

    L += ["", "## Sentier — rattachements par fondamental", "", "| Étape | ID | Fondamental | Articles rattachés |", "|---|---|---|---|"]
    for m in manifest:
        if m["fondamental_num"] == "0":
            continue
        t = f"[{cell(m['titre'], 80)}]({m['url_canonique']})" if m["url_canonique"] else cell(m["titre"], 80)
        L.append(f"| {m['etape_num']} | {m['fondamental_id']} | {t} | {use[m['fondamental_id']] or '—'} |")

    for name, g in groups:
        L += ["", f"## {name} ({len(g)})", "", "| ID | Titre | Thème | Statut | Date | Résumé |", "|---|---|---|---|---|---|"]
        for r in sorted(g, key=lambda r: r["ID"], reverse=True):
            L.append(f"| {r['ID']} | {link(r)} | {r['Theme']} | {r['Statut']} | {r['Date_creation']} | {cell(r['Resume_court'] or r['Objectif'], 200)} |")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"OK: {OUT.relative_to(ROOT)} ({len(rows)} articles)")


if __name__ == "__main__":
    main()
