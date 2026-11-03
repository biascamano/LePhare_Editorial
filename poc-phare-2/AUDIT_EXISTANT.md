# Audit de l'existant

Audit fait en lecture seule le 2026-11-03 : le dépôt `LePhare_Editorial` et l'API REST publique de le-phare.info, en GET uniquement. Les fichiers de configuration locaux qui contiennent des secrets (`tools/wp_config.local.json`, sa copie, `tools/editorial_config.local.json`) n'ont été ni lus ni ouverts.

## 1. Fichiers demandés par la mission

| Fichier | État |
|---|---|
| `tools/phare.py` | Présent (647 lignes) : l'orchestrateur, sous-commandes `next`, `start`, `etape`, `close`, `reporter`, `contexte` |
| `tools/tests/test_phare.py` | Présent (36 tests) |
| `00_Systeme/Journal_phare.csv` | Présent (60 entrées) : colonnes `horodatage, periode, activite, statut, etape, ids, note` |
| Skills Claude Code | `.claude/skills/` : routine-phare, routine-quotidienne, routine-hebdomadaire, routine-mensuelle, routine-renovation, routine-triptyque (archivée), pack-social, atelier-livre |
| Commandes et agents | `.claude/commands/` (un alias par routine) ; `.claude/agents/` : relecteur-prepublication, lecteur-critique |

**Aucun fichier demandé n'est absent.** Rien n'a été recréé.

## 2. Chaîne de publication actuelle

```
rédaction (Claude, .md) → 07_A_Publier/<dossier>/ → daily_run.py --publish-existing
   → wp_push_draft.py (Markdown → HTML maison → POST /wp/v2/posts)
   → post_linking.py (maillage) → publication → verify_publication.py (tag a-la-une, liens ?p=)
index_editorial.csv  ← append_rows_to_index (registre canonique)
```

Les 25 scripts de `tools/` à réutiliser tels quels ou à adapter :

| Rôle | Scripts |
|---|---|
| Registre | `index_editorial_utils.py`, `validate_index_editorial.py` |
| WordPress | `wp_push_draft.py`, `wp_pull_body.py`, `wp_refresh_body.py`, `verify_publication.py` |
| Maillage | `post_linking.py`, `build_hubs.py` |
| État | `build_catalogue.py`, `build_etat_courant.py`, `memoire_append.py` |
| Orchestration | `phare.py`, `daily_run.py` |

Le mode pilote est actif : tant que `00_Systeme/Mode_brouillons.md` existe, rien n'est publié en ligne. Le POC ne s'appuie sur aucun de ces scripts et n'en modifie aucun.

## 3. Formats et métadonnées

- **Registre** : `index_editorial.csv`, 22 colonnes (`ID, Titre, Type, Theme, Statut, Version, Date_creation, Date_derniere_maj, Auteur, Etape_sentier, Articles_lies, Mots_cles, Resume_court, Objectif, Nom_fichier, Chemin_dossier, Date_publication_WP, URL_WordPress, Slug_WordPress, Categorie_WP, Tags_WP, Remarques`). Dernier ID : 2026-579.
- **Articles** : Markdown avec un en-tête de métadonnées, puis un chapeau, des sections `##`, et des blocs finaux nommés : « Repères de sources », « La question suivante », « Pour aller plus loin », « Sur le Sentier du Savoir ».
- **Types** : ACTU, TF, SENTIER, FOND, DOSSIER, SYNTHESE, LIVRE. Le *format* éditorial (question, application, fil, expérimental) se lit dans les tags et catégories WordPress, pas dans `Type`.
- **WordPress** : la catégorie donne la famille (`textes-fondateurs`, `cycle`, `dossier-hebdomadaire`, `sentier-du-savoir`, `livres`, `experimental`). Les tags donnent le thème, le type (`type-question`, `type-application`), la posture et l'étape du Sentier. Le tag `a-la-une` est indispensable, sinon l'article est invisible (D15).

**Réutilisable pour le POC** : le registre et les fichiers .md suffisent à produire l'instantané `mock`, et les catégories et tags suffisent au mode `wordpress`.

## 4. Relations entre contenus

- `Articles_lies` (IDs séparés par `;`) relie les articles entre eux. Les blocs « Pour aller plus loin » et « Sur le Sentier du Savoir » en sont la version publiée.
- **Sentier** : `00_Systeme/Manifests/sentier_fondamentaux.csv` décrit 9 étapes (`etape_num, etape_nom, hub_id, fondamental_*, slug_wp, url_canonique…`). C'est la seule source structurée : WordPress n'a pas de modèle de parcours. Le POC l'utilise sans rien inventer.
- **Dossiers** : rattachés par `Articles_lies` et par la catégorie `dossier-hebdomadaire`. Pas de champ « dossier parent » dédié.
- **Fils** : suivis dans `Memoire_editoriale.md` et `Radar_editorial.md`, en texte libre, sans structure exploitable par un front.

## 5. Images

- Pas d'image dans le corps des articles.
- L'image à la une est attribuée par catégorie ou tag via `tools/wp_featured_media.local.json` (présent, non versionné, non lu). Ce sont des médias existants de la médiathèque, réutilisés.
- Le POC n'affiche aucune image : c'est une décision ouverte (voir PLAN_INTEGRATION.md §4).

## 6. Constats sur le contenu en ligne

Ces constats viennent du build du POC sur l'API publique (290 articles `a-la-une`) et de `verify-dist`. Ce sont des défauts **du contenu actuel**, pas du POC.

| # | Constat | Ampleur | Cause probable |
|---|---|---|---|
| 1 | Astérisques Markdown visibles (« Son \*Cantique des créatures\* ») | 92 pages | `wp_push_draft.py` ne convertit que `**gras**` : l'italique `*…*` part tel quel (fonction de conversion en ligne, l. 387) |
| 2 | Deux h1 par page | 25 pages | `<h1 class="wp-block-heading">` dans le contenu (ex. *science-et-societe*) : contenus anciens ou édités dans Gutenberg |
| 3 | Ancres vides `href="#"` | 15 liens | Contenus importés (ex. *verite-et-politique-hannah-arendt*) |
| 4 | Slugs des hubs du Sentier décalés par rapport aux numéros d'étape | 5 hubs | Étape 3 → `etape-3-approfondir…`, 5 → `etape-4-devenir-polyglotte…`, 7 → `etape-5-ecrire…`, 8 → `etape-7-frequenter…`, 9 → `etape-8-prendre-soin…` |
| 5 | Hub de l'étape 1 sans URL dans le manifest | 1 | — |
| 6 | Articles sans chapeau (548, 554, 558, 561, 562, 570, 571, 575…) | 10 dans l'instantané | Le POC se rabat sur le résumé |
| 7 | Articles sans « Repères de sources » (547, 576) | 2 | 576 est expérimental, 547 est à vérifier |
| 8 | Titres préfixés « Texte fondateur - », « Question du Phare - » | Récurrent | Redondant avec l'étiquette affichée au-dessus du titre ; le POC n'y touche pas |
| 9 | Pas d'espace insécable avant « ; : ? ! » | Général | Pas de traitement typographique dans la chaîne |
| 10 | `/wp-json/wp/v2/users` public | — | Expose les identifiants des auteurs : à fermer côté WordPress (hors périmètre du POC) |
| 11 | Champs Rank Math (titre et description SEO) absents de l'API | — | Le POC utilise l'extrait comme description |

## 7. Écarts entre documents et site

- **Devise** : trois formulations circulent.
  - « Éclairer sans éblouir » : proposition Le Phare 2.0.
  - « Le Phare éclaire l'actualité autrement » : `00_Systeme/Page_accueil_V5.md`.
  - « Transformer l'actualité en compréhension durable » : le logo.

  Le POC reprend la devise V5, celle qui est en ligne. L'arbitrage reste ouvert.
- **Accueil** : la V5 (`Page_accueil_V5.md`) est un flux chronologique unique de 9 articles, alors que la mission demande deux portes et pas de longue liste. Le POC suit la mission. Il reprend de la V5 les textes des blocs et le parcours « Voir l'actualité → l'interroger → la regarder autrement → la relier → en garder les outils ».
- **Charte** : la seule couleur mesurable sur le site est `--td_theme_color: #008d7f` (thème Newspaper). Les autres valeurs du POC sont dérivées ou provisoires (voir ARCHITECTURE.md §3).
