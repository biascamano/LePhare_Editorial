# Systeme editorial Le Phare (V1)

Ce dossier definit la structure source des articles avant publication WordPress.

## Cadre conceptuel actuel

La notion principale a retenir est maintenant :

- `architecture editoriale`

Elle designe l'ensemble coherent forme par :
- une couche de connaissance : noeuds, concepts, tensions, relations
- une couche de publication : types d'articles, parcours de lecture, contenus relies

Dans ce cadre :
- le `triptyque` reste la plus petite forme publiable coherente
- `graphe editorial` et `reseau editorial` sont deux focales du meme systeme

Prompt canonique principal :

- `00_Systeme/Prompts/Prompt_actualite_vers_architecture_editoriale_v1.md`

Memo court associe :

- `00_Systeme/Memo_prompt_court_architecture_editoriale.md`

**Routine quotidienne et graphe de savoir** (un triptyque par jour, architecture qui se construit dans le temps, taxonomie WordPress) :

- `00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md`
- **categories et tags (reference canonique projet)** : `00_Systeme/Taxonomie_WordPress_le-phare_info.md`
- execution : `00_Systeme/Routine_quotidienne.md`

Workflow optionnel pour un **dossier multi-triptyques** ponctuel (sans enchainer le mode technique `architecture_editoriale`) :

- `00_Systeme/Workflow_plan_dossier_triptyques.md`
- gabarit : `00_Systeme/Templates/Plan_dossier_triptyques_TEMPLATE.md`

Le gabarit prevoyait un **nombre libre de triptyques** (selon le sujet) et un **article pivot** optionnel qui relie tout le dossier.

## Arborescence

- `01_Actualites`
- `02_Fonds`
- `03_Dossiers`
- `04_Textes_fondateurs`
- `05_Sentier`
- `06_Syntheses`
- `90_Medias`
- `99_Archives`

## Convention de nommage

Format:

`AAAA-NNN_TYPE_THEME_Titre-court_VX.docx`

Exemple:

`2026-001_ACTU_ECON_Inflation-en-recul-en-Europe_V1.docx`

Regles:

- `AAAA-NNN`: annee + numero unique global (ex: `2026-001`)
- `TYPE`: `ACTU`, `FOND`, `DOSSIER`, `TF`, `SENTIER`, `SYNTHESE`
- `THEME`: `ECON`, `POL`, `TECH`, `CLIMAT`, `SCIENCE`, `MONDE`, `CULTURE`
- `Titre-court`: mots separes par `-`, sans accents ni caracteres speciaux
- `VX`: version (`V1`, `V2`, ...)

## Statuts

- `idee`
- `brouillon`
- `en_cours`
- `pret_a_publier`
- `publie`
- `a_mettre_a_jour`
- `a_relier`
- `archive`

## Workflow minimal

1. Creer l'article source dans le bon dossier.
2. Assigner un ID unique (`AAAA-NNN`).
3. Remplir l'en-tete standard.
4. Rediger et iterer.
5. Publier manuellement dans WordPress.
6. Mettre a jour l'index (`statut`, date, URL WordPress).

## Orientation pratique

Pour penser un sujet :
- utiliser d'abord l'`architecture editoriale`

Pour un **dossier** avec plusieurs triptyques, en restant leger (tokens, controle editorial) :
- remplir d'abord le **plan de dossier** (template ci-dessus)
- puis enchainer **un triptyque par session** avec `00_Systeme/Prompts/Prompt_triptyque_v6.md`

Pour le mode de production par defaut :
- la redaction est faite par l'agent, avec qualite editoriale elevee
- si plusieurs triptyques sont necessaires, l'orchestration se fait via l'agent et ses sous-agents, pas via un backend LLM local
- les scripts techniques servent surtout a l'integration, au push WordPress et au maillage
- le pipeline API LLM reste disponible seulement en option explicite

Pour produire rapidement :
- utiliser le `triptyque` si un noyau de 3 contenus suffit

Pour produire un seul contenu :
- utiliser la methode de l'article d'actualite quotidien

Pour cadrer une question de fond sur la duree :
- utiliser les prompts de cycle editorial
