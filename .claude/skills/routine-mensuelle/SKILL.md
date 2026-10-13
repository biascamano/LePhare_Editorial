---
name: routine-mensuelle
description: Routine mensuelle Le Phare, en deux parties lancées séparément par l'orchestrateur — A. rétro mensuelle interne (bilan, audit de navigation et d'équilibre, révision du Radar, cap du mois suivant, décisions) ; B. consolidation du patrimoine (dossiers, textes fondateurs, ateliers du Sentier, synthèse mensuelle). Déclenché par « routine phare » (via tools/phare.py), ou en secours par « routine mensuelle » ou /routine-mensuelle.
---

# Routine mensuelle — rétro et architecture

**A. Rétro mensuelle** : « Qu'avons-nous appris ce mois-ci, et quel est le cap ? » (interne).
**B. Consolidation** : « Qu'est-ce que tout cela construit durablement dans Le Phare ? » (publications).

Deux activités de l'orchestrateur (`plan.md` D22), sur le mois précédent : `retro_mensuelle` d'abord, `consolidation` ensuite (une séance chacune). En secours, sans orchestrateur : `routine mensuelle` = A puis B. Elle ne produit pas l'article du jour.

---

## A. Rétro mensuelle

Fichier unique : `06_Syntheses/Retros/<YYYY-MM>_retro_mensuelle.md`. Il remplace l'ancien rapport mensuel (`06_Syntheses/Rapports_mensuels/`, conservé jusqu'à 2026-09).

### A1. Rassembler

```bash
python tools/phare.py contexte retro_mensuelle --periode <YYYY-MM>
python tools/build_catalogue.py
```
Le contexte liste les séances, les publications par thème et type, les rétros hebdomadaires qui chevauchent le mois (faites ou non) et les **jours d'activité sans rétro hebdomadaire** : ceux-là sont examinés directement (traces, index), sans reconstituer de rétro hebdomadaire. Lire les rétros hebdomadaires du mois (sections `## Rétro` seulement), `00_Systeme/Catalogue_editorial.md` (équilibre, lacunes), `00_Systeme/Radar_editorial.md` entier, mémoire §1 (lignes du mois), §2, §3, §4 (cap précédent).

### A2. Écrire la rétro

```markdown
# Rétro mensuelle YYYY-MM

## Décisions précédentes et mise en œuvre
(décisions ouvertes de la dernière rétro, hebdomadaire ou mensuelle : état, preuve ; cap §4 précédent : tenu ou non)

## Résultats du mois
(objectifs quotidiens par semaine ; publiés, brouillons et motifs, incidents, reports ; contrôle prépublication ; soutenabilité du rythme ; Fils du Phare)

## Grands phénomènes
(sujets revenus sur des événements réellement différents — matière de la consolidation)

## Navigation
(articles du mois isolés : liens manquants vers précédent, question suivante, dossier, TF, Sentier ; liens proposés)

## Équilibre éditorial
(répartition par thème ECON, POL, MONDE, TECH, CLIMAT, SCIENCE, CULTURE et par type ; sous-représentés, sans viser l'égalité)

## Problèmes et angles morts

## Ajustements proposés

## Cap du mois suivant
(dossiers prioritaires 2–4, questions ouvertes, penseurs utiles sans obligation, fondamentaux Sentier à développer, actualités à surveiller, catégories sous-représentées ; consolidation attendue : dossiers, TF, ateliers, synthèse — 0 est une réponse valide)

## Décisions

| N° | Décision | Priorité | Échéance | État |
|---|---|---|---|---|
| D-YYYY-MM-1 | … | bloquante / importante / normale | … | à faire / en cours / faite / abandonnée |
```
Mêmes règles de décisions que la rétro hebdomadaire (`routine-hebdomadaire` B5) : report des ouvertes avec leur état, « bloquante » suspend la production, « importante » est affichée à chaque séance.

Navigation : ne modifier un article publié que pour un lien manquant évident, puis `python tools/wp_refresh_body.py "<chemin>"` (jamais `02_Fonds/`). Le reste est proposé.

### A3. Mémoire et Radar

- §5 : condenser le mois clos (5–10 lignes, lien vers la rétro mensuelle) ; y déplacer l'ancien §4. Les sessions de rénovation du mois y figurent (d'après les `Remarques` de l'index).
- §1 : retirer les lignes du mois clos si le tableau dépasse ~60 lignes.
- §4 : le cap (copie de « Cap du mois suivant »).
- Radar (`plan.md` D14) : retirer le réalisé ; tenir les blocs 4–5 (TF, applications structurantes, dossiers, ateliers) ; archiver ce qui est resté sans suite depuis plus d'un mois ; vider les archives de plus de trois mois ; P1 = mois suivant ; ≤ 30 entrées actives ; date « État au ».

### A4. Clore

`python tools/verify_publication.py --days 31` (erreur de tag ou `?p=` → `--fix` puis relancer ; brouillons du mois : les lister, pas de `--publish-drafts`), `python tools/build_etat_courant.py`, puis `close retro_mensuelle --statut termine` (`phare.py` exige « Cap du mois suivant » et la table des décisions).

---

## B. Consolidation

Partir de la rétro mensuelle du même mois (phénomènes, cap, navigation) : ne pas refaire l'analyse. Les créations lourdes sont limitées à ce que le mois justifie — **0 est une réponse valide** (clore alors `termine`, avec le motif en note).

### B1. Dossiers existants (`03_Dossiers/<Theme>/`)

Question centrale encore pertinente ? articles à ajouter, sous-thèmes à réorganiser, manques, page principale à créer ou mettre à jour ? Modifier les `.md` locaux, puis `python tools/build_hubs.py` (régénère `## Liens internes du dossier` depuis l'index ; traiter les avertissements `!`) et lancer les `wp_refresh_body.py` qu'il affiche.

### B2. Nouveaux dossiers

Seulement si plusieurs articles **réellement différents** convergent vers une même question durable : `python tools/new_article.py create --type dossier --theme <THEME> --dossier-dir <Nom>_Dossier --title "…" …`. Sinon : proposition dans le rapport.

### B3. Textes fondateurs (0 à 2)

Radar bloc 4 et lacunes du catalogue. Vérifier l'existant (`04_Textes_fondateurs/Auteurs/`, index type `TF`). `python tools/new_article.py create --type texte-fondateur --theme <THEME> --title "…" …` : posture Comprendre, ~900–1600 mots, liens vers les articles du mois, règles de `00_Systeme/Instructions_editoriales_officielles.md`.

### B4. Ateliers du Sentier (0 à 2)

Chercher la **compétence intellectuelle générale** que le mois révèle (cartographier un système, lire des chiffres, comparer des arguments, hiérarchiser des sources). Radar bloc 5. Pas de 11e fondamental (proposition seulement). Règles de l'ancienne routine (`.claude/skills/routine-triptyque/workflow.md` §2 SENTIER et §3) :
- fondamental parent via `00_Systeme/Manifests/sentier_fondamentaux.csv` (jamais `wiki-du-phare`) ;
- `python tools/new_article.py create --type atelier --theme <THEME> --fondamental-id <ID> --pillar <pilier> --title "…" …` ;
- mini-cas ancré sur des articles **réels** du mois, ≥ 2 sources nommées, chaque item de grille appliqué ; rotation d'étape, diversité de titre ;
- ligne dans `## Ateliers` du fondamental parent (`02_Fonds/…`) **en local uniquement** — jamais de push WP sur `02_Fonds/` (refresh éditeur, à signaler) ;
- refresh WP autorisé seulement sur l'atelier `05_Sentier/…`.

### B5. Synthèse mensuelle (si le mois la justifie)

Titre : `Ce que l'actualité du mois nous a appris sur [thème]`. Relier plusieurs événements, prendre de la hauteur, montrer ce qui reste incertain, renvoyer vers dossiers et Sentier. **Pas** un résumé chronologique. `python tools/new_article.py create --type synthese-mensuelle --theme <THEME> --title "…" --tags "…" …`.

### B6. Contrôler et publier (chaque production)

Titres : `--title` sans préfixe (`plan.md` D16). Chaque production : `create`, rédaction, `python tools/new_article.py stage <ID>` (un dossier de transit par article ; KO → corriger, jamais `--force` sur `stage`), puis **contrôle prépublication** (`00_Systeme/Controle_prepublication.md` : auto-contrôle + agent `relecteur-prepublication`) :
- PUBLIER → `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder --force` ;
- CORRIGER (au moins un défaut bloquant) → 2 cycles au plus, cycle 2 ciblé sur les passages modifiés ; défauts mineurs seuls : corrigés et tracés, sans nouveau cycle ;
- BROUILLON → même commande avec `--no-publish-final` ; passer à la production suivante (une production en brouillon ne se remplace pas).

Signaux de vie : `phare.py etape consolidation --etape redaction --ids <IDs créés>` après chaque `create`, `--etape wp` avant chaque `daily_run`.

### B7. Mémoire, vérification, clôture

- §1 : `python tools/memoire_append.py <ID> [--penseur "…"] [--sentier <ID>]` pour chaque production publiée.
- Radar : retirer les entrées des blocs 4–5 réalisées.
- `python tools/verify_publication.py --days 31` (`--fix` si tag ou `?p=`), puis `python tools/build_catalogue.py` et `python tools/build_etat_courant.py`.
- Ajouter à la rétro mensuelle une section `## Consolidation` (productions, IDs, statuts, propositions en attente) — **sans** modifier ses décisions.
- `close consolidation --statut termine --ids <IDs> --note "<n publiés, n brouillons>"`.

---

## Rapports

```
Rétro mensuelle — [mois] (fichier)
Décisions précédentes : … · Cap : … · Nouvelles décisions : … (bloquantes : …)
Vérification : N articles, X erreurs, Y avertissements
```
```
Consolidation — [mois]
Publiés : synthèse / TF / ateliers / dossiers (URLs) · Brouillons : … (motifs)
Propositions en attente : nouveaux dossiers, nouveaux fondamentaux, liens
À faire manuellement : vérifier WP ; refresh éditeur des fondamentaux 02_Fonds/ modifiés
```

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `cd … &&`, `;`, `|`, ni `python -c` multiligne. Read / Grep / Edit plutôt que `cat` / `grep` / `sed`. URLs de l'index : `python tools/index_lookup.py <IDs>`. Refresh WP : `python tools/wp_refresh_body.py "<chemin>"` ; ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande.

> Le quotidien produit les briques. L'hebdomadaire crée les connexions. Le mensuel construit l'architecture.
