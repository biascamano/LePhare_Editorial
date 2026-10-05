# Taxonomie WordPress - reference canonique projet Le Phare Editorial

Ce document fixe la **meilleure structure pour l'objectif** : construire petit a petit un **graphe de savoir**, nourrir l'**encyclopedie** (savoir relatif + absolu), le **Sentier du savoir** et le **moteur editorial**, tout en restant compatible avec la publication sur [le-phare.info](https://le-phare.info/).

**Tu peux ajuster la strategie du site et les categories/tags WordPress** : quand le site diverge, mets a jour ce fichier ou les champs `Categorie_WP` / `Tags_WP` dans `index_editorial.csv` pour **realigner**. Ce depot reste la **source de verite** pour la redaction et les scripts.

---

## 1. Objectif prioritaire (pourquoi ces regles)

| Objectif | Ce que la taxonomie doit permettre |
|----------|-----------------------------------|
| Graphe de savoir | Retrouver et relier les **concepts** dans le temps (tags stables + reutilisation). |
| Encyclopedie | Separer **actualite** (relatif) et **fond / methode** (plus absolu) via **categories** claires. |
| Sentier | Chaque contenu **ancre** une posture ou un theme Sentier **dans les tags**, pas seulement dans le texte. |
| Moteur editorial | Peu de categories, vocabulaire de tags **discipline** pour eviter le bruit. |

---

## 2. Categories WordPress : six familles seulement

**Une categorie principale par article.** Pas de double categorie pour un meme post dans la logique redactionnelle (le site peut avoir des plugins ; ici on simplifie).

| # | Categorie (slug conseille) | Quand l'utiliser |
|---|----------------------------|------------------|
| 1 | **actualites** | ACTU, decryptages, faits contextualises. |
| 2 | **textes-fondateurs** | TF, lectures d'auteurs, concepts ancres par une reference. |
| 3 | **sentier-du-savoir** | SENTIER, exercices de methode, outils cognitifs, articles du parcours Sentier. |
| 4 | **dossier-hebdomadaire** | DOSSIER, series, volets d'un dossier nomme (routine mensuelle). |
| 5 | **syntheses** | SYNTHESE : Fil du Phare (routine hebdomadaire), synthese mensuelle (routine mensuelle). Creee a la volee par `wp_push_draft` au 1er push. |
| 6 | **le-phare** | Pages institutionnelles, charte, methode (rarement des articles de fond). |

La categorie existante `cycle` (id 97, « Dossier hebdomadaire - Notre fil rouge ») n'est **pas utilisee** pour l'instant (voir `plan.md`, backlog B1).

**Correspondance routines / types** (detail : `plan.md`) :

| Routine | Type article | Code index | Categorie WP |
|---------|--------------|-----------|--------------|
| Quotidienne | Actualite / Question / Application | ACTU | actualites |
| Quotidienne (occasionnel) ou mensuelle | Texte fondateur | TF | textes-fondateurs |
| Hebdomadaire | Fil du Phare | SYNTHESE | syntheses |
| Mensuelle | Dossier | DOSSIER | dossier-hebdomadaire |
| Mensuelle | Atelier Sentier | SENTIER | sentier-du-savoir |
| Mensuelle | Synthese mensuelle | SYNTHESE | syntheses |
| Triptyque (archive, `routine triptyque`) | ACTU + TF + SENTIER | ACTU / TF / SENTIER | actualites / textes-fondateurs / sentier-du-savoir |

Si WordPress impose un libelle legerement different (accents, pluriel), **garde** la correspondance dans l'index avec le slug reel du site.

---

## 3. Tags : quatre couches (empilement)

Les tags servent le **graphe**. Ordre de priorite quand tu en remplis :

### Couche A — Theme editorial (obligatoire pour tout article de routine)

Un tag issu du **theme** Le Phare (aligne sur `Theme` dans l'index) :

| Code index | Tag slug |
|------------|----------|
| MONDE | `monde` |
| POL | `politique-societe` |
| ECON | `economie-finance` |
| TECH | `technologie-ia` |
| CLIMAT | `environnement-climat` |
| SCIENCE | `science-sante` |
| CULTURE | `culture-philosophie` |

### Couche B — Pilier Sentier (obligatoire pour SENTIER ; recommande pour ACTU/TF si le sujet s'y prete)

Un parmi les **huit themes** Sentier du site :

`sentier-culture` | `sentier-critique` | `sentier-approfondissement` | `sentier-langues` | `sentier-science` | `sentier-transmission` | `sentier-vision` | `sentier-equilibre`

### Couche C — Concepts (cœur du graphe)

2 a 5 tags **reutilisables** : mots du sujet qui pourront servir a d'autres articles (`inflation`, `biais-cognitifs`, `transition-energetique`, `ordre-maritime`, …).  
**Slug** : minuscules, tirets, pas d'accents si possible (aligne sur les habitudes WP).

### Couche D — Meta (optionnel, avec parcimonie)

- **Posture** (les cinq temps de la methode homepage) : `posture-observer` | `posture-comprendre` | `posture-distance` | `posture-relier` | `posture-transmettre` — utile si tu veux filtrer la progression sans tout melanger dans les concepts.
- **Format** : `triptyque` si tu veux un filtre transversal (un seul tag, pas besoin de repeter par article).
- **Type d'article (routines v3)** : `type-actualite` | `type-question` | `type-application` | `type-texte-fondateur`.
- **Fil commun** : `question-du-phare` sur tout article portant une Question du Phare (quotidien, Fil du Phare, synthese mensuelle).
- **Syntheses** : `fil-du-phare` + `synthese-hebdomadaire` (Fil du Phare) ; `synthese-mensuelle` (synthese du mois).

**Plafond pratique** : **8 tags maximum** par article pour rester lisible ; **4 minimum** si on compte A + B + au moins 2 concepts.

---

## 4. Regles rapides par type d'article

| Type | Categorie | Tags minimum |
|------|-----------|--------------|
| ACTU | actualites | theme (A) + 2 concepts (C) ; + pilier Sentier (B) si l'article le permet |
| TF | textes-fondateurs | theme (A) + auteur ou titre d'oeuvre en concept (C) + 1 concept (C) |
| SENTIER | sentier-du-savoir | theme (A) + pilier Sentier (B) + 2 concepts (C) ; + posture (D) si pertinent |
| DOSSIER | dossier-hebdomadaire | theme (A) + 2 concepts (C) ; + pilier Sentier (B) si pertinent |
| SYNTHESE (Fil du Phare) | syntheses | `fil-du-phare` + `question-du-phare` + `synthese-hebdomadaire` (D) + theme dominant (A) ; concepts (C) dans la limite des 8 tags |
| SYNTHESE (mensuelle) | syntheses | `synthese-mensuelle` + `question-du-phare` (D) + theme dominant (A) + concepts (C) |

Routines v3 (quotidienne) : ajouter le tag de type (D) et `question-du-phare` en plus des minimums ACTU / TF.

---

## 5. index_editorial.csv et WordPress

- `Categorie_WP` : **un** libelle ou slug correspondant a la categorie principale.
- `Tags_WP` : **separateur point-virgule** `;` comme dans l'existant, dans l'ordre A puis B puis C puis D si utile.
- A la publication (`wp_push_draft.py`), les termes sont **creees ou associes** selon les slugs : garde une **cohérence** entre index et admin WP.

### Snapshot des categories WordPress (export automatique)

L'API REST publique `GET /wp-json/wp/v2/categories` liste toutes les categories (pagination automatique). Pour regenerer un fichier dans le depot :

```bash
python tools/fetch_wp_categories.py --csv-out 00_Systeme/Manifests/wp_categories_snapshot.csv
```

JSON complet optionnel : `--json-out CHEMIN`. Autre site : `--site-url https://example.com`. Colonnes CSV : `id`, `count`, `parent`, `slug`, `name`.

### Snapshot des tags WordPress (export automatique)

Meme principe avec `GET /wp-json/wp/v2/tags` :

```bash
python tools/fetch_wp_tags.py --csv-out 00_Systeme/Manifests/wp_tags_snapshot.csv
```

Colonnes CSV : `id`, `count`, `slug`, `name`. Options `--json-out` et `--site-url` comme pour les categories.

### Import inverse : tous les articles WordPress vers le depot

Script authentifie (`tools/wp_config.local.json`), pagination REST `posts`, classes les fichiers selon les categories WP (`tools/import_wp_posts.py`). Conversion HTML vers Markdown **simple** (recuperation de texte, pas une reproduction pixel-perfect des blocs Gutenberg).

```bash
python tools/import_wp_posts.py --dry-run
python tools/import_wp_posts.py --apply
python tools/import_wp_posts.py --apply --limit 50
python tools/import_wp_posts.py --apply --refresh-existing
```

- Nouveau contenu : cree `{ROOT}/{Chemin_dossier}/{Nom_fichier}` et **ajoute** une ligne a `index_editorial.csv` (backup `.csv.bak_import_*` avant ecriture).
- Slug deja present dans l'index (y compris variantes `-2`) ou URL `?p=` connue : **ignore** par defaut ; `--refresh-existing` re-ecrit le `.md` depuis WP sans dupliquer l'index.
- Ajuster les regles de routage : dictionnaires `THEME_*` et fonction `resolve_routing()` dans le script.

### Images de presentation (featured) sans multiplication des assets

Objectif : **une meme piece jointe WordPress** pour plusieurs articles, selon **categorie** puis **tag**, uniquement comme **image a la une** — pas dans le HTML du contenu pousse par `wp_push_draft.py`.

1. Reutiliser des visuels deja charges dans la mediatheque WordPress (pas besoin d'en dupliquer par article).
2. Dans `tools/wp_featured_media.local.json`, associer des slugs soit a un **ID numerique** de media, soit au **nom de fichier** dans l'URL (ex. `economie.png`). Le script interroge l'API REST (`/wp/v2/media`) si besoin. **Pour l instant** on privilegie **`by_tag_slug`** (themes, piliers Sentier, etc.) ; `by_category_slug` reste optionnel (vide par defaut dans le modele). Ordre technique au push : categorie si une entree est renseignee, sinon **tags dans l'ordre `Tags_WP`** de l'index, puis `default_media_id`.
3. Éditer `tools/wp_featured_media.local.json` (cartographie par tags, `by_category_slug` optionnel) ; à défaut, partir de `tools/wp_featured_media.local.example.json` comme squelette vide ; compléter `by_tag_slug` avec les tags concepts (couche C) au besoin.
4. Lors du push, `wp_push_draft.py` lit ce fichier automatiquement si present ; desactiver avec `--no-featured-media` ou surcharger le chemin avec `--featured-media-map`. En `--dry-run`, si la carte contient des noms de fichiers, une connexion authentifiee charge la config pour resoudre les IDs dans l'apercu JSON.

Les cles sont les **slugs** correspondant aux libelles `Categorie_WP` et `Tags_WP` apres normalisation interne (voir `_readme` dans l exemple JSON).

---

## 6. Si tu changes le site plus tard

- **Strategie editoriale** : adapte ce fichier en premier ou ajoute une section "ecarts volontaires".
- **Categories WP** : mets a jour le tableau section 2 (familles et correspondance routines / types) puis `plan.md`.
- **Tags** : fusionne les doublons dans WP puis **remplace** dans l'index par lots (rechercher/remplacer prudent).

---

## 7. Liens utiles

- Site : [le-phare.info](https://le-phare.info/)
- Strategie routine + graphe : `Strategie_routine_quotidienne_graphe_taxonomie_WP.md`
- Plan de reference des routines : `plan.md` (racine du depot)
- Routines v3 : `.claude/skills/routine-quotidienne/SKILL.md`, `routine-hebdomadaire/SKILL.md`, `routine-mensuelle/SKILL.md`
- Routine triptyque (archive) : `Routine_quotidienne.md`
