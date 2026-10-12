#!/usr/bin/env python3
"""Orchestrateur du Phare (plan.md D22) : état, prochaine action et journal des séances.

Décision déterministe, sans IA ni réseau. Lit le journal, l'index, les rétros et les signalements ;
écrit seulement dans 00_Systeme/Journal_phare.csv (ajout en fin de fichier).

  python tools/phare.py next [--date AAAA-MM-JJ] [--heure HH:MM] [--reprendre]
  python tools/phare.py start <activite> [--periode P] [--ids ID;ID] [--note …]
  python tools/phare.py etape <activite> --etape redaction|controle_ok|wp [--periode P] [--ids …]
  python tools/phare.py close <activite> --statut S [--periode P] [--ids …] [--note …]
  python tools/phare.py reporter <activite> --note … [--periode P]
  python tools/phare.py contexte retro_hebdo|retro_mensuelle|bilan_pilote [--periode P]
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from index_editorial_utils import read_index  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PILOTE_DEBUT = date(2026, 10, 12)
VERROU_HEURES = 3
TENTATIVES_MAX = 2
FIL_MIN_ARTICLES = 4
FIL_PREMIER_JOUR = 4  # vendredi (lundi = 0)

JOURNAL_COLS = ["horodatage", "periode", "activite", "statut", "etape", "ids", "note"]
QUOTIDIENNES = ["generale", "curiosite", "question", "rattrapage"]
ACTIVITES = ["retro_hebdo", "retro_mensuelle", "consolidation", "fil", *QUOTIDIENNES]
STATUTS = ["en_cours", "publie", "brouillon", "termine", "termine_sans_publication", "reporte", "incident"]
TRAITES = {"publie", "brouillon", "termine", "termine_sans_publication", "reporte"}
ETAPES = ["debut", "redaction", "controle_ok", "wp"]

LANCEMENT = {
    "retro_hebdo": "skill routine-hebdomadaire, partie B (rétro hebdomadaire de {p})",
    "retro_mensuelle": "skill routine-mensuelle, partie A (rétro mensuelle de {p})",
    "consolidation": "skill routine-mensuelle, partie B (consolidation de {p})",
    "fil": "skill routine-hebdomadaire, partie A (Fil du Phare, semaine {p})",
    "generale": "skill routine-quotidienne, activité generale",
    "curiosite": "skill routine-quotidienne, activité curiosite",
    "question": "skill routine-quotidienne, activité question",
    "rattrapage": "skill routine-renovation, variante rattrapage",
}
ETATS_DECISION_CLOS = {"faite", "abandonnée", "abandonnee"}


class Racine:
    def __init__(self, base: Path) -> None:
        self.base = base
        self.journal = base / "00_Systeme" / "Journal_phare.csv"
        self.index = base / "index_editorial.csv"
        self.retros = base / "06_Syntheses" / "Retros"
        self.signalements = base / "00_Systeme" / "Signalements_renovation.md"
        self.mode_brouillons = base / "00_Systeme" / "Mode_brouillons.md"

    def bilan_pilote(self, jour: str) -> Path:
        return self.retros / f"{jour}_bilan_pilote.md"


# --- Périodes -------------------------------------------------------------

def semaine(d: date) -> str:
    annee, num, _ = d.isocalendar()
    return f"{annee}-S{num:02d}"


def bornes_semaine(periode: str) -> tuple[date, date]:
    annee, num = periode.split("-S")
    lundi = date.fromisocalendar(int(annee), int(num), 1)
    return lundi, lundi + timedelta(days=6)


def mois(d: date) -> str:
    return f"{d.year}-{d.month:02d}"


def bornes_mois(periode: str) -> tuple[date, date]:
    debut = date(int(periode[:4]), int(periode[5:7]), 1)
    suivant = (debut + timedelta(days=32)).replace(day=1)
    return debut, suivant - timedelta(days=1)


def periode_par_defaut(activite: str, jour: date) -> str:
    if activite in QUOTIDIENNES:
        return jour.isoformat()
    if activite == "fil":
        return semaine(jour)
    if activite == "retro_hebdo":
        return semaine(jour - timedelta(days=7))
    return mois(jour.replace(day=1) - timedelta(days=1))


# --- Lectures -------------------------------------------------------------

def lire_journal(r: Racine) -> list[dict[str, str]]:
    if not r.journal.exists():
        return []
    with r.journal.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def ecrire_ligne(r: Racine, ligne: dict[str, str]) -> None:
    neuf = not r.journal.exists()
    r.journal.parent.mkdir(parents=True, exist_ok=True)
    with r.journal.open("a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=JOURNAL_COLS)
        if neuf:
            w.writeheader()
        w.writerow({k: ligne.get(k, "") for k in JOURNAL_COLS})


def lire_index(r: Racine) -> list[dict[str, str]]:
    if not r.index.exists():
        return []
    return read_index(r.index)[1]


def statuts_index(rows: list[dict[str, str]]) -> dict[str, str]:
    return {row.get("ID", ""): row.get("Statut", "") for row in rows}


def split_ids(valeur: str) -> list[str]:
    return [x.strip() for x in re.split(r"[;,\s]+", valeur or "") if x.strip()]


def etats_par_cle(journal: list[dict[str, str]]) -> dict[tuple[str, str], dict[str, str]]:
    etats: dict[tuple[str, str], dict[str, str]] = {}
    for ligne in journal:
        etats[(ligne["periode"], ligne["activite"])] = ligne
    return etats


def tentatives(journal: list[dict[str, str]], cle: tuple[str, str]) -> int:
    return sum(1 for l in journal if (l["periode"], l["activite"]) == cle and l["etape"] == "debut")


def horodatage(ligne: dict[str, str]) -> datetime:
    return datetime.strptime(ligne["horodatage"], "%Y-%m-%d %H:%M")


def traite(etats: dict[tuple[str, str], dict[str, str]], periode: str, activite: str) -> bool:
    ligne = etats.get((periode, activite))
    return bool(ligne) and ligne["statut"] in TRAITES


def dernier_fil(index: list[dict[str, str]]) -> str:
    dates = [
        row.get("Date_publication_WP", "")[:10]
        for row in index
        if row.get("Type") == "SYNTHESE" and "Fil_du_Phare" in row.get("Chemin_dossier", "")
        and row.get("Statut") == "publie"
    ]
    return max(dates, default="")


def publies_depuis(index: list[dict[str, str]], depuis: str) -> list[str]:
    return [
        row["ID"] for row in index
        if row.get("Statut") == "publie" and row.get("Type") != "SYNTHESE"
        and row.get("Date_publication_WP", "")[:10] > depuis
    ]


def fichier_retro(r: Racine, activite: str, periode: str) -> Path:
    if activite == "retro_hebdo":
        return r.retros / f"{periode}.md"
    return r.retros / f"{periode}_retro_mensuelle.md"


def section(texte: str, titre: str) -> str:
    m = re.search(rf"^##\s+{re.escape(titre)}\s*$(.*?)(?=^##\s|\Z)", texte, re.M | re.S)
    return m.group(1) if m else ""


def lire_decisions(chemin: Path) -> list[dict[str, str]]:
    """Table « Décisions » : | N° | Décision | Priorité | Échéance | État |."""
    if not chemin.exists():
        return []
    texte = chemin.read_text(encoding="utf-8")
    m = re.search(r"^#{2,3}\s+Décisions\s*$(.*?)(?=^#{1,3}\s|\Z)", texte, re.M | re.S)
    if not m:
        return []
    decisions = []
    for ligne in m.group(1).splitlines():
        cellules = [c.strip() for c in ligne.strip().strip("|").split("|")]
        if len(cellules) < 5 or not ligne.strip().startswith("|"):
            continue
        if cellules[0] in ("N°", "") or set(cellules[0]) <= {"-", ":"}:
            continue
        decisions.append({
            "num": cellules[0], "texte": cellules[1], "priorite": cellules[2].lower(),
            "echeance": cellules[3], "etat": cellules[4].lower(), "source": chemin.name,
        })
    return decisions


def derniere_retro(r: Racine) -> Path | None:
    """Rétro la plus récente (par fin de période) : elle porte l'état courant des décisions."""
    candidats: list[tuple[date, Path]] = []
    if not r.retros.exists():
        return None
    for chemin in r.retros.glob("*.md"):
        nom = chemin.stem
        if re.fullmatch(r"\d{4}-S\d{2}", nom):
            fin = bornes_semaine(nom)[1]
        elif re.fullmatch(r"\d{4}-\d{2}_retro_mensuelle", nom):
            fin = bornes_mois(nom[:7])[1] + timedelta(hours=1)  # le mois passe après la semaine qui le clôt
        else:
            continue
        if lire_decisions(chemin):
            candidats.append((fin, chemin))
    return max(candidats)[1] if candidats else None


def decisions_ouvertes(r: Racine) -> list[dict[str, str]]:
    chemin = derniere_retro(r)
    if not chemin:
        return []
    return [d for d in lire_decisions(chemin) if d["etat"] not in ETATS_DECISION_CLOS]


def signalements_ouverts(r: Racine) -> int:
    if not r.signalements.exists():
        return 0
    corps = section(r.signalements.read_text(encoding="utf-8"), "Ouverts")
    return sum(1 for l in corps.splitlines() if re.match(r"^\|\s*\d{4}-\d{2}-\d{2}", l))


def retro_hebdo_complete(r: Racine, periode: str) -> str:
    """Vide si la rétro est complète, sinon le motif du refus."""
    chemin = fichier_retro(r, "retro_hebdo", periode)
    if not chemin.exists():
        return f"{chemin.name} absent"
    corps = section(chemin.read_text(encoding="utf-8"), "Rétro")
    prose = "".join(l for l in corps.splitlines() if not l.lstrip().startswith(("#", "|")))
    if len(re.sub(r"\(.*?\)|\s", "", prose)) < 200:
        return "section « ## Rétro » vide ou trop courte"
    if not lire_decisions(chemin):
        return "table « ### Décisions » absente ou vide"
    return ""


def retro_mensuelle_complete(r: Racine, periode: str) -> str:
    chemin = fichier_retro(r, "retro_mensuelle", periode)
    if not chemin.exists():
        return f"{chemin.name} absent"
    texte = chemin.read_text(encoding="utf-8")
    for titre in ("Cap du mois suivant",):
        if len(section(texte, titre).strip()) < 50:
            return f"section « ## {titre} » vide"
    if not lire_decisions(chemin):
        return "table « ## Décisions » absente ou vide"
    return ""


# --- Décision -------------------------------------------------------------

def instruction_reprise(ligne: dict[str, str], st_index: dict[str, str]) -> str:
    activite, ids = ligne["activite"], split_ids(ligne["ids"])
    if activite.startswith("retro"):
        return "Reprendre la rétro dans le fichier existant (ne pas le recréer)."
    if activite == "rattrapage":
        cible = ", ".join(ids) or "l'article choisi"
        return (f"Reprendre l'action sur {cible} : comparer local et WP (`wp_pull_body.py <ID>` à blanc) "
                "avant tout refresh ; contrôle prépublication avant `wp_refresh_body.py`.")
    if not ids:
        return "Aucun ID créé : relancer l'activité depuis le début."
    etats = {i: st_index.get(i, "absent") for i in ids}
    detail = ", ".join(f"{i} {s}" for i, s in etats.items())
    if all(s == "publie" for s in etats.values()):
        return (f"Publié ({detail}) : terminer mémoire, Radar, trace et `verify_publication.py`, "
                "puis `close … --statut publie`.")
    if ligne["etape"] in ("controle_ok", "wp") or "wp_draft" in etats.values():
        return (f"{detail} : contrôle déjà PUBLIER ou envoi WP entamé → relancer `daily_run.py "
                "--publish-existing <même dossier> --keep-publish-folder --force` (le push retrouve le "
                "post par slug). Ne pas recréer l'article.")
    return (f"{detail} : reprendre avec le même ID (rédaction, `stage`, contrôle prépublication). "
            "Jamais de nouveau `create`.")


def decider(r: Racine, jour: date, maintenant: datetime, reprendre: bool = False) -> dict[str, object]:
    journal = lire_journal(r)
    index = lire_index(r)
    st_index = statuts_index(index)
    etats = etats_par_cle(journal)
    infos: list[str] = []

    actives = [l for l in etats.values() if l["statut"] == "en_cours"
               and maintenant - horodatage(l) < timedelta(hours=VERROU_HEURES)]
    if actives and not reprendre:
        l = actives[0]
        return {"type": "verrou", "activite": l["activite"], "periode": l["periode"],
                "raison": (f"Séance active : {l['activite']} ({l['periode']}), dernière étape "
                           f"« {l['etape']} » à {l['horodatage'][11:]}. Rien n'est lancé. Si cette séance "
                           f"est réellement interrompue : `routine phare — reprendre`."),
                "infos": infos}

    ouverts = sorted((l for l in etats.values() if l["statut"] in ("incident", "en_cours")), key=horodatage)
    for l in ouverts:
        cle = (l["periode"], l["activite"])
        nature = "incident technique" if l["statut"] == "incident" else "séance interrompue"
        if tentatives(journal, cle) >= TENTATIVES_MAX:
            return {"type": "intervention", "activite": l["activite"], "periode": l["periode"],
                    "raison": (f"{nature} persistant : {l['activite']} ({l['periode']}, IDs "
                               f"{l['ids'] or '—'}) après {TENTATIVES_MAX} tentatives. Note : "
                               f"{l['note'] or '—'}. Intervention humaine requise ; une fois réglé : "
                               "`phare.py close` avec le statut réel, ou `phare.py reporter`."),
                    "infos": infos}
    if ouverts:
        l = ouverts[0]
        return {"type": "reprise", "activite": l["activite"], "periode": l["periode"],
                "raison": f"Reprise contrôlée ({l['statut']}, note : {l['note'] or '—'}). "
                          + instruction_reprise(l, st_index),
                "infos": infos}

    ouvertes = decisions_ouvertes(r)
    for d in ouvertes:
        infos.append(f"Décision {d['priorite']} ouverte : {d['num']} — {d['texte']} "
                     f"(échéance {d['echeance']}, {d['etat']}, {d['source']})")

    p_hebdo = periode_par_defaut("retro_hebdo", jour)
    if bornes_semaine(p_hebdo)[0] >= bornes_semaine(semaine(PILOTE_DEBUT))[0] and not traite(etats, p_hebdo, "retro_hebdo"):
        return action("retro_hebdo", p_hebdo, f"La semaine {p_hebdo} est terminée et n'a pas de rétro.", infos)

    p_mois = periode_par_defaut("retro_mensuelle", jour)
    if p_mois >= mois(PILOTE_DEBUT):
        if not traite(etats, p_mois, "retro_mensuelle"):
            return action("retro_mensuelle", p_mois, f"Le mois {p_mois} est terminé et n'a pas de rétro.", infos)

    bloquantes = [d for d in ouvertes if d["priorite"].startswith("bloquant")]
    if bloquantes:
        return {"type": "suspendu", "activite": "", "periode": "",
                "raison": ("Production suspendue : décision bloquante ouverte ("
                           + ", ".join(d["num"] for d in bloquantes)
                           + "). La traiter, puis passer son État à « faite » dans "
                           + bloquantes[0]["source"] + "."),
                "infos": infos}

    if p_mois >= mois(PILOTE_DEBUT) and not traite(etats, p_mois, "consolidation"):
        return action("consolidation", p_mois, f"Rétro de {p_mois} faite, consolidation du patrimoine due.", infos)

    if jour.weekday() >= FIL_PREMIER_JOUR:
        p_fil = semaine(jour)
        if not traite(etats, p_fil, "fil"):
            depuis = dernier_fil(index)
            n = len(publies_depuis(index, depuis))
            if n >= FIL_MIN_ARTICLES:
                return action("fil", p_fil, f"{n} articles publiés depuis le dernier Fil ({depuis or '—'}) : "
                              "seuil atteint (condition minimale ; sans connexion sérieuse → termine_sans_publication).", infos)
            infos.append(f"Fil : conditions non réunies ({n}/{FIL_MIN_ARTICLES} articles depuis {depuis or '—'}).")

    for activite in QUOTIDIENNES:
        if not traite(etats, jour.isoformat(), activite):
            return action(activite, jour.isoformat(), "Objectif quotidien non traité aujourd'hui.", infos)

    return {"type": "rien", "activite": "", "periode": "",
            "raison": "Aucune action obligatoire en attente pour cette période.",
            "suggestion": suggestion(r, journal, st_index, jour), "infos": infos}


def action(activite: str, periode: str, raison: str, infos: list[str]) -> dict[str, object]:
    return {"type": "action", "activite": activite, "periode": periode, "raison": raison, "infos": infos}


def ids_brouillon(journal: list[dict[str, str]]) -> set[str]:
    return {i for l in journal if l["statut"] == "brouillon" for i in split_ids(l["ids"])}


def brouillons_en_attente(journal: list[dict[str, str]], st_index: dict[str, str]) -> list[str]:
    return sorted(i for i in ids_brouillon(journal) if st_index.get(i) == "wp_draft")


def brouillons_publies(journal: list[dict[str, str]], st_index: dict[str, str]) -> list[str]:
    """Clos en brouillon par la séance, publiés ensuite par le fondateur (l'index fait foi)."""
    return sorted(i for i in ids_brouillon(journal) if st_index.get(i) == "publie")


def suggestion(r: Racine, journal: list[dict[str, str]], st_index: dict[str, str], jour: date) -> str:
    if r.mode_brouillons.exists() and not r.bilan_pilote(jour.isoformat()).exists():
        return (f"Bilan de pilote dû avant toute autre production : `routine phare — bilan pilote` "
                f"({r.bilan_pilote(jour.isoformat()).relative_to(r.base).as_posix()}).")
    brouillons = brouillons_en_attente(journal, st_index)
    if brouillons:
        return (f"Facultatif : relire le brouillon {brouillons[0]} (publication par le fondateur : "
                f"`verify_publication.py --publish-drafts {brouillons[0]}`).")
    n = signalements_ouverts(r)
    if n:
        return f"Facultatif : {n} signalement(s) de rénovation ouvert(s) (`routine renovation — rattrapage`)."
    return "Aucune suggestion."


# --- Commandes ------------------------------------------------------------

def maintenant_de(args: argparse.Namespace) -> tuple[date, datetime]:
    if args.date:
        jour = date.fromisoformat(args.date)
        h, m = (args.heure or "12:00").split(":")
        return jour, datetime(jour.year, jour.month, jour.day, int(h), int(m))
    now = datetime.now().replace(second=0, microsecond=0)
    return now.date(), now


def cmd_next(r: Racine, args: argparse.Namespace) -> int:
    jour, now = maintenant_de(args)
    journal = lire_journal(r)
    st_index = statuts_index(lire_index(r))
    d = decider(r, jour, now, reprendre=args.reprendre)
    jours = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    print(f"Orchestrateur du Phare — {jour.isoformat()} ({jours[jour.weekday()]}, {semaine(jour)})")
    if r.mode_brouillons.exists():
        print("MODE BROUILLONS (pilote) : rien n'est publié ni modifié en ligne ; variante `brouillons seulement`.")
    du_jour = [l for l in etats_par_cle(journal).values() if l["periode"] == jour.isoformat()]
    print("Aujourd'hui : " + (", ".join(f"{l['activite']} {l['statut']} {l['ids']}".strip() for l in du_jour) or "rien"))
    brouillons = brouillons_en_attente(journal, st_index)
    if brouillons:
        print("Brouillons en attente du fondateur : " + ", ".join(brouillons))
    for info in d["infos"]:  # type: ignore[union-attr]
        print(info)
    if d["type"] == "action":
        p = d["periode"]
        print(f"→ PROCHAINE ACTION : {d['activite']} (période {p})")
        print(f"  Raison : {d['raison']}")
        print(f"  1. python tools/phare.py start {d['activite']} --periode {p}")
        print(f"  2. {LANCEMENT[str(d['activite'])].format(p=p)}")
        return 0
    if d["type"] == "reprise":
        print(f"→ REPRISE : {d['activite']} (période {d['periode']})")
        print(f"  {d['raison']}")
        print(f"  1. python tools/phare.py start {d['activite']} --periode {d['periode']}")
        print(f"  2. {LANCEMENT[str(d['activite'])].format(p=d['periode'])}, en reprise")
        return 0
    if d["type"] == "rien":
        print(f"→ {d['raison']}")
        print(f"  {d['suggestion']}")
        return 0
    print(f"→ ARRÊT ({d['type']}) : {d['raison']}")
    return 3


def cle_args(args: argparse.Namespace) -> tuple[str, date, datetime]:
    jour, now = maintenant_de(args)
    return args.periode or periode_par_defaut(args.activite, jour), jour, now


def cmd_start(r: Racine, args: argparse.Namespace) -> int:
    periode, jour, now = cle_args(args)
    journal = lire_journal(r)
    etats = etats_par_cle(journal)
    cle = (periode, args.activite)
    for l in etats.values():
        if l["statut"] == "en_cours" and (l["periode"], l["activite"]) != cle \
                and now - horodatage(l) < timedelta(hours=VERROU_HEURES):
            print(f"Refusé : séance active {l['activite']} ({l['periode']}) depuis {l['horodatage'][11:]}.")
            return 3
    if traite(etats, periode, args.activite):
        print(f"Refusé : {args.activite} ({periode}) déjà traité ({etats[cle]['statut']}).")
        return 3
    if tentatives(journal, cle) >= TENTATIVES_MAX:
        print(f"Refusé : {TENTATIVES_MAX} tentatives déjà faites pour {args.activite} ({periode}).")
        return 3
    precedente = etats.get(cle)
    ids = args.ids or (precedente["ids"] if precedente else "")
    ecrire_ligne(r, {"horodatage": now.strftime("%Y-%m-%d %H:%M"), "periode": periode,
                     "activite": args.activite, "statut": "en_cours", "etape": "debut",
                     "ids": ids, "note": args.note or ""})
    print(f"Séance ouverte : {args.activite} ({periode})" + (f", IDs {ids}" if ids else ""))
    return 0


def cmd_etape(r: Racine, args: argparse.Namespace) -> int:
    periode, _, now = cle_args(args)
    precedente = etats_par_cle(lire_journal(r)).get((periode, args.activite))
    if not precedente or precedente["statut"] != "en_cours":
        print(f"Refusé : aucune séance en cours pour {args.activite} ({periode}).")
        return 3
    ecrire_ligne(r, {"horodatage": now.strftime("%Y-%m-%d %H:%M"), "periode": periode,
                     "activite": args.activite, "statut": "en_cours", "etape": args.etape,
                     "ids": args.ids or precedente["ids"], "note": args.note or precedente["note"]})
    print(f"Étape notée : {args.activite} ({periode}) → {args.etape}")
    return 0


def verifier_cloture(r: Racine, activite: str, periode: str, statut: str, ids: list[str], note: str) -> str:
    st_index = statuts_index(lire_index(r))
    if statut in ("termine_sans_publication", "reporte", "incident") and not note:
        return f"le statut {statut} exige une note (motif)"
    if statut == "publie":
        if not ids:
            return "publie exige les IDs"
        non = [f"{i} ({st_index.get(i, 'absent')})" for i in ids if st_index.get(i) != "publie"]
        if non:
            return "l'index ne dit pas « publie » pour " + ", ".join(non) + " → incident ou brouillon"
    if statut == "brouillon":
        if not ids:
            return "brouillon exige les IDs"
        non = [f"{i} ({st_index.get(i, 'absent')})" for i in ids if st_index.get(i) != "wp_draft"]
        if non:
            return "l'index ne dit pas « wp_draft » pour " + ", ".join(non) + " → brouillon WP non créé : incident"
        if not note:
            return "brouillon exige le motif du contrôle (note)"
    if statut == "termine":
        if activite == "retro_hebdo":
            return retro_hebdo_complete(r, periode)
        if activite == "retro_mensuelle":
            return retro_mensuelle_complete(r, periode)
        if activite != "consolidation":
            return f"termine est réservé aux rétros et à la consolidation (ici : publie, brouillon ou termine_sans_publication)"
    return ""


def cmd_close(r: Racine, args: argparse.Namespace) -> int:
    periode, _, now = cle_args(args)
    precedente = etats_par_cle(lire_journal(r)).get((periode, args.activite))
    if not precedente or precedente["statut"] not in ("en_cours", "incident"):
        print(f"Refusé : aucune séance ouverte ni incident pour {args.activite} ({periode}).")
        return 3
    ids = args.ids or precedente["ids"]
    motif = verifier_cloture(r, args.activite, periode, args.statut, split_ids(ids), args.note or "")
    if motif:
        print(f"Refusé : {motif}.")
        return 2
    ecrire_ligne(r, {"horodatage": now.strftime("%Y-%m-%d %H:%M"), "periode": periode,
                     "activite": args.activite, "statut": args.statut, "etape": "fin",
                     "ids": ids, "note": args.note or ""})
    print(f"Clôturé : {args.activite} ({periode}) → {args.statut}")
    return 0


def cmd_reporter(r: Racine, args: argparse.Namespace) -> int:
    periode, _, now = cle_args(args)
    etats = etats_par_cle(lire_journal(r))
    if traite(etats, periode, args.activite):
        print(f"Refusé : {args.activite} ({periode}) déjà traité.")
        return 3
    precedente = etats.get((periode, args.activite))
    ecrire_ligne(r, {"horodatage": now.strftime("%Y-%m-%d %H:%M"), "periode": periode,
                     "activite": args.activite, "statut": "reporte", "etape": "fin",
                     "ids": precedente["ids"] if precedente else "", "note": args.note})
    print(f"Reporté : {args.activite} ({periode})")
    return 0


def cmd_contexte(r: Racine, args: argparse.Namespace) -> int:
    jour, _ = maintenant_de(args)
    if args.activite == "bilan_pilote":
        periode = args.periode or jour.isoformat()
        debut = fin = date.fromisoformat(periode)
    else:
        periode = args.periode or periode_par_defaut(args.activite, jour)
        debut, fin = bornes_semaine(periode) if args.activite == "retro_hebdo" else bornes_mois(periode)
    journal = lire_journal(r)
    index = lire_index(r)
    st_index = statuts_index(index)
    print(f"Contexte {args.activite} {periode} ({debut} → {fin})")

    print("\n## Séances (état final par activité et jour ; tentatives, durée de la première ouverture à la clôture)")
    for (p, a), l in sorted(etats_par_cle(journal).items()):
        jour_l = horodatage(l).date()
        if debut <= jour_l <= fin or p == periode:
            lignes = [x for x in journal if (x["periode"], x["activite"]) == (p, a)]
            minutes = int((horodatage(l) - min(horodatage(x) for x in lignes)).total_seconds() // 60)
            ensuite = [i for i in split_ids(l["ids"]) if l["statut"] == "brouillon" and st_index.get(i) == "publie"]
            print(f"- {p} {a} : {l['statut']} {l['ids']} ({tentatives(journal, (p, a))} tentative(s), {minutes} min)"
                  + (f" → publié ensuite par le fondateur : {', '.join(ensuite)}" if ensuite else "")
                  + (f" — {l['note']}" if l["note"] else ""))
    publies_ensuite = brouillons_publies(journal, st_index)
    if publies_ensuite:
        print("Brouillons publiés ensuite (toutes périodes) : " + ", ".join(publies_ensuite)
              + " — vérifier le « relier en retour » des Questions et Applications.")

    print("\n## Publications et brouillons de l'index")
    for row in index:
        d = (row.get("Date_publication_WP") or row.get("Date_creation") or "")[:10]
        if debut.isoformat() <= d <= fin.isoformat() and row.get("Statut") in ("publie", "wp_draft"):
            regard = next((t for t in row.get("Tags_WP", "").split(";") if t.startswith("type-")), row.get("Type", ""))
            print(f"- {d} {row['ID']} {row.get('Statut')} {row.get('Theme')} {regard} — {row.get('Titre', '')[:90]}")

    if args.activite == "retro_mensuelle":
        etats = etats_par_cle(journal)
        print("\n## Rétros hebdomadaires qui chevauchent le mois")
        couverts: set[date] = set()
        lundi = debut - timedelta(days=debut.weekday())
        while lundi <= fin:
            p = semaine(lundi)
            ligne = etats.get((p, "retro_hebdo"))
            etat = ligne["statut"] if ligne else "absente"
            print(f"- {p} : {etat} ({fichier_retro(r, 'retro_hebdo', p).name})")
            if ligne and ligne["statut"] == "termine":
                couverts.update(lundi + timedelta(days=i) for i in range(7))
            lundi += timedelta(days=7)
        actifs = {horodatage(l).date() for l in journal}
        actifs |= {date.fromisoformat(row["Date_publication_WP"][:10]) for row in index
                   if row.get("Statut") == "publie" and debut.isoformat() <= row.get("Date_publication_WP", "")[:10] <= fin.isoformat()}
        non_couverts = sorted(j for j in actifs if debut <= j <= fin and j not in couverts)
        print("\n## Jours d'activité sans rétro hebdomadaire (à examiner directement)")
        print("- " + (", ".join(j.isoformat() for j in non_couverts) if non_couverts else "aucun"))

    print("\n## Décisions de la rétro précédente")
    chemin = derniere_retro(r)
    if chemin:
        for d in lire_decisions(chemin):
            print(f"- {d['num']} | {d['texte']} | {d['priorite']} | {d['echeance']} | {d['etat']}")
        print(f"(source : {chemin.name})")
    else:
        print("- aucune (première rétro)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Orchestrateur du Phare (plan.md D22).")
    parser.add_argument("--racine", type=Path, default=ROOT, help="Racine du dépôt (tests).")
    parser.add_argument("--date", help="Date simulée AAAA-MM-JJ (tests, à blanc).")
    parser.add_argument("--heure", help="Heure simulée HH:MM (avec --date).")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("next")
    p.add_argument("--reprendre", action="store_true", help="Ignorer le verrou d'une séance supposée active.")
    for nom in ("start", "etape", "close", "reporter"):
        p = sub.add_parser(nom)
        p.add_argument("activite", choices=ACTIVITES)
        p.add_argument("--periode")
        p.add_argument("--ids", default="")
        p.add_argument("--note", default="", required=(nom == "reporter"))
        if nom == "etape":
            p.add_argument("--etape", required=True, choices=ETAPES[1:])
        if nom == "close":
            p.add_argument("--statut", required=True, choices=[s for s in STATUTS if s != "en_cours"])
    p = sub.add_parser("contexte")
    p.add_argument("activite", choices=["retro_hebdo", "retro_mensuelle", "bilan_pilote"])
    p.add_argument("--periode")

    args = parser.parse_args(argv)
    r = Racine(args.racine)
    commandes = {"next": cmd_next, "start": cmd_start, "etape": cmd_etape, "close": cmd_close,
                 "reporter": cmd_reporter, "contexte": cmd_contexte}
    return commandes[args.cmd](r, args)


if __name__ == "__main__":
    sys.exit(main())
