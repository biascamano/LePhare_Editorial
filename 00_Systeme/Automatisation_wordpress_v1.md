# Automatisation WordPress V1.2

## Objectif

Cette V1.2 permet de transformer un fichier source ou un dossier complet depuis `07_A_Publier` en brouillon(s) WordPress via l'API REST.

Portee :
- creation de brouillon uniquement
- pas d'image
- categories et tags automatiques depuis `index_editorial.csv`
- mise a jour optionnelle de `index_editorial.csv`
- traitement d'un repertoire complet de fichiers `.md`
- pas de publication automatique

## Fichiers

- `tools/wp_push_draft.py`
- `tools/wp_config.example.json`

## Prerequis

- Python 3 installe localement
- un compte WordPress avec Application Password active
- un fichier de config local (ne pas commiter les secrets)

## Configuration

Copier `tools/wp_config.example.json` vers un fichier local, par exemple :

`tools/wp_config.local.json`

Puis renseigner :
- `site_url`
- `username`
- `application_password`

Alternative :
utiliser des variables d'environnement :
- `LP_WP_SITE_URL`
- `LP_WP_USERNAME`
- `LP_WP_APPLICATION_PASSWORD`

## Usage

### Dry-run

Verifier l'extraction sans creer de brouillon :

```bash
python tools/wp_push_draft.py "07_A_Publier/Inflation_en_Europe_Dossier/2026-419_DOSSIER_ECON_Inflation-en-recul-en-Europe-accalmie-ou-pause_V2.md" --dry-run
```

### Dry-run sur un dossier complet

```bash
python tools/wp_push_draft.py "07_A_Publier/Inflation_en_Europe_Dossier" --dry-run --index "index_editorial.csv"
```

### Creation du brouillon

```bash
python tools/wp_push_draft.py "07_A_Publier/Inflation_en_Europe_Dossier/2026-419_DOSSIER_ECON_Inflation-en-recul-en-Europe-accalmie-ou-pause_V2.md" --config "tools/wp_config.local.json"
```

### Creation du brouillon + mise a jour de l'index

```bash
python tools/wp_push_draft.py "07_A_Publier/Inflation_en_Europe_Dossier/2026-419_DOSSIER_ECON_Inflation-en-recul-en-Europe-accalmie-ou-pause_V2.md" --config "tools/wp_config.local.json" --index "index_editorial.csv"
```

### Creation de tous les brouillons d'un dossier

```bash
python tools/wp_push_draft.py "07_A_Publier/Inflation_en_Europe_Dossier" --config "tools/wp_config.local.json" --index "index_editorial.csv"
```

### Forcer un article deja passe en `wp_draft`

```bash
python tools/wp_push_draft.py "07_A_Publier/Inflation_en_Europe_Dossier" --config "tools/wp_config.local.json" --index "index_editorial.csv" --force
```

## Ce que le script lit

Champs requis :
- `Titre`
- `Slug propose`
- contenu principal

Champs optionnels :
- `Resume court`
- `Mot-cle principal`
- `Meta-description`

## Ce que le script ignore

- bloc `# SEO`
- bloc `## Bloc image WordPress`
- bloc `## Bloc publication`

## Sortie

En `dry-run`, le script affiche :
- titre
- slug
- excerpt
- SEO
- apercu HTML pour un fichier unique
- liste resumee pour un dossier

En creation reelle, le script affiche :
- ID WordPress
- slug
- status
- link
- `index_updated` si l'option `--index` est utilisee
- un resume global `created / skipped / failed` sur un dossier

## Effet sur l'index (si `--index` est fourni)

Le script met a jour la ligne de l'article source a partir de `ID article` et renseigne :
- `Statut = wp_draft`
- `URL_WordPress`
- `Slug_WordPress`
- `Date_derniere_maj`
- `Remarques`

Si un article est deja en `wp_draft` avec une URL WordPress renseignee, il est ignore par defaut pour eviter les doublons.
Utiliser `--force` pour le repousser volontairement.

## Taxonomies WordPress

Si `--index` est fourni, le script lit aussi :
- `Categorie_WP`
- `Tags_WP`

Puis il :
- cherche les termes existants dans WordPress
- cree le terme s'il n'existe pas
- assigne categories et tags au brouillon

## Limites actuelles

- HTML volontairement simple
- pas de mise en forme WordPress avancée
- pas de featured image
- pas de suivi automatique de publication finale

## Evolution conseillee ensuite

1. upload d'image
2. suivi des statuts `wp_draft` / `publie`
3. suppression ou archivage auto dans `07_A_Publier`
4. mapping editorial plus fin des taxonomies WordPress
