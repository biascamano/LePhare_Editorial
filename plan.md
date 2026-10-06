# Plan — Système éditorial Le Phare en trois routines

> **Document de référence pour toutes les évolutions** du système de routines.
> Créé le 2026-10-05. Toute évolution met à jour ce fichier (§13 Journal des évolutions) **dans le même changement** que le code / les skills.
> En cas d'écart entre ce plan et les fichiers réels (`.claude/skills/*`, `tools/*`, `CLAUDE.md`), **les fichiers réels font foi** : corriger le plan, ne pas « réparer » le code pour coller au plan sans décision explicite.

---

## Sommaire

1. Contexte et motivation
2. Principes directeurs
3. Décisions actées
4. Architecture d'ensemble
5. Routine quotidienne
6. Routine hebdomadaire
7. Routine mensuelle
8. Mémoire éditoriale partagée
9. Données, fichiers et métadonnées
10. Outillage technique (scripts)
11. Règles et interdits transverses
12. État d'avancement
13. Journal des évolutions
14. Plan de validation
15. Risques et points de vigilance
16. Backlog des évolutions envisagées
17. Procédure pour faire évoluer le système
18. Index des fichiers concernés
19. Rénovation du stock ancien

---

## 1. Contexte et motivation

### 1.1 Situation avant 2026-10-05 (« ère triptyque »)

- Une seule routine, `routine quotidienne`, produisait chaque jour un **triptyque** : ACTU + TF (texte fondateur) + SENTIER (atelier rattaché à un fondamental du Sentier du Savoir).
- Publication : `tools/daily_run.py --publish-existing` → `wp_push_draft.py` (brouillons WP) → `post_linking.py` (maillage « Dans ce triptyque ») → publication.
- Dernier triptyque : 2026-528 / 529 / 530 (2026-06-25).

### 1.2 Problèmes constatés

- Routine lourde (3 articles/jour) : coût en tokens, temps, risque de TF et d'ateliers artificiels.
- Aucune consolidation : pas de lien entre les jours, pas de fil rouge, pas de vue d'ensemble des dossiers ni du Sentier.
- Aucune mémoire de « où en est » le fil éditorial : chaque routine repartait de zéro (lecture de l'index uniquement).

### 1.3 Sources de la refonte

- `ROUTINE QUOTIDIENNE.docx` (9 étapes), `ROUTINE HEBDOMADAIRE.docx` (7 étapes), `ROUTINE MENSUELLE.docx` (10 étapes), à la racine du dépôt.
- Consigne : sortir de la quotidienne tout ce qui relève de la consolidation ; trois routines légères et spécialisées ; **un seul fichier de mémoire éditoriale** partagé.
- `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` (racine du dépôt) : mission, architecture en cinq niveaux, exigences de l'article d'actualité, critères de la Question du Phare, usage des penseurs. Intégré en v3.7 (§2.1–§2.2, §5.6–§5.8). **Le docx s'arrête au milieu du §5 « Place de Simone Weil »** : la suite reste à fournir (T12).

---

## 2. Principes directeurs

### 2.1 Mission (socle)

Le Phare Info pratique un *slow journalism* : l'actualité n'est pas seulement racontée, elle sert de **point de départ** pour comprendre le monde, poser des questions durables et transmettre des outils pour penser par soi-même. Transformer progressivement l'information en compréhension, la compréhension en connexions, les connexions en savoir durable.

### 2.2 Les cinq niveaux et leur routine

Parcours : **Actualité → Question du Phare → Pensée / Texte fondateur → Dossier → Sentier du Savoir**.

| Niveau | Fonction | Question principale | Produit par |
|--------|----------|---------------------|-------------|
| 1 Actualité | Voir | Que vient-il de se passer ? | Quotidienne (article A) |
| 2 Question du Phare | Interroger | Qu'est-ce que cet événement révèle au-delà de lui-même ? | Quotidienne (article Question, quand c'est le meilleur prochain article — D12) ; Fil du Phare (hebdo) |
| 3 Pensée / Texte fondateur | Regarder autrement | Quelle pensée peut nous aider à mieux comprendre ce problème ? | Mensuelle (TF) ; quotidienne occasionnelle (D) ; grille de lecture dans B |
| 4 Dossier | — (non détaillé par le socle) | — | Mensuelle |
| 5 Sentier du Savoir | — (non détaillé par le socle) | — | Mensuelle (ateliers) |

### 2.3 Routines

| Routine | Question | Rôle |
|---------|----------|------|
| Quotidienne | « Quel est le meilleur prochain article du Phare ? » | Produire **les briques** : un article par jour, type choisi après le sujet (D12) |
| Hebdomadaire | « Qu'est-ce que nos articles racontent ensemble ? » | Créer **les connexions** |
| Mensuelle | « Qu'est-ce que tout cela construit durablement dans Le Phare ? » | Construire **l'architecture** |

Principes transverses :

1. **Une routine = une responsabilité.** Une routine ne fait pas le travail d'une autre (ex. pas d'atelier Sentier au quotidien).
2. **Mémoire avant action.** Chaque routine lit d'abord l'état éditorial, et l'écrit en dernier. La quotidienne lit la vue compressée (`Etat_editorial_courant.md` + `Radar_editorial.md`, D13–D14) ; l'hebdomadaire et la mensuelle lisent `00_Systeme/Memoire_editoriale.md`.
3. **La mémoire pointe, l'index détaille.** `index_editorial.csv` reste la source de vérité technique (IDs, slugs, URLs, tags) ; la mémoire porte le sens (questions, fils, cap).
4. **Autonomie totale.** Aucune question intermédiaire ; rapport final court ; vérification humaine sur WordPress.
5. **Slow journalism.** Qualité selon `00_Systeme/Instructions_editoriales_officielles.md` ; pas de sensationnel ; l'article doit pouvoir être lu seul.
6. **Rien d'artificiel.** Texte fondateur, dossier, atelier ou synthèse seulement si le contenu le justifie ; « 0 ce mois-ci » est une réponse valide. Le type d'article quotidien découle du sujet, jamais d'un équilibrage (D12).
7. **Rédaction par Claude**, pas par API/Ollama (sauf demande explicite `api`).
8. **Rétrocompatibilité.** L'ancienne routine reste disponible (`routine triptyque`).
9. **Les penseurs sont des grilles de lecture, jamais des arguments d'autorité** (§5.8).

---

## 3. Décisions actées

| # | Sujet | Décision | Date |
|---|-------|----------|------|
| D1 | TF et atelier Sentier quotidiens | **Retirés** du quotidien → routine mensuelle. Le type D « Texte fondateur » reste possible au quotidien **occasionnellement**, s'il est nécessaire pour comprendre les articles précédents. | 2026-10-05 |
| D2 | Taxonomie | **Conservée** : types index `ACTU`, `TF`, `SENTIER`, `FOND`, `DOSSIER`, `SYNTHESE` ; thèmes `TECH`, `CLIMAT`, `ECON`, `SCIENCE`, `POL`, `CULTURE`, `MONDE`. Les catégories proposées par le docx mensuel ne sont **pas** ajoutées. | 2026-10-05 |
| D3 | Fil du Phare (hebdo) et synthèse mensuelle | **Publiés sur WordPress**, catégorie existante `cycle` (id 97, B1), type index `SYNTHESE`. | 2026-10-05 |
| D4 | Déclenchement | **Manuel** (prompt ou slash command). Pas de cron. | 2026-10-05 |
| D5 | Ancienne routine | Conservée sous `routine triptyque` / `triptyque` / `/routine-triptyque`. | 2026-10-05 |
| D6 | Mémoire | Un seul fichier : `00_Systeme/Memoire_editoriale.md`, sections attribuées par routine (§8). | 2026-10-05 |
| D7 | Docs `00_Systeme/Routine_quotidienne*.md` | **Non déplacés** (trop référencés) ; bandeau « ARCHIVÉ » en tête. | 2026-10-05 |
| D8 | Fondamentaux parents `02_Fonds/` | Inchangé : **jamais** de push WP par une routine ; mise à jour locale de `## Ateliers` uniquement, refresh WP par l'éditeur humain. | rappel |
| D9 | Paire quotidienne | ~~La routine quotidienne produit deux articles le même jour (A Actualité + B Question).~~ **Remplacée par D12** (2026-10-06) ; la paire reste disponible sur demande (`routine quotidienne — paire`). | 2026-10-05 |
| D10 | Socle éditorial | `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` fait référence pour la ligne éditoriale (niveaux, exigences, critères de question, usage des penseurs) ; `Instructions_editoriales_officielles.md` reste la référence de qualité rédactionnelle. En cas d'écart entre les deux : signaler, ne pas trancher seul. | 2026-10-05 |
| D11 | Partage des rôles A / B | L'actualité se recentre sur les faits (certain / incertain / causes / conséquences / acteurs / interprétations) et se termine par la question ; l'analyse réflexive et le penseur passent dans B. Pas de redite : B rappelle l'actualité en un paragraphe et renvoie vers A. | 2026-10-05 |
| D12 | Pilotage éditorial adaptatif (V5) | **Un article par jour** : le meilleur prochain article du Phare. Ordre de lecture : état immédiat → Radar → cap → actualité. 5 candidats au plus (1–3 issus de la veille), notés Faible/Moyen/Fort sur importance actuelle, continuité, durabilité, valeur de compréhension, nouveauté ; priorité à notes proches : actualité majeure → suite naturelle → connexion → structurant. Le **type est choisi après le sujet** (Actualité, Question, Application, exceptionnellement Texte fondateur) ; pas de série rigide ni d'équilibrage artificiel. La question finale d'une Actualité entre au Radar (bloc 2). Remplace D9. | 2026-10-06 |
| D13 | Couches de compression | `00_Systeme/Etat_editorial_courant.md` (≤ 50 lignes), **généré** par `tools/build_etat_courant.py` depuis la mémoire §1–§4 et le Radar, jamais édité à la main. La quotidienne ne lit ni le catalogue ni la mémoire entière. Sources de vérité inchangées : mémoire (sens) et index (technique). | 2026-10-06 |
| D14 | Radar éditorial | `00_Systeme/Articles_a_creer.md` → `00_Systeme/Radar_editorial.md` : `\| P \| Type potentiel \| Sujet / Question \| Origine \| Statut \|`, ≤ 30 entrées actives ; statuts `approfondir`, `relier`, `à échéance (…)`, `conserver`, `archivé` ; blocs 1 Suites, 2 Questions, 3 Connexions, 4 Structurants, 5 Dossiers et Sentier, Archives. Quotidienne : retire le réalisé, ajoute la question finale d'une Actualité. Hebdomadaire : comité éditorial (tri, fusion, priorités, blocs 1–3). Mensuelle : blocs 4–5, archivage. | 2026-10-06 |
| D15 | Vérification de fin de routine et visibilité | Chaque routine se termine par `tools/verify_publication.py` (articles des 7 derniers jours) : liens internes, maillage aller-retour, navigation, URL nues, statut WP, tag `a-la-une`. **Un article publié sans le tag `a-la-une` est invisible sur le site** : `new_article.py` l'ajoute à `Tags_WP` (hors quota de 8 tags), `wp_push_draft.py` le force à chaque push. `--fix` corrige tag et liens `?p=` ; `--publish-drafts` ne publie que des brouillons désignés ou récents, jamais un ancien brouillon par défaut. | 2026-10-06 |
| D16 | Préfixe de titre par type | `new_article.py` préfixe le titre de tout type **sauf** l'Actualité : « Question du Phare - », « Application du Phare - », « Texte fondateur - », « Le Fil du Phare - », « Synthèse du mois - », « Dossier du Phare - », « Sentier du Savoir - ». Tiret court plutôt que deux-points (beaucoup de titres en contiennent déjà) ; préfixe déjà présent normalisé, jamais doublé. Slug sans préfixe (sauf Fil du Phare, historique). Appliqué rétroactivement aux 8 articles non-Actualité de 2026-531…552, 559, 560 (`wp_refresh_body.py --title`) ; les plus anciens gardent leur titre. | 2026-10-06 |
| D17 | Rénovation du stock ancien | Pas de réécriture globale : tri en trois niveaux (Trier / Remettre à niveau / Refaire) calculé par `tools/build_inventaire_renovation.py` (§19). Un article rénové garde **son ID et son URL**. Hors périmètre : `02_Fonds/` (éditeur humain), pages `wiki-du-phare`, articles déjà au format actuel. Toute copie locale marquée « tronquée » est **resynchronisée depuis WordPress avant retouche** : un refresh depuis le local écraserait la version en ligne, plus longue. Rénovation en sessions dédiées, jamais dans une routine éditoriale. | 2026-10-06 |

---

## 4. Architecture d'ensemble

```
                 ┌──────────────────────────────────────────┐
                 │  00_Systeme/Memoire_editoriale.md        │
                 │  §1 Journal  §2 Fils  §3 Fil du Phare    │
                 │  §4 Cap du mois  §5 Archives mensuelles  │
                 │  + 00_Systeme/Radar_editorial.md (≤ 30)  │
                 └──────┬──────────────▲──────────────▲─────┘
       build_etat_courant.py           │              │
                        ▼              │              │
     Etat_editorial_courant.md (≤ 50 l.)              │
     lit État courant + Radar          │ lit §1,2,4   │ lit §1-4 + catalogue
     écrit §1 (memoire_append), Radar  │ écrit §1,2,3 │ écrit §1(archive),4,5
                                       │ + Radar 1–3  │ + Radar 4–5, archives
     ┌───────────────────────┐  ┌──────┴────────────┐  ┌┴──────────────────────┐
     │ QUOTIDIENNE           │  │ HEBDOMADAIRE      │  │ MENSUELLE             │
     │ 1 article/jour, type  │  │ Fil du Phare      │  │ Dossiers, TF, ateliers│
     │ choisi après le sujet │  │ comité du Radar   │  │ catalogue, archivage  │
     └─────────┬─────────────┘  └────────┬──────────┘  └──────────┬────────────┘
               │ index (append_rows_to_index) + 07_A_Publier/<dossier>/
               ▼
     tools/daily_run.py --publish-existing … --keep-publish-folder [--force]
       → wp_push_draft.py → post_linking.py (1 ou 3 articles) → publication WP
       (variante paire A+B : deux dossiers de transit, deux runs — §5.9)
```

### 4.1 Déclencheurs

| Prompt | Slash command | Skill |
|--------|---------------|-------|
| `routine quotidienne` (+ `— sujet : …, thème X` / `— brouillons seulement` / `type actualite|application|texte fondateur` = type imposé / `type question — sur <ID>` = Question sur la question finale de `<ID>` / `paire` = Actualité + Question le même jour) | `/routine-quotidienne` | `.claude/skills/routine-quotidienne/SKILL.md` |
| `routine hebdomadaire`, `fil du phare` | `/routine-hebdomadaire` | `.claude/skills/routine-hebdomadaire/SKILL.md` |
| `routine mensuelle` | `/routine-mensuelle` | `.claude/skills/routine-mensuelle/SKILL.md` |
| `routine renovation` (+ `— lot 2|3` / `— <IDs>` / `— à blanc`) | `/routine-renovation` | `.claude/skills/routine-renovation/SKILL.md` (D17, §19) |
| `routine triptyque`, `triptyque` | `/routine-triptyque` | `.claude/skills/routine-triptyque/SKILL.md` + `workflow.md` |
| `… api` | — | Exception : `editorial_pipeline.py --use-api-llm` |

### 4.2 Cadence recommandée (non automatisée)

- Quotidienne : jours ouvrés.
- Hebdomadaire : fin de semaine (vendredi/samedi), **après** la quotidienne du jour si les deux tournent le même jour.
- Mensuelle : premier jour ouvré du mois suivant (porte sur le mois clos).

---

## 5. Routine quotidienne

Skill : `.claude/skills/routine-quotidienne/SKILL.md`.

### 5.1 Périmètre

- **Fait** : lecture de l'état (État courant, Radar), veille, candidats et arbitrage, choix du sujet **puis** du type (D12), rédaction d'**un** article, navigation, index, publication, lien retour vers l'article d'origine, ligne de mémoire §1 (`memoire_append.py`), retrait/ajout au Radar, régénération de l'État courant.
- **Ne fait pas** : triptyque, atelier Sentier, restructuration de dossier, synthèse de la semaine/du mois, tri du Radar, lecture du catalogue ou de la mémoire entière, modification de `02_Fonds/` ou `03_Dossiers/`, écriture des §2–§5 de la mémoire.

### 5.2 Étapes

| # | Étape | Détail |
|---|-------|--------|
| 1 | Regarder derrière | `Etat_editorial_courant.md` (régénéré s'il a plus de 7 jours). |
| 2 | Regarder devant | `Radar_editorial.md` : échéances atteintes, suites, questions, connexions. |
| 3 | Regarder autour | Veille 24–72 h ; réduite à une vérification si le Radar a déjà un candidat fort. |
| 4 | Candidats et arbitrage | ≤ 5 (A nouvelle actualité, B suite, C connexion, D structurant), notés F/M/F sur 5 critères (D12). |
| 5 | Type | Actualité, Question, Application, exceptionnellement TF — après le sujet. |
| 6 | Fiche de préparation | Une seule Question du Phare ; ≤ 5 articles internes vérifiés (`index_lookup.py --search/--type/--theme/--dossier`). |
| 7 | Rédiger | §5.6 (Actualité), §5.7 (Question), Application, TF. |
| 8 | Navigation | §5.4. |
| 9 | Publier | `new_article.py create` / `stage`, `daily_run.py --publish-existing … --keep-publish-folder` ; lien retour dans l'article d'origine + `wp_refresh_body.py`. |
| 10 | Mémoriser | `memoire_append.py <ID>` ; Radar (retirer le réalisé, ajouter la question d'une Actualité) ; `build_etat_courant.py`. |

Indicateur de réussite : « l'article publié aujourd'hui était-il réellement le meilleur prochain article du Phare ? »

### 5.3 Correspondance des types

| Type article | Code index | Dossier canonique | Catégorie WP | Tag de type |
|--------------|-----------|-------------------|--------------|-------------|
| Actualité | `ACTU` | `01_Actualites/<Theme>/` | `actualites` | `type-actualite` |
| Question du Phare | `ACTU` | `01_Actualites/<Theme>/` | `actualites` | `type-question` |
| Application | `ACTU` | `01_Actualites/<Theme>/` | `actualites` | `type-application` |
| Texte fondateur (occasionnel) | `TF` | `04_Textes_fondateurs/Auteurs/` | `textes-fondateurs` | `type-texte-fondateur` |

Tag commun : `question-du-phare`. Dossiers par thème : `Technologie_IA`, `Climat_Transition`, `Economie_Finance`, `Science_Sante`, `Politique_Societe`, `Culture` (MONDE → `Politique_Societe`).

### 5.4 Navigation finale (remplace « Dans ce triptyque »)

```markdown
---

**Repères de sources**

- Source : [libellé](url)

**La question suivante**

[Question du Phare]

**Pour aller plus loin**

- [Article précédent ou dossier](url)

**Sur le Sentier du Savoir**

- [Fondamental](url_canonique)
```

Liens internes : uniquement des URLs réelles lues dans `index_editorial.csv` / `sentier_fondamentaux.csv` (jamais `wiki-du-phare`).

### 5.5 Rapport final

Candidats (sorte, notes) ; choix (titre, ID, type, URL) ; pourquoi ce sujet, pourquoi ce type ; Question du Phare ; liens retour ; Radar retiré/ajouté ; idée d'image (légende + alt) ; rappel « vérifier WordPress ».

### 5.6 Article A — Actualité (« Voir »)

Factuel, sourcé, accessible, contextualisé, non sensationnaliste. Il répond notamment à :

- Que s'est-il passé ?
- Que savons-nous avec certitude ? Que reste-t-il incertain ?
- Quelles sont les causes ? Quelles sont les conséquences ?
- Quels acteurs sont concernés ?
- Quelles interprétations s'opposent ?

Intertitres adaptés au sujet (pas de plan fixe). Il ne se termine pas sur une simple synthèse : il fait **émerger** la Question du Phare des faits. Pas de section penseur (elle passe dans B, D11).

### 5.7 Article B — Question du Phare (« Interroger »)

Question principale : *qu'est-ce que cet événement révèle au-delà de lui-même ?*

Critères de la question (socle) : claire ; ouverte ; durable ; compréhensible ; directement issue des faits ; réutilisable dans d'autres domaines ; profonde sans devenir artificiellement philosophique.

Exemple du socle : actualité « Black-out ibérique : que s'est-il passé ? » → question « Jusqu'où une société peut-elle rendre ses citoyens dépendants d'une infrastructure sans leur garantir de solutions de continuité ? ».

Structure indicative (intertitres à adapter) :

1. **Le point de départ** — l'actualité en un paragraphe, lien vers A.
2. **Pourquoi cette question** — ce que l'événement révèle au-delà de lui-même.
3. **Ailleurs, la même question** — au moins deux autres domaines ou situations réels où elle se pose (articles du Phare de préférence, URLs de l'index).
4. **Une pensée pour regarder autrement** — si pertinent (§5.8) : tester une intuition, puis la confronter aux faits.
5. **Ce qui résiste** — objections, limites, ce que la question ne permet pas de trancher.
6. **Ce que nous pouvons en retenir** — outils pour penser par soi-même.
7. **La question laissée ouverte** — prolongement. Elle n'appelle **pas** automatiquement un nouvel article : elle alimente la mémoire, et l'hebdo choisit les fils à poursuivre.

Titre : la question elle-même ou une formulation courte qui la porte. En-tête : `Type article : Question`, `Question du Phare` = la question traitée, `Article precedent (ID)` = ID de A, `Articles lies` = A + liens de la section 3.

### 5.8 Penseurs et textes fondateurs comme grilles de lecture

- Mobilisés seulement s'ils apportent réellement quelque chose ; jamais pour dire au lecteur quoi penser.
- Jamais d'argument d'autorité : pas de « Simone Weil avait raison », mais « cette situation permet de tester une intuition de Simone Weil », puis confrontation aux faits.
- Repères du socle (non limitatifs) : Simone Weil (obligation, besoins humains, enracinement, attention, travail, responsabilité, force, vérité) ; Hannah Arendt (pouvoir, violence, responsabilité, espace public, totalitarisme) ; Jacques Ellul (technique, autonomie du système technique, propagande) ; Albert Camus (mesure, révolte, responsabilité) ; Hartmut Rosa (accélération, aliénation, résonance) ; Tocqueville (démocratie, individualisme, centralisation) ; Ivan Illich (institutions, autonomie, contre-productivité) ; David Collingridge (dilemme du contrôle technologique) ; John Ruskin (patrimoine, transmission, restauration) ; Thomas Schelling (stratégie, signal, dissuasion).
- Lien vers un TF seulement s'il figure dans l'index ; sinon nommer sans lien et le proposer à la mensuelle.
- Place particulière de Simone Weil : à compléter (socle tronqué, T12).

### 5.9 Publication de la paire (variante `paire`, mécanique transitoire)

`post_linking.py` refuse un dossier de 2 articles (1 ou 3 seulement) : la paire passe par **deux** dossiers de transit et deux runs, sans changement de code.

1. `new_article.py create` A puis B ; rédiger A ; `stage` A ; `daily_run.py --publish-existing <transit A> --keep-publish-folder [--no-publish-final]`.
2. Rédiger B avec l'URL de A lue dans l'index ; `stage` B ; `daily_run.py … <transit B> --keep-publish-folder --force [--no-publish-final]`.
3. Remplacer dans A la question nue de « La question suivante » par le lien vers B (URL lue dans l'index) ; `wp_refresh_body.py` sur A.

Cible : mode paire intégré (B16).

---

## 6. Routine hebdomadaire

Skill : `.claude/skills/routine-hebdomadaire/SKILL.md`.

### 6.1 Périmètre

- **Fait** : relecture de la semaine, connexions, **une** grande question, article « Le Fil du Phare », audit des fils, pistes de la semaine suivante, mise à jour §1/§2/§3.
- **Ne fait pas** : recherche du sujet du jour, création/réorganisation de dossier, TF, atelier Sentier.

### 6.2 Étapes

| # | Étape | Détail |
|---|-------|--------|
| 1 | Relire la semaine | §1 (7 derniers jours) + fichiers canoniques. **Moins de 3 articles → pas de Fil du Phare**, seulement étapes 5–7. |
| 2 | Connexions | Questions récurrentes, tensions, phénomène commun, contradictions, thèmes émergents. |
| 3 | Grande question | Une seule. |
| 4 | Le Fil du Phare | ~900–1400 mots ; sections : Cette semaine / Le lien invisible / La grande question / Un penseur pour regarder autrement (si pertinent) / Ce que ces événements nous apprennent / Ce que nous ne savons pas encore / Où poursuivre ? |
| 5 | Audit des fils | À poursuivre / à clôturer / à mettre de côté (+ condition de reprise) ; **5 fils actifs au plus**. |
| 6 | Semaine suivante — comité éditorial | 3 à 5 pistes, **pas** de programme fixe ; Radar blocs 1–3 : retirer le réalisé, fusionner, re-prioriser, archiver, ≤ 30 actives (D14). |
| 7 | Mémoire | §1 (`memoire_append.py`), §2, §3 (nouvelle ligne en haut) ; puis `build_etat_courant.py`. Rétro optionnelle via `00_Systeme/Retro_routine_hebdo_TEMPLATE.md`. |

### 6.3 Métadonnées du Fil du Phare

| Champ | Valeur |
|-------|--------|
| Titre | `Le Fil du Phare - [question]` (préfixe ajouté par `new_article.py`, D16) |
| Type index | `SYNTHESE` |
| Theme | thème dominant de la semaine |
| Type article | `Fil du Phare` |
| Fichier | `06_Syntheses/Fil_du_Phare/YYYY-NNN_SYNTHESE_<THEME>_fil-du-phare-<slug>_V1.md` |
| Catégorie WP | `cycle` (id 97) |
| Tags | `fil-du-phare`, `question-du-phare`, `synthese-hebdomadaire` + concepts |
| Articles liés | tous les IDs de la semaine |
| Slug | `fil-du-phare-<slug>` |
| Publication | `daily_run.py --publish-existing … --keep-publish-folder --force` |

---

## 7. Routine mensuelle

Skill : `.claude/skills/routine-mensuelle/SKILL.md`.

### 7.1 Périmètre

- **Fait** : analyse du mois, phénomènes, dossiers (mise à jour / création), TF (0–2), ateliers Sentier (0–2), synthèse mensuelle (si justifiée), audit de navigation, équilibre thématique, rapport mensuel, cap du mois suivant, archivage mémoire.
- **Ne fait pas** : article d'actualité du jour ; 11e fondamental Sentier (proposition seulement) ; push WP sur `02_Fonds/`.

### 7.2 Étapes

| # | Étape | Sortie |
|---|-------|--------|
| 1 | Examiner le mois | `build_catalogue.py` ; Radar entier ; mémoire §1–§4. |
| 2 | Grands phénomènes | Liste ; un dossier = plusieurs événements **réellement différents** autour d'un même problème. |
| 3 | Dossiers existants | Mise à jour `03_Dossiers/<Theme>/` ; `--refresh-body` si la page WP existe. |
| 4 | Nouveaux dossiers | Création (`DOSSIER`, catégorie `dossier-hebdomadaire`) ou proposition dans le rapport. |
| 5 | Textes fondateurs | 0–2 créations (`TF`, `04_Textes_fondateurs/Auteurs/`, `textes-fondateurs`) ; vérification de l'existant par grep + index. |
| 6 | Sentier du Savoir | Compétence intellectuelle du mois ; 0–2 ateliers (règles de `routine-triptyque/workflow.md` §2–§3) ; ligne `## Ateliers` du parent **en local** ; `--refresh-body` seulement sur `05_Sentier/…`. |
| 7 | Synthèse mensuelle | `Ce que l'actualité du mois nous a appris sur [thème]` ; `SYNTHESE`, `06_Syntheses/Mensuelles/`, catégorie `cycle`, tags `synthese-mensuelle`, `question-du-phare`. |
| 8 | Audit navigation | Articles isolés, liens manquants (proposés ; correction seulement si évidente). |
| 9 | Équilibre éditorial | Répartition par thème via l'index ; sous-représentés. |
| 10 | Mois suivant | Mémoire §5 (condensé + lien rapport), §1 (purge si > ~60 lignes), §4 (nouveau cap) ; Radar blocs 4–5 + archivage ; `build_catalogue.py` puis `build_etat_courant.py`. |

Rapport : `06_Syntheses/Rapports_mensuels/YYYY-MM.md` + résumé à l'utilisateur (publiés, propositions en attente, cap, actions manuelles dont refresh des `02_Fonds/` modifiés).

---

## 8. Mémoire éditoriale partagée

Fichier : `00_Systeme/Memoire_editoriale.md`.

### 8.1 Sections et propriété

| Section | Contenu | Écrit par | Lu par |
|---------|---------|-----------|--------|
| §1 Journal quotidien | Une ligne par article publié | Q (articles), H (Fil du Phare), M (synthèse + purge) | Q, H, M |
| §2 Fils éditoriaux | Actifs / mis de côté / clôturés | H | Q, H, M |
| §3 Fil du Phare | Une ligne par semaine (plus récente en haut) | H | Q, M |
| §4 Cap du mois | Dossiers prioritaires, questions ouvertes, penseurs, fondamentaux, actualités à surveiller, sous-représentés | M | Q, H, M |
| §5 Archives mensuelles | 5–10 lignes par mois + lien rapport | M | M |

Couches dérivées (D13–D14) : `Etat_editorial_courant.md` (généré, lu par Q) ; `Radar_editorial.md` (écrit par Q — retrait, ajout de questions —, H — blocs 1–3, tri —, M — blocs 4–5, archives).

### 8.2 Colonnes du §1

`Date | ID | Titre | Type | Catégorie / Thème | Question du Phare | Dossier | Penseur / concept | Sentier | Article précédent | Prolongement envisagé`

Types : `Actualité` | `Question` | `Application` | `Texte fondateur` | `Fil du Phare` | `Synthèse mensuelle`.

### 8.3 Règles

- Titre en lien `[titre](url)` ; champ inconnu = `—`.
- Ne jamais recopier le contenu des articles.
- Une routine n'écrit **que** ses sections.
- La quotidienne écrit une ligne par article via `tools/memoire_append.py` (deux en variante `paire`).
- Taille cible : §1 ≤ ~60 lignes (purge mensuelle).
- Amorçage : 8 triptyques (2026-505 → 2026-528), fil actif « Souveraineté technologique européenne », cap TECH/CULTURE sous-représentés.

---

## 9. Données, fichiers et métadonnées

### 9.1 Arborescence

```
00_Systeme/                      instructions, taxonomie, manifests, logs, Memoire_editoriale.md
01_Actualites/<Theme>/           ACTU (quotidienne)
02_Fonds/<Theme>/                FOND — fondamentaux parents (éditeur humain pour le push WP)
03_Dossiers/<Theme>/             DOSSIER (mensuelle)
04_Textes_fondateurs/Auteurs/    TF (mensuelle ; quotidienne occasionnelle)
05_Sentier/Etape_XX_…/           SENTIER — ateliers (mensuelle ; triptyque)
06_Syntheses/
  Thematiques/                   existant
  Fil_du_Phare/                  hebdomadaire (à créer au 1er run)
  Mensuelles/                    synthèses mensuelles (à créer au 1er run)
  Rapports_mensuels/             YYYY-MM.md (à créer au 1er run)
07_A_Publier/<YYYY-MM-DD_slug>/  transit (1 article, ou 3 en triptyque)
08_Reseaux_sociaux/, 90_Medias/, 99_Archives/   hors périmètre routines
index_editorial.csv              registre canonique
```

### 9.2 IDs et nommage

- ID `YYYY-NNN` réservé depuis la dernière ligne de l'index (dernier au 2026-10-05 : **2026-530**) ; jamais réutilisé.
- Fichier : `YYYY-NNN_TYPE_THEME_slug_descriptif_V1.md`, TYPE ∈ `ACTU`, `TF`, `SENTIER`, `FOND`, `DOSSIER`, `SYNTHESE`.

### 9.3 Index (`index_editorial.csv`)

En-tête : `ID,Titre,Type,Theme,Statut,Version,Date_creation,Date_derniere_maj,Auteur,Etape_sentier,Articles_lies,Mots_cles,Resume_court,Objectif,Nom_fichier,Chemin_dossier,Date_publication_WP,URL_WordPress,Slug_WordPress,Categorie_WP,Tags_WP,Remarques`.

Écriture **uniquement** via `tools/index_editorial_utils.build_index_row(...)` + `append_rows_to_index(Path("index_editorial.csv"), rows)`. `Remarques` : `Routine quotidienne v3 — type <type>` / `Routine hebdomadaire — Fil du Phare` / `Routine mensuelle — <nature>`.

### 9.4 En-tête d'article

Base : `00_Systeme/Modele_Entete_Article.md` (ID, Titre, Type, Theme, Statut, Version, dates, Auteur, Étape/Fondamental/Type/Posture Sentier, Articles liés, Mots-clés, Résumé court ≤ 500 car., Objectif, Sources, URL WP, `---`).

Champs ajoutés par les routines v3 :

```
Type article : Actualité | Question | Application | Texte fondateur | Fil du Phare | Synthèse mensuelle
Question du Phare : …   (pour B : la question traitée, identique à celle de A)
Dossier : …
Article precedent (ID) : YYYY-NNN
Prolongement envisage : …
```

Fin de fichier : bloc `# SEO` (Mot-clé principal, Meta description, `Slug propose`) — obligatoire pour `wp_push_draft`.

### 9.5 Taxonomie WordPress

| Catégorie | Usage |
|-----------|-------|
| `actualites` | ACTU (types A, B, C) |
| `textes-fondateurs` | TF |
| `sentier-du-savoir` | SENTIER |
| `dossier-hebdomadaire` | DOSSIER |
| `le-phare` | pages institutionnelles |
| `cycle` (id 97) | existante, « Dossier hebdomadaire - Notre fil rouge » — Fil du Phare, synthèse mensuelle (B1) |

Tag de visibilité : `a-la-une` sur **tout** article publié (sans lui, le thème n'affiche pas l'article — D15).

Tags thème : `monde`, `politique-societe`, `economie-finance`, `technologie-ia`, `environnement-climat`, `science-sante`, `culture-philosophie`. Nouveaux tags : `question-du-phare`, `type-actualite`, `type-question`, `type-application`, `type-texte-fondateur`, `fil-du-phare`, `synthese-hebdomadaire`, `synthese-mensuelle`.

---

## 10. Outillage technique

| Script | Rôle | Changement v3 |
|--------|------|---------------|
| `tools/daily_run.py` | Orchestration publication (`--publish-existing`, `--keep-publish-folder`, `--no-publish-final`, `--force`) | Aucun. Garde `00_Systeme/Logs/daily_run_YYYY-MM-DD.json` → `--force` pour un 2e run le même jour. |
| `tools/wp_push_draft.py` | Création brouillons WP, `--refresh-body` | `_slug_from_filename` reconnaît `ACTU, TF, SENTIER, FOND, DOSSIER, SYNTHESE`. |
| `tools/wp_refresh_body.py` | `wp_push_draft --refresh-body` avec la config locale résolue par le script ; refuse `02_Fonds/` sauf `--allow-fonds` (triptyque archivé) ; `--title` met aussi à jour le titre WP depuis l'en-tête `Titre :` | v3.10 : le chemin `tools/*.local.json` n'apparaît plus dans une commande (bloquée par la règle deny). |
| `tools/index_lookup.py` | `ID Type Theme Statut URL Titre` pour une liste d'IDs ou une recherche | v3.10 : lecture d'URL sans `python -c` ni filtre shell. v5 : `--search`, `--type`, `--theme`, `--dossier`, `--limit`. |
| `tools/memoire_append.py` | Ajoute la ligne d'un article au §1 de la mémoire depuis l'en-tête + l'index (+ manifeste Sentier) ; `--penseur`, `--sentier`, `--type-label`, `--dry-run` ; refuse un doublon | v5 (B3 partiel). |
| `tools/build_etat_courant.py` | Génère `Etat_editorial_courant.md` (≤ 50 lignes) depuis la mémoire §1–§4 et le Radar | v5 (D13). |
| `tools/verify_publication.py` | Contrôle de fin de routine (D15) : liens, maillage, navigation, statut WP, tag `a-la-une` ; `[IDs…]`, `--days`, `--offline`, `--fix`, `--publish-drafts` ; réécrit les liens `?p=` en permaliens et rafraîchit les corps | v5.1. |
| `tools/build_catalogue.py` | Génère `Catalogue_editorial.md` (vue large, mensuelle) | v5 : renvoi vers le Radar et l'État courant. |
| `tools/post_linking.py` | Maillage + publication | Accepte **1** article (sans contrainte de type, sans injection de bloc) ou **3** (triptyque). `update_index_notes` seulement si > 1 article. |
| `tools/post_seo_enrich.py` | Enrichissement SEO optionnel | Exige 3 IDs (`daily_run.py` ~l.322) → inactif hors triptyque (voir B4). |
| `tools/index_editorial_utils.py` | `build_index_row`, `append_rows_to_index` | Aucun. |
| `tools/validate_index_editorial.py` | Validation de l'index | Aucun : contrôle d'alignement des colonnes seulement, `SYNTHESE` accepté (T3). |
| `tools/editorial_pipeline.py` | Génération par API | Exception `api` uniquement. |
| `tools/fetch_wp_categories.py`, `fetch_wp_tags.py` | Snapshots taxonomie | À relancer après T5 (nouveaux tags). |

Configuration locale (non lue par Claude) : `tools/wp_config.local.json`, `tools/editorial_config.local.json`, `tools/wp_featured_media.local.json`.

Permissions (`.claude/settings.json`) : Bash python/mkdir/cp/curl/ls/find, WebFetch, WebSearch ; Edit/Write sur `01_Actualites`, `02_Fonds`, `03_Dossiers`, `04_Textes_fondateurs`, `05_Sentier`, `06_Syntheses`, `07_A_Publier`, `index_editorial.csv`, `00_Systeme/Memoire_editoriale.md`. Pas de `rm` (volontaire : la veille web expose à l'injection) → ménage manuel de `07_A_Publier/`.

---

## 11. Règles et interdits transverses

1. Aucun appel API silencieux pour rédaction/calibrage (`calibration_api_enabled` / `seo_enrich_api_enabled` requis).
2. `editorial_pipeline.py` jamais comme moteur d'écriture sans demande `api`.
3. **Jamais** de push WP sur `02_Fonds/` (ni création ni refresh) — éditeur humain.
4. Pas d'URL nue dans `Repères de sources` : `[libellé](url)`.
5. Pas de 11e fondamental Sentier sans accord humain ; un SENTIER = atelier d'un fondamental existant.
6. Index modifié uniquement via `append_rows_to_index`.
7. Liens internes : URLs réelles uniquement (index / manifest), jamais inventées, jamais `wiki-du-phare`.
8. Ne jamais lire `tools/*.local.json`, `**/.env`, `**/*credentials*`.
9. Autonomie : pas de question intermédiaire ; rapport final court.
10. Économie de tokens : pas de relecture après édition réussie ; lecture ciblée (tail/filtres) de l'index et de la mémoire ; sorties JSON résumées (`status`, `error`, `wordpress_id`, `link`).
11. Git : jamais `push --force`, pas d'amend, pas de commit sans accord.
12. Penseurs : grille de lecture, jamais argument d'autorité (§5.8).
13. Variante `paire` : si B échoue (publication, validation), le signaler au rapport plutôt que livrer A seul en silence.
14. Sans demande de permission : une commande Bash simple par appel (pas de `&&`, `;`, `|`, `python -c` multiligne), Read/Grep/Edit plutôt que `cat`/`grep`/`sed`, jamais le chemin d'un `tools/*.local.json` dans une commande (`wp_refresh_body.py`, `index_lookup.py`).

---

## 12. État d'avancement (au 2026-10-05)

### 12.1 Fait

- [x] Archivage ancienne routine : `.claude/skills/routine-triptyque/` (SKILL.md + workflow.md), `.claude/commands/routine-triptyque.md` ; suppression de `.claude/rules/`.
- [x] Bandeau ARCHIVÉ sur `00_Systeme/Routine_quotidienne.md` et `Routine_quotidienne_V2.md`.
- [x] `00_Systeme/Memoire_editoriale.md` créé et amorcé.
- [x] Skills + commandes : `routine-quotidienne`, `routine-hebdomadaire`, `routine-mensuelle`.
- [x] `tools/post_linking.py` (1 ou 3 articles) — testé en dry-run sur une copie de 2026-429.
- [x] `tools/wp_push_draft.py` (`DOSSIER`, `SYNTHESE` dans `_slug_from_filename`).
- [x] `CLAUDE.md` réécrit (déclencheurs, règles communes, arborescence).
- [x] `.claude/settings.json` (permissions `03_Dossiers`, `06_Syntheses`, mémoire).
- [x] `py_compile` OK sur les scripts modifiés.
- [x] T1 — `Modele_Entete_Article.md` : champs v3, note sur le plan indicatif, navigation finale v3 et bloc `# SEO`.
- [x] T2 — `Taxonomie_WordPress_le-phare_info.md` : six familles (`syntheses`), mention `cycle` non utilisée, correspondance routines / types, tags de type / Fil du Phare / synthèse, règles DOSSIER et SYNTHESE, liens vers `plan.md` et skills.
- [x] T3 — Validé sur copie scratch de l'index : `build_index_row` + `append_rows_to_index` avec `Type=SYNTHESE`, chemin `06_Syntheses/Fil_du_Phare`, aucune alerte de `validate_index_editorial.py` sur la ligne ; `wp_push_draft --dry-run` → slug `Slug propose`, catégorie `syntheses`, 4 tags. Le validateur ne contrôle ni le type ni le chemin (alignement de colonnes seulement).
- [x] T7 — `Strategie_routine_quotidienne_graphe_taxonomie_WP.md` (bandeau v3, défauts), `Checklist_publication.md` (navigation v3, en-tête v3, `# SEO`), `.cursor/rules/editorial-assisted-writing.mdc` (bandeau v3, déclencheurs).

### 12.2 À faire

| ID | Tâche | Priorité |
|----|-------|----------|
| T4 | Premier run `routine quotidienne — brouillons seulement` (validation §14) | Haute |
| T5 | Premier run hebdomadaire en brouillons ; vérifier le classement dans `cycle` (id 97) | Haute |
| T6 | Relancer `fetch_wp_categories.py` / `fetch_wp_tags.py` après T5 | Moyenne |
| T8 | Premier run mensuel (fin octobre → début novembre 2026) | Moyenne |
| T10 | Aligner sur D9–D11 : `routine-quotidienne/SKILL.md` (paire, §5.6–§5.9), `CLAUDE.md`, `actions.md`, `Instructions_editoriales_officielles.md` (renvoi au socle), `.claude/commands/routine-quotidienne.md` ; puis premier run paire en brouillons | Fait (v3.8) : premier run paire 2026-543 (A) + 2026-544 (B), brouillons |
| T11 | Rattrapage optionnel : articles B pour les actualités 2026-533 → 542 (`type question — sur <ID>`) | Moyenne |
| T12 | Compléter le socle : §5 « Place de Simone Weil » tronqué dans le docx (décision humaine) | Moyenne |
| T9 | Commit ciblé des fichiers de la refonte | Fait — `19fd68c` + `e56e6aa` (configs locales hors suivi) |
| T13 | Premier run quotidien V5 (D12) : vérifier arbitrage, `memoire_append`, mise à jour du Radar, `build_etat_courant` | Haute |
| T14 | ~~Rénovation lot 1 (tri, §19.3)~~ fait le 2026-10-06 ; reste : URL WP de 062 et 064 | Basse |
| T15 | Outils de rénovation : resynchronisation WP → local (B18), remise à niveau de la navigation (B19), skill `routine-renovation` (B20) | B18 et B20 faits (v5.4) ; B19 reste (lot 2 à la main en attendant) |
| T16 | Refresh WP des articles au `# SEO` final publiés avant v5.4 (fuite « SEO » visible en bas d'article, Rank Math vide)  : 35 articles, 2026-528 → 562 ; `wp_refresh_body.py` sur chaque fichier, puis `verify_publication.py` | Fait (v5.4) — 35/35 rafraîchis, 0 erreur ; restent les avertissements 528/529 (navigation triptyque) et 536 (lien vers le brouillon 445) |

---

## 13. Journal des évolutions

| Date | Version | Changement | Fichiers |
|------|---------|------------|----------|
| 2026-10-05 | v3.0 | Passage du triptyque quotidien à trois routines + mémoire partagée | voir §12.1 |
| 2026-10-05 | v3.1 | Alignement documentaire (T1, T2, T7) + validation index/WP du type `SYNTHESE` (T3) | `Modele_Entete_Article.md`, `Taxonomie_WordPress_le-phare_info.md`, `Strategie_routine_quotidienne_graphe_taxonomie_WP.md`, `Checklist_publication.md`, `.cursor/rules/editorial-assisted-writing.mdc` |
| 2026-10-05 | v3.2 | Rangement automatique : `new_article.py` (B13) branché dans les routines ; backlog B14–B15 | `plan.md`, `tools/new_article.py`, `actions.md`, `.claude/skills/routine-{quotidienne,hebdomadaire,mensuelle}/SKILL.md` |
| 2026-10-05 | v3.3 | Validateur v3 (B14) branché sur `new_article.py stage` ; `.gitignore` des configs locales | `tools/validate_index_editorial.py`, `tools/new_article.py`, skills, `actions.md`, `.gitignore` |
| 2026-10-05 | v3.4 | Hubs de dossiers générés depuis l'index (B15) | `tools/build_hubs.py`, `routine-mensuelle`, `routine-quotidienne`, `actions.md` |
| 2026-10-05 | v3.5 | B12 : faux positifs du validateur d'alignement (imports WP) | `tools/index_editorial_utils.py` |
| 2026-10-05 | v3.6 | B1 : synthèses dans la catégorie existante `cycle` | `tools/new_article.py`, `tools/validate_index_editorial.py`, skills hebdo/mensuelle, `actions.md`, `CLAUDE.md`, `Taxonomie_WordPress_le-phare_info.md` |
| 2026-10-05 | v3.7 | Socle éditorial consolidé intégré ; paire quotidienne Actualité + Question du Phare (D9–D11) — plan seulement, skills à aligner (T10) | `plan.md` |
| 2026-10-05 | v3.8 | T10 : skill quotidien réécrit pour la paire (§4 forme, §6A/§6B, §7 navigation croisée, §8 séquence de publication §5.9, §9 deux lignes) ; variantes `type application` / `type texte fondateur` = article seul, `type question — sur <ID>` = B seul ; commande, `CLAUDE.md`, `actions.md` alignés ; renvoi au socle dans les Instructions §1. Premier run paire en brouillons : 2026-543 (A, ?p=5493) + 2026-544 (B, ?p=5495), liens croisés ok ; `wp_push_draft --refresh-body` exige `--config tools/wp_config.local.json` (ajouté au §8 du skill) | `.claude/skills/routine-quotidienne/SKILL.md`, `.claude/commands/routine-quotidienne.md`, `CLAUDE.md`, `actions.md`, `00_Systeme/Instructions_editoriales_officielles.md`, `plan.md` |
| 2026-10-05 | v3.9 | Base éditoriale : `tools/build_catalogue.py` génère `00_Systeme/Catalogue_editorial.md` (inventaire depuis l'index, équilibre, lacunes) ; `00_Systeme/Articles_a_creer.md` = liste priorisée P1–P3 par niveau du parcours. Branchés : quotidienne (pioche P1, retire le réalisé), hebdomadaire (ajoute suivis/questions), mensuelle (régénère, révise) | `tools/build_catalogue.py`, `00_Systeme/Catalogue_editorial.md`, `00_Systeme/Articles_a_creer.md`, skills des 3 routines, `actions.md`, `plan.md` |
| 2026-10-06 | v3.10 | Routines sans demande de permission : `tools/wp_refresh_body.py` (refresh WP sans chemin de config dans la commande, garde `02_Fonds/`) et `tools/index_lookup.py` (URLs d'index) ; `build_hubs.py` imprime la nouvelle commande ; règle « une commande Bash simple par appel » dans les skills | `tools/wp_refresh_body.py`, `tools/index_lookup.py`, `tools/build_hubs.py`, skills des 4 routines, `plan.md` |

| 2026-10-06 | v5.0 | Pilotage éditorial adaptatif (`planV5.docx`) : D12 (un article par jour, type après le sujet, remplace D9), D13 (État courant généré), D14 (Radar). Phases 1, 2, 4 ; phase 3 « Relations » reportée (B17). `Articles_a_creer.md` → `Radar_editorial.md` (réécrit en 5 blocs) ; nouveaux `memoire_append.py`, `build_etat_courant.py` ; `index_lookup.py` (recherche) ; skill quotidien réécrit (lectures : État courant, Radar, veille ; arbitrage noté ; variante `paire`) ; hebdo = comité du Radar + 5 fils actifs ; mensuelle = blocs 4–5, archivage, catalogue | `plan.md`, `CLAUDE.md`, `actions.md`, skills et commande quotidienne, `00_Systeme/Radar_editorial.md`, `00_Systeme/Etat_editorial_courant.md`, `00_Systeme/Memoire_editoriale.md`, `tools/memoire_append.py`, `tools/build_etat_courant.py`, `tools/index_lookup.py`, `tools/build_catalogue.py` |
| 2026-10-06 | v5.1 | D15 : vérification de fin de routine (`verify_publication.py`) et tag `a-la-une` obligatoire (`new_article.py`, `wp_push_draft.py`, validateur hors quota). Publication des brouillons 531–552, 559, 560 ; tag ajouté à 553–558, 561, 562 ; liens `?p=` réécrits | `tools/verify_publication.py`, `tools/new_article.py`, `tools/wp_push_draft.py`, `tools/validate_index_editorial.py`, skills des 3 routines, `plan.md`, `CLAUDE.md` |
| 2026-10-06 | v5.2 | D16 : préfixe de titre par type (sauf Actualité), tiret court ; `wp_refresh_body.py --title` ; préfixe appliqué à 544, 546, 547, 548, 550, 552, 559, 560 | `tools/new_article.py`, `tools/wp_push_draft.py`, `tools/wp_refresh_body.py`, skills des 3 routines, `plan.md`, 8 articles, index |
| 2026-10-06 | v5.3 | D17 : inventaire de rénovation du stock ancien (lecture seule, GET WP) et plan en lots (§19) ; contenus de démo 414–418 retirés | `tools/build_inventaire_renovation.py`, `00_Systeme/Inventaire_renovation.md`, `plan.md` |
| 2026-10-06 | v5.4 | B18 : `wp_pull_body.py` (resynchronisation WP → local, contrôle d'aller-retour) ; B20 : skill et commande `routine-renovation`. Bug corrigé dans `wp_push_draft.extract_seo_and_body` : un bloc `# SEO` **final** (format v3) était publié dans le corps (`<h1>SEO</h1>` + paragraphe) et Rank Math ne recevait ni mot-clé ni description ; clés « Meta description » / « Meta-description » acceptées. T16 : refresh WP des 35 articles 528 → 562. `wp_refresh_body.py` force `PYTHONUTF8` dans le sous-processus (échec cp1252 sur « Hōlei ») | `tools/wp_pull_body.py`, `tools/wp_push_draft.py`, `tools/wp_refresh_body.py`, `.claude/skills/routine-renovation/SKILL.md`, `.claude/commands/routine-renovation.md`, `CLAUDE.md`, `plan.md` |

*(Ajouter une ligne par évolution, la plus récente en bas.)*

---

## 14. Plan de validation

### 14.1 Quotidienne (brouillons)

1. `routine quotidienne — brouillons seulement`.
2. Vérifier : 2 IDs réservés (A, B), liens croisés A → B et B → A, fichier canonique au bon endroit, en-tête v3 complet, navigation finale sans « Dans ce triptyque », liens internes réels, `# SEO` présent.
3. Index : nouvelle ligne valide (`validate_index_editorial.py`).
4. WP : brouillon créé, catégorie `actualites`, tags de type + `question-du-phare`.
5. Mémoire : deux lignes §1, rien d'autre modifié.
6. Puis un run publié complet.

### 14.2 Hebdomadaire

1. Après ≥ 3 quotidiennes v3 (sinon tester la branche « < 3 articles »).
2. Vérifier : `06_Syntheses/Fil_du_Phare/` créé, brouillon classé dans `cycle`, `--force` fonctionnel, liens vers chaque article de la semaine, §1/§2/§3 mis à jour.

### 14.3 Mensuelle

1. Vérifier : rapport `06_Syntheses/Rapports_mensuels/YYYY-MM.md`, aucun push sur `02_Fonds/`, ateliers ancrés sur un fondamental existant, purge §1 → §5, nouveau §4.

### 14.4 Non-régression triptyque

`/routine-triptyque — brouillons seulement` : `post_linking` doit toujours injecter « Dans ce triptyque » et exiger ACTU/TF/SENTIER.

---

## 15. Risques et points de vigilance

| Risque | Effet | Parade |
|--------|-------|--------|
| Garde `daily_run` un même jour | 2e routine refusée | `--force` (hebdo, mensuelle) |
| Mémoire qui grossit | Coût tokens | Purge mensuelle §1, lecture ciblée |
| Mémoire désynchronisée de l'index | Liens faux, ID manquant | L'index fait foi ; la mensuelle réconcilie |
| Routine qui écrit hors de ses sections | Perte d'information | Règle §8.3 ; contrôle au rapport |
| Questions du Phare artificielles | Baisse de qualité | Une seule question, critères §5.7 ; pas de question rhétorique |
| Redite entre A et B | Contenu dupliqué | D11 : A = faits, B = sens ; B résume A en un paragraphe |
| Question finale jamais développée | Question orpheline | Elle entre au Radar bloc 2 (D12) ; l'hebdo la priorise ou l'archive |
| État courant périmé | Choix sur une vue fausse | Régénéré par chaque routine ; la quotidienne le régénère s'il a > 7 jours |
| Radar qui gonfle | Lecture coûteuse, priorités floues | ≤ 30 actives ; tri hebdo, archivage mensuel |
| Type choisi par habitude | Retour d'une série rigide | Arbitrage noté (D12), justification du type au rapport |
| Penseur plaqué | Argument d'autorité | §5.8 : tester une intuition, confronter aux faits |
| TF / ateliers forcés en mensuelle | Retour de l'artificiel | Plafond 0–2, « 0 » valide |
| Docs `00_Systeme/` encore orientés triptyque | Consignes contradictoires | Bandeaux v3 posés (T7) ; les skills v3 font foi |
| `post_seo_enrich` inactif hors triptyque | SEO moins riche | Accepté ; B4 |
| Pas de `rm` | `07_A_Publier/` s'accumule | Ménage manuel périodique |
| Injection via veille web | Actions non voulues | Pas de `rm`, deny sur secrets, publication seulement via scripts |
| Copie locale tronquée (~70 anciens articles : WP bien plus long que le `.md`) | Un refresh depuis le local écrase la version en ligne | D17 : resynchroniser depuis WP avant toute retouche (B18) ; marqueur « tronquée » dans l'inventaire |
| Lignes d'index en double (même URL) | Article compté deux fois, maillage ambigu | Lot 1 de la rénovation (§19.3) |
| Liens `?p=` vers des posts absents de l'index | Liens fragiles, `--fix` impuissant | Résolus à la main pendant la remise à niveau (lot 2) |
| Pertes au pull WP → local (italique, images, iframes, tableaux) | Contenu appauvri après resynchronisation | `wp_pull_body.py` les signale ; pas d'`--apply` si image/iframe/tableau ou écart d'aller-retour |
| Bloc `# SEO` final publié dans le corps (avant v5.4) | « SEO » visible en bas d'article, Rank Math vide | Corrigé dans `wp_push_draft.py` ; refresh des articles concernés (T16) |

---

## 16. Backlog des évolutions envisagées

| ID | Évolution | Statut |
|----|-----------|--------|
| B1 | Utiliser la catégorie existante `cycle` (id 97) pour le Fil du Phare au lieu de `syntheses` | Fait — Fil du Phare et synthèse mensuelle dans `cycle` ; pas de catégorie `syntheses` |
| B2 | Déclenchement planifié (cron / RemoteTrigger) | Écarté (D4), réévaluable |
| B3 | Script `tools/memoire_editoriale.py` (ajout ligne §1, purge, lecture N dernières lignes) pour fiabiliser et économiser des tokens | Partiel (v5) — ajout §1 : `memoire_append.py` ; lecture : `build_etat_courant.py` ; purge restante |
| B4 | `post_seo_enrich` compatible article unique (lever la contrainte 3 IDs dans `daily_run.py`) | Idée |
| B5 | Page WordPress « Les questions du Phare » (agrégation des Questions du Phare via tag) | Idée |
| B6 | Lien automatique « Pour aller plus loin » vers le dernier Fil du Phare | Idée |
| B7 | Génération/choix d'image à la une par type (`wp_featured_media.local.json`) | Idée |
| B8 | Déclinaison réseaux sociaux (`08_Reseaux_sociaux/`) depuis le Fil du Phare | Idée |
| B9 | Rétro hebdomadaire systématique (template existant) | Optionnel |
| B10 | Rapport d'équilibre thématique calculé par script (index → tableau) | Idée |
| B11 | Retrait définitif de la routine triptyque après N semaines sans usage | Après validation v3 |
| B12 | Corriger les lignes préexistantes de l'index signalées par `validate_index_editorial.py` (« Categorie_WP contains ';' but Tags_WP is empty » : 2026-050, 059, 061–066, 081–082, 102–104, 107, 233, 259, 315–317, 327, 329, 332, 335–418) | Fait — faux positifs : les 106 lignes sont des imports WP (« Import auto API WP ») aux catégories multiples réelles et sans tags ; règle désactivée pour ces lignes dans `validate_row_columns`, index inchangé |
| B13 | `tools/new_article.py` : création déterministe d'un article (type + thème + slug) — réserve l'ID, calcule chemin canonique, nom de fichier, catégorie et tags WP, écrit le squelette v3, ajoute la ligne d'index, prépare le dossier de transit `07_A_Publier/` (sous-commande `stage`) | Fait — branché dans les 3 skills |
| B14 | Validateur étendu : cohérence type/chemin/catégorie, ≤ 8 tags dont le tag de thème, champs v3 présents, liens internes existants dans l'index ; lancé par les routines avant publication | Fait — `validate_index_editorial.py --ids`, appelé automatiquement par `new_article.py stage` |
| B15 | `tools/build_hubs.py` : sections « Articles de ce dossier » générées depuis l'index + `--refresh-body` des hubs (jamais `02_Fonds`) | Fait — hub = plus petit ID du sous-dossier ; section `## Liens internes du dossier` remplacée ; refresh WP affiché, pas lancé |
| B16 | Mode paire intégré : `post_linking.py` accepte 2 articles (A ACTU + B `type-question`), injecte les liens croisés et publie en un seul `daily_run` | Idée, moins urgente depuis D12 (paire = variante) |
| B17 | Champ d'en-tête « Relations » (phase 3 de la V5) : relations typées entre articles (suite de, applique, répond à…) | Reporté (décision 2026-10-06) |
| B18 | `tools/wp_pull_body.py <ID>` : remplace le corps local par la version WP (HTML → Markdown relu par `wp_push_draft`), en gardant l'en-tête, le titre et le bloc `# SEO` ; à blanc par défaut (mots local / WP / aller-retour, pertes), `--apply` pour écrire ; refuse `02_Fonds/` | Fait (v5.4) — aller-retour exact sur 497, 010, 531, 499, 153, 250 |
| B19 | `tools/renovate_nav.py <ID>` : navigation v3 semi-automatique (« Dans ce triptyque » → « Pour aller plus loin », squelette « La question suivante » et « Sur le Sentier du Savoir » depuis le manifeste, liens `?p=` signalés) ; texte de la question rédigé à la main | Idée — lot 2 |
| B20 | Skill `routine-renovation` (§19.4) | Fait (v5.4) — `.claude/skills/routine-renovation/SKILL.md` + `/routine-renovation` |

---

## 17. Procédure pour faire évoluer le système

1. **Décrire** l'évolution (ligne en §16 ou nouvelle décision en §3).
2. **Vérifier l'existant** : grep des usages + `git log` sur les fichiers touchés ; le code réel prime sur ce plan.
3. **Identifier les fichiers impactés** (§18) — un changement de type/catégorie touche en général : skill(s), `CLAUDE.md`, taxonomie, modèle d'en-tête, `wp_push_draft.py`, éventuellement `validate_index_editorial.py` et la mémoire.
4. **Modifier** skills / scripts / docs ensemble ; `python -m py_compile` sur les scripts modifiés ; dry-run si un script de publication change.
5. **Valider** en brouillons (§14), puis non-régression triptyque si `post_linking` / `daily_run` / `wp_push_draft` changent.
6. **Mettre à jour ce plan** : §3 (décision), §12 (état), §13 (journal), §16 (backlog).
7. **Commit** ciblé, après accord, incluant tous les fichiers impactés.

---

## 18. Index des fichiers concernés

| Fichier | Rôle |
|---------|------|
| `plan.md` | Ce document |
| `CLAUDE.md` | Instructions projet chargées à chaque session |
| `.claude/settings.json` | Permissions |
| `.claude/skills/routine-quotidienne/SKILL.md` | Routine quotidienne |
| `.claude/skills/routine-hebdomadaire/SKILL.md` | Routine hebdomadaire |
| `.claude/skills/routine-mensuelle/SKILL.md` | Routine mensuelle |
| `.claude/skills/routine-renovation/SKILL.md` | Routine de rénovation du stock ancien (D17, §19) |
| `.claude/skills/routine-triptyque/SKILL.md`, `workflow.md` | Ancienne routine (archivée) |
| `.claude/commands/routine-*.md` | Slash commands (5) |
| `00_Systeme/Memoire_editoriale.md` | Mémoire partagée |
| `00_Systeme/Instructions_editoriales_officielles.md` | Qualité rédactionnelle |
| `00_Systeme/Catalogue_editorial.md` | Inventaire généré (`tools/build_catalogue.py`) : articles, équilibre, lacunes — lu par la mensuelle seulement |
| `00_Systeme/Radar_editorial.md` | Radar éditorial (D14), ex-`Articles_a_creer.md` |
| `00_Systeme/Etat_editorial_courant.md` | Vue courte générée (D13), lue par la quotidienne |
| `tools/memoire_append.py`, `tools/build_etat_courant.py`, `tools/index_lookup.py` | Outils V5 (mémoire §1, état courant, recherche d'index) |
| `tools/verify_publication.py` | Vérification de fin de routine (D15) |
| `tools/build_inventaire_renovation.py`, `00_Systeme/Inventaire_renovation.md` | Inventaire de rénovation du stock ancien (D17, §19), généré |
| `tools/wp_pull_body.py` | Resynchronisation du corps local depuis WP (B18) |
| `planV5.docx` | Source de la V5 (pilotage éditorial adaptatif) |
| `00_Systeme/Modele_Entete_Article.md` | En-tête v3 |
| `00_Systeme/Taxonomie_WordPress_le-phare_info.md` | Catégories/tags |
| `00_Systeme/Manifests/sentier_fondamentaux.csv` | Fondamentaux parents |
| `00_Systeme/Sentier_fondamentaux_referentiel.md` | Règles ateliers |
| `00_Systeme/Retro_routine_hebdo_TEMPLATE.md` | Rétro hebdo |
| `00_Systeme/Routine_quotidienne.md`, `Routine_quotidienne_V2.md` | Archivés (bandeau) |
| `00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md`, `Checklist_publication.md` | Alignés v3 (bandeau) |
| `.cursor/rules/editorial-assisted-writing.mdc` | Règle Cursor (bandeau v3) |
| `index_editorial.csv` | Registre canonique |
| `actions.md` | Répertoire de toutes les actions (prompts, scripts, options) |
| `tools/daily_run.py`, `wp_push_draft.py`, `post_linking.py`, `index_editorial_utils.py`, `validate_index_editorial.py` | Chaîne technique |
| `ROUTINE QUOTIDIENNE.docx`, `ROUTINE HEBDOMADAIRE.docx`, `ROUTINE MENSUELLE.docx` | Sources de la refonte |
| `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` | Socle éditorial (D10) — tronqué au §5 |

---

## 19. Rénovation du stock ancien

Décision D17. Inventaire : `python tools/build_inventaire_renovation.py` (avec `--offline` : sans WordPress) → `00_Systeme/Inventaire_renovation.md`. Le script est en lecture seule et se relance après chaque session.

### 19.1 Périmètre (état au 2026-10-06, 553 lignes d'index)

| Groupe | Nombre | Traitement |
|--------|--------|------------|
| Hors périmètre : `02_Fonds/` | 259 | Éditeur humain, jamais de push |
| Hors périmètre : pages `wiki-du-phare` | 79 | Aucun |
| Format actuel (routines v3/V5) | 32 | Aucun |
| **Trier** | 68 | Lot 1 : décision humaine, puis action technique |
| **Remettre à niveau** | 62 | Lot 2 : navigation et titre, sans réécriture |
| **Refaire** | 53 | Lot 3 : réécriture au format actuel |

Familles d'origine : `triptyque` (ère 2026-419 → 530), `import` (« Import auto » depuis WP).

### 19.2 Classement (règles du script, dans l'ordre)

1. Même URL qu'une ligne `02_Fonds/` ou wiki → Trier (ligne d'index en double).
2. Jamais publié → Refaire si DOSSIER, sinon Trier (brouillon). `Statut=archive` → hors périmètre.
3. Même début de titre qu'un autre article → Refaire (fusion dans le mieux relié, sans dépublier).
4. Titre court à emoji → hors périmètre (page rubrique, hors flux).
5. Introuvable sur WP → Trier.
6. Cité par un article actuel, OU par la mémoire, le Radar ou un dossier, OU TF de score ≥ 3 → Refaire.
7. Sinon → Remettre à niveau.

Score de priorité = 3 × liens entrants depuis un article actuel + autres liens entrants + 2 × références (mémoire, Radar, dossiers) + 2 si TF. Dans chaque niveau, l'inventaire est trié par score décroissant.

### 19.3 Lots

**Lot 0 — garde-fous (avant tout).**
- Article marqué « copie locale tronquée » (69 dans le périmètre) : resynchroniser depuis WP (B18) avant toute retouche. Ne jamais lancer `wp_refresh_body.py` sur une copie tronquée.
- Ne jamais toucher `02_Fonds/`.

**Lot 1 — Trier (68) : fait le 2026-10-06.**

| Sous-lot | IDs | Décision appliquée |
|----------|-----|--------------------|
| Doublons d'index par URL | 29 paires import (120–129, 152–160, 193–202) ↔ wiki (335–344, 355–363, 394–403) | **Lignes wiki retirées** (inverse de la proposition initiale : la ligne import, rattachée au manifeste, est canonique) ; 28 fichiers wiki identiques supprimés. 394 conservé (corps différent, publié sous `/wiki-du-phare/`), sans ligne d'index |
| Brouillons jamais publiés | 419–435, 439–447 | DOSSIER (419–428, 435) gardés en `wp_draft` → lot 3 (format actuel puis publication) ; 15 autres passés en `Statut=archive` |
| Doublons de titre | 111 ↔ 455, 005 ↔ 419, 118 ↔ 024, 078 ↔ 029, 192 ↔ 193 | Fusion au lot 3 dans l'article retenu, **sans dépublier** (toute dépublication : accord explicite) |
| Pages rubriques | 058, 059, 061, 063, 065, 066 | `a-la-une` retiré sur WP ; hors périmètre de l'inventaire. 062 et 064 : post introuvable sur WP (URL d'index à vérifier) |

**Lot 2 — Remettre à niveau (62, par paquets de 5 à 10).**
- Remplacer « Dans ce triptyque » par la navigation v3 (§5.4) : « La question suivante », « Pour aller plus loin », « Sur le Sentier du Savoir » (B19).
- Titre : retirer l'emoji. Le préfixe D16 n'est pas rétroactif au-delà des articles déjà traités.
- Liens `?p=` : remplacer par l'URL de l'index, ou retirer.
- Puis `wp_refresh_body.py`, et `verify_publication.py <IDs>`.

**Lot 3 — Refaire (53, 1 à 3 par session, par score décroissant).**
- Réécriture complète au format du type actuel (Actualité / Question / Application / TF ; SENTIER → atelier d'un fondamental existant), selon les Instructions et le socle.
- **Même ID, même URL, même slug** ; en-tête complété au format v3 ; `Remarques` de l'index : `Rénové (Routine rénovation) YYYY-MM-DD`.
- Faits d'actualité anciens : les garder datés, sans les « actualiser » artificiellement ; ajouter si besoin un encadré « Depuis » sourcé.
- Pas de ligne en mémoire §1 (ce n'est pas une publication nouvelle) ; noter le lot en §5 de la mémoire lors de la mensuelle.

### 19.4 Rythme et routine

La rénovation **ne se mêle pas** aux routines éditoriales : une session dédiée, déclenchée à la main (`routine renovation` ou `/routine-renovation`, `.claude/skills/routine-renovation/SKILL.md`), par exemple 1 à 2 fois par semaine, en dehors des jours chargés.

Une session :
1. régénérer l'inventaire ;
2. prendre le lot ouvert le plus bas : lot 1 jusqu'à épuisement, puis lot 2 (5 à 10 articles) et lot 3 (1 à 3 articles) en alternance ;
3. resynchroniser les copies tronquées, traiter, rafraîchir sur WP ;
4. lancer `verify_publication.py <IDs>` ;
5. régénérer l'inventaire, puis rapporter ce qui est fait et ce qui reste par niveau.

Le Radar peut signaler qu'un ancien article mérite d'être refait (statut `relier`). La quotidienne ne rénove pas ; elle crée un **nouvel** article qui renvoie à l'ancien.

Ordre de grandeur : lot 1 en 1 session ; lot 2 en 6 à 8 sessions ; lot 3 en 20 à 30 sessions.
