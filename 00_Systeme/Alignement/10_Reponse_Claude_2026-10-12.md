# Réponse : implémentation de l'Orchestrateur du Phare

Décision consignée : `plan.md` D22 (v5.9). Rien n'est publié ni commité à ce stade.

## Arbitrages → mise en œuvre

| # | Arbitrage | Où |
|---|---|---|
| 1 | Rétros à partir du pilote : S42 le 19 octobre, octobre début novembre, pas de reconstitution | `tools/phare.py` (`PILOTE_DEBUT = 2026-10-12`) ; `06_Syntheses/Retros/README.md` |
| 2 | Quatre objectifs quotidiens, une activité par exécution ; contrôle non satisfait → brouillon ou absence de publication | `phare.py next` (générale → curiosité → question → rattrapage) ; skill `routine-phare` |
| 3 | Comité Radar et audit des fils dans la rétro hebdomadaire ; rapport et cap dans la rétro mensuelle ; Fil distinct | `routine-hebdomadaire` (A. Fil, B. rétro : B3 fils, B4 Radar) ; `routine-mensuelle` (A. rétro mensuelle, qui remplace `Rapports_mensuels/` ; B. consolidation) |
| 4 | Fil vendredi–dimanche, ≥ 4 articles depuis le Fil précédent ; pas de synthèse forcée | `phare.py` (`FIL_MIN_ARTICLES = 4`) ; `routine-hebdomadaire` A : sans connexion sérieuse → `termine_sans_publication` |
| 5a | Verrou : séance réellement en cours → signaler et arrêter | `phare.py next` : séance `en_cours` de moins de 3 h → ARRÊT (code 3) |
| 5b | Reprise contrôlée sans double création ni publication | Étapes `debut` / `redaction` / `controle_ok` / `wp` / `fin` ; consigne de reprise selon l'état de l'index (jamais de nouveau `create`, `daily_run --force` sur le même dossier, `wp_pull_body` à blanc pour un rattrapage) ; intervention humaine après 2 tentatives |
| 5c | Quatre cas distincts | Statuts `brouillon`, `incident`, `reporte`, `termine_sans_publication` ; `close` vérifie l'index (`publie` / `wp_draft`) ; un incident reste visible jusqu'à reprise réussie ; pas de sujet de remplacement |
| 6 | Rétros : six points, décisions conservées, problèmes bloquants visibles dans la sélection | Gabarit `## Rétro` en six sous-sections ; table `## Décisions` (N°, priorité bloquante / importante / normale, échéance, état) ; `next` lit la rétro la plus récente : une décision bloquante ouverte suspend la production, les importantes sont affichées ; `close` refuse une rétro vide |
| 7 | Contrôle prépublication conservé | `Controle_prepublication.md` étendu au Fil et à la consolidation ; « Rien n'est publié sans décision PUBLIER » |
| 8 | Simplicité, tests hors ligne, pilote en brouillons | Un script (~420 lignes), un CSV, 31 tests unittest ; variante `routine phare — brouillons seulement` |

## Fichiers

- Nouveaux : `tools/phare.py`, `tools/tests/test_phare.py`, `00_Systeme/Journal_phare.csv`, `.claude/skills/routine-phare/SKILL.md`, `.claude/commands/routine-phare.md`, ce fichier et les messages 9–10.
- Modifiés : skills `routine-quotidienne`, `routine-hebdomadaire`, `routine-mensuelle`, `routine-renovation` ; `00_Systeme/Controle_prepublication.md` ; `06_Syntheses/Retros/README.md` ; `CLAUDE.md` ; `actions.md` ; `plan.md`.

## Écart signalé

Le journal a été amorcé avec 2026-566 (publié le 12 octobre par l'ancienne routine quotidienne) en `generale`, pour que l'orchestrateur ne redemande pas une actualité générale le premier jour.

## Suite proposée

1. Pilote en brouillons : `routine phare — brouillons seulement`, une conversation par activité.
2. Première rétro hebdomadaire le 19 octobre : elle décide du passage à la publication réelle et de la soutenabilité des quatre activités.
