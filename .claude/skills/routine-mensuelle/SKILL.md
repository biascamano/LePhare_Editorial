---
name: routine-mensuelle
description: Routine mensuelle Le Phare — consolider le mois en savoir durable : dossiers, textes fondateurs, ateliers du Sentier, audit de navigation et d'équilibre, synthèse mensuelle (catégorie cycle), cap du mois suivant dans la mémoire éditoriale. Déclenché par « routine mensuelle » ou /routine-mensuelle.
---

# Routine mensuelle — Architecture du Phare

**Question du mois : « Qu'est-ce que tout cela construit durablement dans Le Phare ? »**

Le mensuel construit l'architecture. Il ne produit pas l'article d'actualité du jour.

Autonomie : exécuter l'analyse et les productions jusqu'au rapport. Les **créations lourdes** (nouveau dossier, nouveau texte fondateur, atelier Sentier) sont limitées à ce que le mois justifie — 0 est une réponse valide.

## 1. Examiner le mois écoulé

Mémoire §1 (lignes du mois), §2, §3 (Fils du Phare du mois), §4 (cap précédent). Pour chaque article : thème, Question du Phare, dossier, concepts, penseurs, Sentier, articles reliés.

## 2. Identifier les grands phénomènes

Sujets revenus plusieurs fois (dépendance, attention, accélération, travail, autonomie, vérité, technique, démocratie, responsabilité…). Un mot qui revient ne suffit pas : un dossier relie plusieurs événements **réellement différents** autour d'un même problème.

## 3. Mettre à jour les dossiers existants (`03_Dossiers/<Theme>/`)

Pour chaque dossier touché : question centrale encore pertinente ? articles associés à ajouter, sous-thèmes à réorganiser, manques, page principale à créer/mettre à jour ? Modifier les `.md` locaux, puis `python tools/build_hubs.py` : régénère `## Liens internes du dossier` de chaque page principale (plus petit ID du sous-dossier) depuis l'index — autres volets du sous-dossier + articles dont l'en-tête `Dossier :` vise ce dossier. Traiter les avertissements `!` (dossier inconnu, chemin hors `03_Dossiers`). Le script affiche les commandes `wp_push_draft.py --refresh-body` des pages déjà sur WP : les lancer.

## 4. Évaluer les nouveaux dossiers

Proposer un dossier seulement si plusieurs articles différents convergent vers une même question durable. Création : `python tools/new_article.py create --type dossier --theme <THEME> --dossier-dir <Nom>_Dossier --title "…" …` (→ `03_Dossiers/<Theme>/<Nom>_Dossier/`, type `DOSSIER`, `dossier-hebdomadaire`). Sinon : noter la proposition dans le rapport.

## 5. Textes fondateurs

Repérer les penseurs/concepts fréquemment nécessaires. Décider : TF existants (grep `04_Textes_fondateurs/Auteurs/` + index type `TF`), à créer, à relier aux nouveaux articles.
Création (0 à 2 par mois) : `python tools/new_article.py create --type texte-fondateur --theme <THEME> --title "…" …` (posture Comprendre, `04_Textes_fondateurs/Auteurs/`, `textes-fondateurs`), ~900–1600 mots, liens vers les articles du mois. Règles détaillées : `00_Systeme/Instructions_editoriales_officielles.md`.

## 6. Sentier du Savoir

Ne pas transformer chaque actualité en Sentier. Chercher la **compétence intellectuelle générale** que le mois révèle (crises complexes → cartographier un système ; controverses statistiques → lire des chiffres ; débats contradictoires → comparer des arguments ; problèmes de sources → hiérarchiser les sources).

Identifier fondamentaux disponibles / à enrichir / éventuels nouveaux (à **proposer** seulement : pas de 11e fondamental sans accord humain).

Atelier (0 à 2 par mois), règles de l'ancienne routine conservées (`.claude/skills/routine-triptyque/workflow.md` §2 SENTIER et §3) :
- fondamental parent via `00_Systeme/Manifests/sentier_fondamentaux.csv` (jamais `wiki-du-phare`) ;
- création : `python tools/new_article.py create --type atelier --theme <THEME> --fondamental-id <ID> --pillar <pilier> --title "…" …` (dossier `05_Sentier/Etape_NN_…`, en-tête `Type Sentier : atelier`, `Fondamental lie (ID)`, `Fondamental numero`, tags `atelier-sentier`/`fondamental-<ID>` calculés) ;
- mini-cas ancré sur des articles **réels** du mois, ≥ 2 sources nommées, chaque item de grille appliqué ;
- rotation d'étape + diversité de titre ;
- ligne dans `## Ateliers` du fondamental parent (`02_Fonds/…`) en local uniquement — **jamais** de push WP sur `02_Fonds/` (refresh réservé à l'éditeur, à signaler dans le rapport) ;
- `--refresh-body` autorisé seulement sur l'atelier `05_Sentier/…`.

## 7. Synthèse mensuelle (si le mois la justifie)

Titre : `Ce que l'actualité du mois nous a appris sur [thème]`. Relier plusieurs événements, prendre de la hauteur, intégrer les questions étudiées, montrer ce qui reste incertain, renvoyer vers dossiers et Sentier. **Pas** un résumé chronologique.
Création : `python tools/new_article.py create --type synthese-mensuelle --theme <THEME> --title "…" --tags "<concept>;…" …` (→ `06_Syntheses/Mensuelles/`, `SYNTHESE`, `cycle`, tags `synthese-mensuelle`, `question-du-phare`).

## 8. Auditer la navigation

Pour les articles du mois (et ceux reliés) : liens vers article précédent, question suivante, dossier, texte fondateur, Sentier. Repérer les articles isolés. **Proposer** les liens à ajouter dans le rapport ; ne modifier un article publié que pour ajouter un lien manquant évident, puis `--refresh-body`.

## 9. Équilibre éditorial

Répartition du mois par thème (`ECON`, `POL`, `MONDE`, `TECH`, `CLIMAT`, `SCIENCE`, `CULTURE` — taxonomie actuelle) via l'index. Identifier les sous-représentés, sans viser l'égalité.

## 10. Préparer le mois suivant → mémoire

- §5 : condenser le mois clos (5–10 lignes) + lien vers le rapport ; déplacer l'ancien §4 ici.
- §1 : retirer les lignes du mois clos si le tableau dépasse ~60 lignes (elles sont condensées en §5).
- §4 : nouveau cap — dossiers prioritaires (2–4), questions ouvertes, penseurs utiles (sans obligation), fondamentaux Sentier à développer, actualités à surveiller, catégories sous-représentées.

## Publication

Chaque production (synthèse, TF, atelier, dossier) est créée par `new_article.py create` (ID + ligne d'index, jamais d'écriture manuelle de l'index), rédigée, puis `python tools/new_article.py stage <ID>` (un dossier `07_A_Publier/<date>_<slug>/` **par article** ; `stage` lance le contrôle v3 (`validate_index_editorial.py --ids`) : s'il est KO, corriger le fichier ou la ligne d'index et relancer — jamais `--force` en routine.), puis
```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder --force
```

## Rapport mensuel

Écrire `06_Syntheses/Rapports_mensuels/YYYY-MM.md` (phénomènes, dossiers, TF, Sentier, navigation — liens à ajouter, équilibre, cap) puis résumer à l'utilisateur :

```
Routine mensuelle — [mois]
Publiés : synthèse / TF / ateliers / dossiers (URLs)
Propositions en attente : nouveaux dossiers, nouveaux fondamentaux, liens internes
Cap du mois suivant : …
À faire manuellement : vérifier WP
```

> Le quotidien produit les briques. L'hebdomadaire crée les connexions. Le mensuel construit l'architecture.
