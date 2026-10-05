from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from index_editorial_utils import append_rows_to_index, build_index_row, read_index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SENTIER_CSV = Path("00_Systeme") / "Manifests" / "sentier_fondamentaux.csv"
STAGING_DIR = Path("07_A_Publier")
MAX_TAGS = 8

THEMES = {
    "MONDE": ("Politique_Societe", "monde"),
    "POL": ("Politique_Societe", "politique-societe"),
    "ECON": ("Economie_Finance", "economie-finance"),
    "TECH": ("Technologie_IA", "technologie-ia"),
    "CLIMAT": ("Climat_Transition", "environnement-climat"),
    "SCIENCE": ("Science_Sante", "science-sante"),
    "CULTURE": ("Culture", "culture-philosophie"),
}

PILLARS = ("culture", "critique", "approfondissement", "langues", "science", "transmission", "vision", "equilibre")
POSTURES = ("Observer", "Comprendre", "Distance", "Relier", "Transmettre")

TYPES: dict[str, dict] = {
    "actualite": {"code": "ACTU", "label": "Actualite", "category": "actualites", "tags": ["type-actualite"], "posture": "Observer", "routine": "quotidienne"},
    "question": {"code": "ACTU", "label": "Question", "category": "actualites", "tags": ["type-question"], "posture": "Comprendre", "routine": "quotidienne"},
    "application": {"code": "ACTU", "label": "Application", "category": "actualites", "tags": ["type-application"], "posture": "Relier", "routine": "quotidienne"},
    "texte-fondateur": {"code": "TF", "label": "Texte fondateur", "category": "textes-fondateurs", "tags": ["type-texte-fondateur"], "posture": "Comprendre", "routine": "mensuelle"},
    "fil-du-phare": {"code": "SYNTHESE", "label": "Fil du Phare", "category": "cycle", "tags": ["fil-du-phare", "question-du-phare", "synthese-hebdomadaire"], "posture": "Relier", "routine": "hebdomadaire"},
    "synthese-mensuelle": {"code": "SYNTHESE", "label": "Synthese mensuelle", "category": "cycle", "tags": ["synthese-mensuelle", "question-du-phare"], "posture": "Relier", "routine": "mensuelle"},
    "dossier": {"code": "DOSSIER", "label": "Dossier", "category": "dossier-hebdomadaire", "tags": [], "posture": "Relier", "routine": "mensuelle"},
    "atelier": {"code": "SENTIER", "label": "Atelier Sentier", "category": "sentier-du-savoir", "tags": ["atelier-sentier"], "posture": "Transmettre", "routine": "mensuelle"},
}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ID_RE = re.compile(r"^(\d{4})-(\d{3,})$")


def slugify(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii").lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")


def split_list(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def next_article_id(rows: list[dict[str, str]], year: int) -> str:
    highest = 0
    for row in rows:
        match = ID_RE.match((row.get("ID") or "").strip())
        if match and int(match.group(1)) == year:
            highest = max(highest, int(match.group(2)))
    return f"{year}-{highest + 1:03d}"


def load_fondamental(fondamental_id: str) -> dict[str, str]:
    with (ROOT / SENTIER_CSV).open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    target = next((r for r in rows if r["fondamental_id"] == fondamental_id and r["fondamental_num"] != "0"), None)
    if target is None:
        raise SystemExit(f"Fondamental inconnu dans {SENTIER_CSV.name} : {fondamental_id}")
    return target


def resolve_location(args: argparse.Namespace, spec: dict) -> tuple[str, dict[str, str] | None]:
    theme_dir = THEMES[args.theme][0]
    if args.type in ("actualite", "question", "application"):
        return f"01_Actualites/{theme_dir}", None
    if args.type == "texte-fondateur":
        return "04_Textes_fondateurs/Auteurs", None
    if args.type == "fil-du-phare":
        return "06_Syntheses/Fil_du_Phare", None
    if args.type == "synthese-mensuelle":
        return "06_Syntheses/Mensuelles", None
    if args.type == "dossier":
        if not args.dossier_dir:
            raise SystemExit("--dossier-dir est obligatoire pour un dossier")
        return f"03_Dossiers/{theme_dir}/{args.dossier_dir}", None
    if not args.fondamental_id:
        raise SystemExit("--fondamental-id est obligatoire pour un atelier")
    target = load_fondamental(args.fondamental_id)
    folders = sorted((ROOT / "05_Sentier").glob(f"Etape_{int(target['etape_num']):02d}_*"))
    if len(folders) != 1:
        raise SystemExit(f"Dossier d'étape introuvable ou ambigu pour l'étape {target['etape_num']}")
    return f"05_Sentier/{folders[0].name}", target


def build_tags(args: argparse.Namespace, spec: dict, posture: str, fondamental: dict[str, str] | None) -> list[str]:
    tags = [THEMES[args.theme][1]]
    if args.pillar:
        tags.append(f"sentier-{args.pillar}")
    tags.append(f"posture-{posture.lower()}")
    tags.extend(spec["tags"])
    if (args.routine or spec["routine"]) == "quotidienne":
        tags.append("question-du-phare")
    if fondamental:
        tags.append(f"fondamental-{fondamental['fondamental_id']}")
    tags.extend(split_list(args.tags))
    unique = list(dict.fromkeys(tags))
    if len(unique) > MAX_TAGS:
        raise SystemExit(f"{len(unique)} tags > {MAX_TAGS} : {';'.join(unique)}")
    return unique


def render_skeleton(meta: list[tuple[str, str]], title: str, slug: str, keyword: str) -> str:
    header = "\n".join(f"{key} : {value}".rstrip() for key, value in meta)
    return f"""{header}

---

# {title}

[Corps de l'article à rédiger]

---

**Repères de sources**

- Source : [libellé](url)

**La question suivante**

[Question du Phare, une phrase]

**Pour aller plus loin**

- [Titre](url)

**Sur le Sentier du Savoir**

- [Fondamental ou atelier](url)

# SEO

Mot-cle principal : {keyword}
Meta description :
Slug propose : {slug}
"""


def cmd_create(args: argparse.Namespace) -> dict:
    spec = TYPES[args.type]
    index_path = Path(args.index)
    _, rows = read_index(index_path)
    creation_date = date.fromisoformat(args.date) if args.date else date.today()

    slug = slugify(args.slug or args.title)
    if not SLUG_RE.match(slug):
        raise SystemExit(f"Slug invalide : {slug!r}")
    wp_slug = f"fil-du-phare-{slug}" if args.type == "fil-du-phare" and not slug.startswith("fil-du-phare-") else slug
    if any((r.get("Slug_WordPress") or "").strip() == wp_slug for r in rows):
        raise SystemExit(f"Slug déjà présent dans l'index : {wp_slug}")

    known_ids = {(r.get("ID") or "").strip() for r in rows}
    linked = split_list(args.linked)
    for ref in [*linked, *([args.previous] if args.previous else [])]:
        if ref not in known_ids:
            raise SystemExit(f"ID lié absent de l'index : {ref}")

    posture = args.posture or spec["posture"]
    relative_folder, fondamental = resolve_location(args, spec)
    tags = build_tags(args, spec, posture, fondamental)

    article_id = next_article_id(rows, creation_date.year)
    filename = f"{article_id}_{spec['code']}_{args.theme}_{wp_slug.replace('-', '_')}_V1.md"
    target = ROOT / relative_folder / filename
    if target.exists():
        raise SystemExit(f"Fichier déjà existant : {target}")

    etape = args.etape or ""
    if fondamental:
        etape = f"Etape {int(fondamental['etape_num']):02d} — {fondamental['etape_nom']}"
    keywords = split_list(args.keywords)

    meta = [
        ("ID article", article_id),
        ("Titre", args.title),
        ("Type", spec["code"]),
        ("Type article", spec["label"]),
        ("Theme", args.theme),
        ("Statut", "brouillon"),
        ("Version", "V1"),
        ("Date de creation", creation_date.isoformat()),
        ("Date de derniere mise a jour", creation_date.isoformat()),
        ("Auteur", "Le Phare Info"),
        ("Etape du Sentier liee", etape),
        ("Fondamental lie (ID)", fondamental["fondamental_id"] if fondamental else ""),
        ("Fondamental numero", fondamental["fondamental_num"] if fondamental else ""),
        ("Type Sentier", "atelier" if fondamental else ""),
        ("Posture Sentier", posture),
        ("Articles lies (IDs)", ";".join(linked)),
        ("Question du Phare", args.question or ""),
        ("Dossier", args.dossier or ""),
        ("Article precedent (ID)", args.previous or ""),
        ("Prolongement envisage", args.prolongement or ""),
        ("Mots-cles", ";".join(keywords)),
        ("Resume court (500 caracteres max)", args.summary or ""),
        ("Objectif de l'article", args.objective or ""),
        ("Sources principales", ""),
        ("URL WordPress (si publie)", ""),
    ]

    routine = args.routine or spec["routine"]
    if routine == "quotidienne":
        remarques = f"Routine quotidienne v3 — type {spec['label'].lower()}"
    elif routine == "hebdomadaire":
        remarques = "Routine hebdomadaire — Fil du Phare"
    else:
        remarques = f"Routine mensuelle — {spec['label'].lower()}"

    row = build_index_row(
        article_id=article_id,
        title=args.title,
        type_code=spec["code"],
        theme_code=args.theme,
        etape_sentier=etape,
        linked_ids=linked,
        keywords=keywords,
        summary=args.summary or "",
        objective=args.objective or "",
        filename=filename,
        relative_folder=relative_folder,
        slug=wp_slug,
        wp_categories=[spec["category"]],
        wp_tags=tags,
        remarques=remarques,
        statut="en_redaction",
    )
    row["Date_creation"] = row["Date_derniere_maj"] = creation_date.isoformat()

    result = {
        "id": article_id,
        "path": str(target.relative_to(ROOT)).replace("\\", "/"),
        "slug": wp_slug,
        "category": spec["category"],
        "tags": tags,
        "dry_run": args.dry_run,
    }
    if args.dry_run:
        return result

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_skeleton(meta, args.title, wp_slug, keywords[0] if keywords else ""), encoding="utf-8", newline="\n")
    append_rows_to_index(index_path, [row])
    return result


def cmd_stage(args: argparse.Namespace) -> dict:
    _, rows = read_index(Path(args.index))
    row = next((r for r in rows if (r.get("ID") or "").strip() == args.id), None)
    if row is None:
        raise SystemExit(f"ID absent de l'index : {args.id}")
    from validate_index_editorial import check_article

    errors = check_article(row, rows, ROOT)
    if errors and not args.force:
        raise SystemExit("Contrôle v3 KO (corriger puis relancer) :\n- " + "\n- ".join(errors))
    source = ROOT / row["Chemin_dossier"] / row["Nom_fichier"]
    stage_date = args.date or date.today().isoformat()
    folder = ROOT / STAGING_DIR / f"{stage_date}_{row['Slug_WordPress']}"
    existing = [p for p in folder.glob("*.md") if p.name != source.name] if folder.exists() else []
    if existing:
        raise SystemExit(f"Le dossier de transit contient déjà un autre .md : {existing[0].name}")
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, folder / source.name)
    return {"id": args.id, "staging": str(folder.relative_to(ROOT)).replace("\\", "/")}


def main() -> None:
    global ROOT
    parser = argparse.ArgumentParser(description="Crée un article rangé (fichier canonique + ligne d'index) ou le copie dans 07_A_Publier.")
    parser.add_argument("--root", default=str(ROOT), help="racine du projet (tests)")
    parser.add_argument("--index", help="défaut <root>/index_editorial.csv")
    sub = parser.add_subparsers(dest="command", required=True)

    create = sub.add_parser("create", help="Réserve l'ID, écrit le squelette v3 et ajoute la ligne d'index")
    create.add_argument("--type", required=True, choices=sorted(TYPES))
    create.add_argument("--theme", required=True, choices=sorted(THEMES))
    create.add_argument("--title", required=True)
    create.add_argument("--slug", help="kebab-case ; dérivé du titre si absent")
    create.add_argument("--keywords", help="séparés par ;")
    create.add_argument("--summary")
    create.add_argument("--objective")
    create.add_argument("--linked", help="IDs séparés par ;")
    create.add_argument("--question")
    create.add_argument("--dossier")
    create.add_argument("--previous")
    create.add_argument("--prolongement")
    create.add_argument("--etape")
    create.add_argument("--pillar", choices=PILLARS)
    create.add_argument("--posture", choices=POSTURES)
    create.add_argument("--tags", help="tags sujet supplémentaires séparés par ;")
    create.add_argument("--fondamental-id", help="atelier : ID du fondamental (sentier_fondamentaux.csv)")
    create.add_argument("--dossier-dir", help="dossier : sous-dossier de 03_Dossiers/<Theme>/")
    create.add_argument("--routine", choices=("quotidienne", "hebdomadaire", "mensuelle"), help="défaut selon le type")
    create.add_argument("--date", help="YYYY-MM-DD, défaut aujourd'hui")
    create.add_argument("--dry-run", action="store_true")
    create.set_defaults(handler=cmd_create)

    stage = sub.add_parser("stage", help="Copie le fichier canonique dans 07_A_Publier/<date>_<slug>/")
    stage.add_argument("id")
    stage.add_argument("--date", help="YYYY-MM-DD, défaut aujourd'hui")
    stage.add_argument("--force", action="store_true", help="copier malgré un contrôle v3 KO")
    stage.set_defaults(handler=cmd_stage)

    args = parser.parse_args()
    ROOT = Path(args.root).resolve()
    args.index = args.index or str(ROOT / "index_editorial.csv")
    print(json.dumps(args.handler(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
