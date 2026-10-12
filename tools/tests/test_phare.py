"""Tests hors ligne de l'orchestrateur (tools/phare.py) : arborescences temporaires, aucune écriture dans le dépôt.

  python -m unittest discover -s tools/tests
"""

from __future__ import annotations

import contextlib
import csv
import io
import sys
import tempfile
import unittest
from datetime import date, datetime
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import phare  # noqa: E402

INDEX_COLS = ["ID", "Type", "Theme", "Titre", "Statut", "Date_creation", "Date_publication_WP",
              "Chemin_dossier", "Tags_WP"]
RETRO_COMPLETE = """# Semaine {p}

## Traces de la semaine

(blocs de séance)

## Rétro

### Décisions précédentes

{texte}

### Ajustements proposés

### Décisions

| N° | Décision | Priorité | Échéance | État |
|---|---|---|---|---|
{decisions}
"""


class Base(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.base = Path(self._tmp.name)
        self.r = phare.Racine(self.base)
        self.index_rows: list[dict[str, str]] = []
        self.ecrire_index()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def ecrire_index(self) -> None:
        with self.r.index.open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=INDEX_COLS)
            w.writeheader()
            for row in self.index_rows:
                w.writerow({k: row.get(k, "") for k in INDEX_COLS})

    def article(self, id_: str, statut: str = "publie", publie_le: str = "2026-10-08", type_: str = "ACTU",
                chemin: str = "01_Actualites/Culture") -> None:
        self.index_rows.append({"ID": id_, "Type": type_, "Theme": "CULTURE", "Titre": f"Titre {id_}",
                                "Statut": statut, "Date_creation": publie_le,
                                "Date_publication_WP": publie_le if statut == "publie" else "",
                                "Chemin_dossier": chemin, "Tags_WP": "type-actualite"})
        self.ecrire_index()

    def journal(self, horo: str, periode: str, activite: str, statut: str, etape: str = "fin",
                ids: str = "", note: str = "") -> None:
        phare.ecrire_ligne(self.r, {"horodatage": horo, "periode": periode, "activite": activite,
                                    "statut": statut, "etape": etape, "ids": ids, "note": note})

    def retro(self, periode: str, decisions: str = "| D-1 | Ras | normale | — | faite |",
              texte: str = "Bilan " * 60) -> None:
        self.r.retros.mkdir(parents=True, exist_ok=True)
        (self.r.retros / f"{periode}.md").write_text(
            RETRO_COMPLETE.format(p=periode, texte=texte, decisions=decisions), encoding="utf-8")

    def retro_mensuelle(self, periode: str, decisions: str = "| D-1 | Ras | normale | — | faite |") -> None:
        self.r.retros.mkdir(parents=True, exist_ok=True)
        (self.r.retros / f"{periode}_retro_mensuelle.md").write_text(
            f"# Rétro {periode}\n\n## Cap du mois suivant\n\n{'Cap précis et argumenté. ' * 5}\n\n"
            f"## Décisions\n\n| N° | Décision | Priorité | Échéance | État |\n|---|---|---|---|---|\n{decisions}\n",
            encoding="utf-8")

    def decide(self, jour: str, heure: str = "12:00", reprendre: bool = False) -> dict[str, object]:
        j = date.fromisoformat(jour)
        h, m = heure.split(":")
        return phare.decider(self.r, j, datetime(j.year, j.month, j.day, int(h), int(m)), reprendre)

    def cli(self, *args: str) -> tuple[int, str]:
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            code = phare.main(["--racine", str(self.base), *args])
        return code, sortie.getvalue()

    def journee_complete(self, jour: str) -> None:
        for act in phare.QUOTIDIENNES:
            self.journal(f"{jour} 10:00", jour, act, "termine_sans_publication", note="test")


class TestPeriodes(unittest.TestCase):
    def test_periodes_par_defaut(self) -> None:
        lundi = date(2026, 10, 19)
        self.assertEqual(phare.periode_par_defaut("generale", lundi), "2026-10-19")
        self.assertEqual(phare.periode_par_defaut("fil", lundi), "2026-S43")
        self.assertEqual(phare.periode_par_defaut("retro_hebdo", lundi), "2026-S42")
        self.assertEqual(phare.periode_par_defaut("retro_mensuelle", date(2026, 11, 2)), "2026-10")
        self.assertEqual(phare.bornes_mois("2026-12"), (date(2026, 12, 1), date(2026, 12, 31)))


class TestDecision(Base):
    def test_premier_jour_pas_de_retro_anterieure(self) -> None:
        d = self.decide("2026-10-12")
        self.assertEqual((d["type"], d["activite"]), ("action", "generale"))

    def test_quotidiennes_dans_l_ordre(self) -> None:
        self.journal("2026-10-13 09:00", "2026-10-13", "generale", "publie", ids="2026-567")
        self.assertEqual(self.decide("2026-10-13")["activite"], "curiosite")
        self.journal("2026-10-13 11:00", "2026-10-13", "curiosite", "brouillon", ids="2026-568", note="chiffre")
        self.assertEqual(self.decide("2026-10-13")["activite"], "question")

    def test_journee_complete(self) -> None:
        self.journee_complete("2026-10-13")
        d = self.decide("2026-10-13")
        self.assertEqual(d["type"], "rien")

    def test_lundi_retro_hebdo_due(self) -> None:
        d = self.decide("2026-10-19")
        self.assertEqual((d["activite"], d["periode"]), ("retro_hebdo", "2026-S42"))
        self.journal("2026-10-19 09:00", "2026-S42", "retro_hebdo", "termine")
        self.assertEqual(self.decide("2026-10-19")["activite"], "generale")

    def test_retro_hebdo_seulement_semaine_precedente(self) -> None:
        d = self.decide("2026-10-27")
        self.assertEqual(d["periode"], "2026-S43")

    def test_premier_du_mois(self) -> None:
        self.journal("2026-11-02 08:00", "2026-S44", "retro_hebdo", "termine")
        d = self.decide("2026-11-02")
        self.assertEqual((d["activite"], d["periode"]), ("retro_mensuelle", "2026-10"))
        self.journal("2026-11-02 09:00", "2026-10", "retro_mensuelle", "termine")
        self.assertEqual(self.decide("2026-11-02")["activite"], "consolidation")
        self.journal("2026-11-02 10:00", "2026-10", "consolidation", "termine")
        self.assertEqual(self.decide("2026-11-02")["activite"], "generale")

    def test_pas_de_retro_mensuelle_de_septembre(self) -> None:
        self.assertEqual(self.decide("2026-10-14")["activite"], "generale")

    def test_verrou_actif(self) -> None:
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="redaction")
        d = self.decide("2026-10-13", "11:30")
        self.assertEqual(d["type"], "verrou")
        self.assertIn("Séance active", str(d["raison"]))
        code, _ = self.cli("--date", "2026-10-13", "--heure", "11:30", "start", "curiosite")
        self.assertEqual(code, 3)

    def test_verrou_perime_devient_reprise(self) -> None:
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="debut")
        self.journal("2026-10-13 10:20", "2026-10-13", "generale", "en_cours", etape="redaction", ids="2026-567")
        d = self.decide("2026-10-13", "14:00")
        self.assertEqual((d["type"], d["activite"]), ("reprise", "generale"))
        self.assertIn("même ID", str(d["raison"]))

    def test_reprendre_force_le_verrou(self) -> None:
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="debut")
        d = self.decide("2026-10-13", "10:30", reprendre=True)
        self.assertEqual(d["type"], "reprise")

    def test_interruption_apres_wp_draft(self) -> None:
        self.article("2026-567", statut="wp_draft")
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="debut")
        self.journal("2026-10-13 10:40", "2026-10-13", "generale", "en_cours", etape="controle_ok", ids="2026-567")
        d = self.decide("2026-10-13", "15:00")
        self.assertEqual(d["type"], "reprise")
        self.assertIn("--force", str(d["raison"]))
        self.assertIn("Ne pas recréer", str(d["raison"]))

    def test_interruption_apres_publication(self) -> None:
        self.article("2026-567", publie_le="2026-10-13")
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="wp", ids="2026-567")
        d = self.decide("2026-10-13", "15:00")
        self.assertIn("close … --statut publie", str(d["raison"]))

    def test_incident_veille_reste_ouvert(self) -> None:
        self.journal("2026-10-12 10:00", "2026-10-12", "question", "en_cours", etape="debut")
        self.journal("2026-10-12 10:30", "2026-10-12", "question", "incident", note="WP 500")
        d = self.decide("2026-10-13")
        self.assertEqual((d["type"], d["activite"], d["periode"]), ("reprise", "question", "2026-10-12"))

    def test_incident_apres_deux_tentatives(self) -> None:
        for h in ("10:00", "11:00"):
            self.journal(f"2026-10-13 {h}", "2026-10-13", "generale", "en_cours", etape="debut")
            self.journal(f"2026-10-13 {h[:2]}:30", "2026-10-13", "generale", "incident", note="WP 500")
        d = self.decide("2026-10-13", "16:00")
        self.assertEqual(d["type"], "intervention")
        code, _ = self.cli("--date", "2026-10-13", "--heure", "16:00", "start", "generale")
        self.assertEqual(code, 3)

    def test_brouillon_pas_relance(self) -> None:
        self.article("2026-567", statut="wp_draft")
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "brouillon", ids="2026-567", note="source")
        d = self.decide("2026-10-13")
        self.assertEqual(d["activite"], "curiosite")
        code, sortie = self.cli("--date", "2026-10-13", "next")
        self.assertIn("Brouillons en attente du fondateur : 2026-567", sortie)

    def test_report_volontaire(self) -> None:
        code, _ = self.cli("--date", "2026-10-13", "reporter", "generale", "--note", "fondateur absent")
        self.assertEqual(code, 0)
        self.assertEqual(self.decide("2026-10-13")["activite"], "curiosite")

    def test_fil_seuil(self) -> None:
        self.article("2026-562", publie_le="2026-10-06", type_="SYNTHESE", chemin="06_Syntheses/Fil_du_Phare")
        for i, j in ((563, "08"), (564, "08"), (565, "09")):
            self.article(f"2026-{i}", publie_le=f"2026-10-{j}")
        d = self.decide("2026-10-16")
        self.assertEqual(d["activite"], "generale")
        self.assertTrue(any("3/4" in i for i in d["infos"]))  # type: ignore[union-attr]
        self.article("2026-566", publie_le="2026-10-12")
        d = self.decide("2026-10-16")
        self.assertEqual((d["activite"], d["periode"]), ("fil", "2026-S42"))

    def test_fil_pas_avant_vendredi(self) -> None:
        for i in range(563, 568):
            self.article(f"2026-{i}", publie_le="2026-10-13")
        self.assertEqual(self.decide("2026-10-15")["activite"], "generale")

    def test_decision_bloquante_suspend(self) -> None:
        self.journal("2026-10-19 09:00", "2026-S42", "retro_hebdo", "termine")
        self.retro("2026-S42", "| D-2026-S42-1 | Corriger le maillage | bloquante | 2026-10-20 | à faire |\n"
                               "| D-2026-S42-2 | Varier les thèmes | importante | 2026-10-25 | en cours |")
        d = self.decide("2026-10-20")
        self.assertEqual(d["type"], "suspendu")
        self.assertIn("D-2026-S42-1", str(d["raison"]))
        self.assertTrue(any("D-2026-S42-2" in i for i in d["infos"]))  # type: ignore[union-attr]
        self.retro("2026-S42", "| D-2026-S42-1 | Corriger le maillage | bloquante | 2026-10-20 | faite |")
        self.assertEqual(self.decide("2026-10-20")["activite"], "generale")

    def test_decisions_de_la_retro_la_plus_recente(self) -> None:
        self.retro("2026-S42", "| D-2026-S42-1 | Ancienne | bloquante | — | à faire |")
        self.retro("2026-S43", "| D-2026-S42-1 | Ancienne | bloquante | — | faite |")
        self.assertEqual(phare.decisions_ouvertes(self.r), [])

    def test_suggestion_signalement(self) -> None:
        self.journee_complete("2026-10-13")
        self.r.signalements.parent.mkdir(parents=True, exist_ok=True)
        self.r.signalements.write_text(
            "## Ouverts\n\n| Date | ID | Titre | Signalé par | Constat | Suite proposée |\n|---|---|---|---|---|---|\n"
            "| 2026-10-13 | 2026-100 | T | quotidienne | daté | rattrapage |\n\n## Traités\n", encoding="utf-8")
        d = self.decide("2026-10-13")
        self.assertIn("1 signalement", str(d["suggestion"]))


class TestCommandes(Base):
    def test_cycle_publie(self) -> None:
        self.assertEqual(self.cli("--date", "2026-10-13", "start", "generale")[0], 0)
        self.assertEqual(self.cli("--date", "2026-10-13", "etape", "generale", "--etape", "redaction",
                                  "--ids", "2026-567")[0], 0)
        code, sortie = self.cli("--date", "2026-10-13", "close", "generale", "--statut", "publie")
        self.assertEqual(code, 2)
        self.assertIn("absent", sortie)
        self.article("2026-567", publie_le="2026-10-13")
        self.assertEqual(self.cli("--date", "2026-10-13", "close", "generale", "--statut", "publie")[0], 0)
        self.assertEqual(self.cli("--date", "2026-10-13", "start", "generale")[0], 3)

    def test_brouillon_exige_wp_draft_et_motif(self) -> None:
        self.cli("--date", "2026-10-13", "start", "generale", "--ids", "2026-567")
        self.article("2026-567", statut="wp_draft")
        self.assertEqual(self.cli("--date", "2026-10-13", "close", "generale", "--statut", "brouillon")[0], 2)
        self.assertEqual(self.cli("--date", "2026-10-13", "close", "generale", "--statut", "brouillon",
                                  "--note", "chiffre non vérifié")[0], 0)

    def test_termine_reserve_aux_activites_internes(self) -> None:
        self.cli("--date", "2026-10-13", "start", "generale")
        self.assertEqual(self.cli("--date", "2026-10-13", "close", "generale", "--statut", "termine")[0], 2)

    def test_etape_sans_seance(self) -> None:
        self.assertEqual(self.cli("--date", "2026-10-13", "etape", "generale", "--etape", "wp")[0], 3)

    def test_close_retro_hebdo_exige_contenu(self) -> None:
        self.cli("--date", "2026-10-19", "start", "retro_hebdo")
        code, sortie = self.cli("--date", "2026-10-19", "close", "retro_hebdo", "--statut", "termine")
        self.assertEqual(code, 2)
        self.retro("2026-S42", texte="(à remplir)")
        self.assertEqual(self.cli("--date", "2026-10-19", "close", "retro_hebdo", "--statut", "termine")[0], 2)
        self.retro("2026-S42", decisions="", texte="Bilan " * 60)
        self.assertEqual(self.cli("--date", "2026-10-19", "close", "retro_hebdo", "--statut", "termine")[0], 2)
        self.retro("2026-S42")
        self.assertEqual(self.cli("--date", "2026-10-19", "close", "retro_hebdo", "--statut", "termine")[0], 0)

    def test_close_retro_mensuelle(self) -> None:
        self.cli("--date", "2026-11-02", "start", "retro_mensuelle")
        self.assertEqual(self.cli("--date", "2026-11-02", "close", "retro_mensuelle", "--statut", "termine")[0], 2)
        self.retro_mensuelle("2026-10")
        self.assertEqual(self.cli("--date", "2026-11-02", "close", "retro_mensuelle", "--statut", "termine")[0], 0)

    def test_reprise_conserve_les_ids(self) -> None:
        self.cli("--date", "2026-10-13", "--heure", "10:00", "start", "generale")
        self.cli("--date", "2026-10-13", "--heure", "10:10", "etape", "generale", "--etape", "redaction",
                 "--ids", "2026-567")
        self.cli("--date", "2026-10-13", "--heure", "15:00", "start", "generale")
        derniere = phare.lire_journal(self.r)[-1]
        self.assertEqual((derniere["etape"], derniere["ids"]), ("debut", "2026-567"))

    def test_contexte_mensuel_jours_non_couverts(self) -> None:
        self.journal("2026-10-19 09:00", "2026-S42", "retro_hebdo", "termine")
        self.journal("2026-10-14 10:00", "2026-10-14", "generale", "publie", ids="2026-567")
        self.journal("2026-10-28 10:00", "2026-10-28", "generale", "publie", ids="2026-580")
        self.article("2026-566", publie_le="2026-10-12")
        self.article("2026-580", publie_le="2026-10-28")
        code, sortie = self.cli("--date", "2026-11-02", "contexte", "retro_mensuelle")
        self.assertEqual(code, 0)
        self.assertIn("2026-S42 : termine", sortie)
        self.assertIn("2026-S44 : absente", sortie)
        ligne = next(l for l in sortie.splitlines() if l.startswith("- 2026-10-28"))
        self.assertNotIn("2026-10-14", ligne)

    def test_next_code_arret(self) -> None:
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="debut")
        code, sortie = self.cli("--date", "2026-10-13", "--heure", "10:30", "next")
        self.assertEqual(code, 3)
        self.assertIn("ARRÊT (verrou)", sortie)


class TestModeBrouillons(Base):
    def activer(self) -> None:
        self.r.mode_brouillons.parent.mkdir(parents=True, exist_ok=True)
        self.r.mode_brouillons.write_text("pilote", encoding="utf-8")

    def test_bilan_pilote_suggere(self) -> None:
        self.journee_complete("2026-10-13")
        self.assertEqual(self.decide("2026-10-13")["suggestion"], "Aucune suggestion.")
        self.activer()
        self.assertIn("Bilan de pilote dû", str(self.decide("2026-10-13")["suggestion"]))
        self.r.retros.mkdir(parents=True, exist_ok=True)
        self.r.bilan_pilote("2026-10-13").write_text("bilan", encoding="utf-8")
        self.assertNotIn("Bilan de pilote", str(self.decide("2026-10-13")["suggestion"]))

    def test_next_signale_le_mode(self) -> None:
        self.assertNotIn("MODE BROUILLONS", self.cli("--date", "2026-10-13", "next")[1])
        self.activer()
        self.assertIn("MODE BROUILLONS", self.cli("--date", "2026-10-13", "next")[1])

    def test_brouillon_publie_ensuite(self) -> None:
        self.article("2026-567", statut="wp_draft", publie_le="2026-10-13")
        self.article("2026-568", publie_le="2026-10-13")
        self.journal("2026-10-13 10:00", "2026-10-13", "generale", "en_cours", etape="debut")
        self.journal("2026-10-13 10:45", "2026-10-13", "generale", "brouillon", ids="2026-567", note="pilote")
        self.journal("2026-10-13 11:00", "2026-10-13", "curiosite", "brouillon", ids="2026-568", note="pilote")
        journal = phare.lire_journal(self.r)
        st_index = phare.statuts_index(phare.lire_index(self.r))
        self.assertEqual(phare.brouillons_publies(journal, st_index), ["2026-568"])
        code, sortie = self.cli("--date", "2026-10-13", "contexte", "bilan_pilote")
        self.assertEqual(code, 0)
        ligne = next(l for l in sortie.splitlines() if "generale" in l and l.startswith("- "))
        self.assertIn("1 tentative(s), 45 min", ligne)
        self.assertNotIn("publié ensuite", ligne)
        ligne = next(l for l in sortie.splitlines() if "curiosite" in l and l.startswith("- "))
        self.assertIn("publié ensuite par le fondateur : 2026-568", ligne)
        self.assertIn("Brouillons publiés ensuite (toutes périodes) : 2026-568", sortie)


class TestRefusScripts(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.sentinelle = Path(self._tmp.name) / "Mode_brouillons.md"
        self.sentinelle.write_text("pilote", encoding="utf-8")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def test_wp_refresh_body_refuse(self) -> None:
        import wp_refresh_body
        sortie = io.TextIOWrapper(io.BytesIO(), encoding="utf-8")
        with mock.patch.object(wp_refresh_body, "MODE_BROUILLONS", self.sentinelle), \
                mock.patch.object(sys, "argv", ["wp_refresh_body.py", "01_Actualites/x.md"]), \
                contextlib.redirect_stdout(sortie):
            self.assertEqual(wp_refresh_body.main(), 2)

    def test_post_linking_refuse_publish_final(self) -> None:
        import post_linking
        with mock.patch.object(post_linking, "MODE_BROUILLONS", self.sentinelle), \
                mock.patch.object(sys, "argv", ["post_linking.py", "07_A_Publier/x", "--index", "i.csv",
                                                "--config", "c.json", "--publish-final"]), \
                contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(post_linking.main(), 2)


if __name__ == "__main__":
    unittest.main()
