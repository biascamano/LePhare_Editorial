# Automatisation editoriale V1

## Objectif

Cette V1 lance un pipeline editorial complet a partir d'un sujet d'actualite.

Important :

Cette documentation decrit la mecanique technique actuellement disponible dans le pipeline.
Elle ne remplace pas la nouvelle logique conceptuelle du projet, qui est desormais formulee en termes d'`architecture editoriale`.

Important aussi :

Par defaut, la redaction editoriale ne doit pas partir sur un backend API.
Le mode normal du projet est une redaction assistee par l'agent.
Le pipeline technique avec backend LLM compatible OpenAI API reste disponible, mais seulement comme option explicite.

Autrement dit :
- le pipeline V1 pense desormais en `architecture_editoriale`
- mais le mode normal du projet reste une orchestration agent-first
- `output_profile` cadre le manifest et l'organisation editoriale, pas un systeme local de sous-agents Python

Etat actuel :
- `triptyque_minimal` est pleinement executable
- `dossier_2_triptyques` devient le premier profil multi-triptyques reellement genere
- en multi-triptyques, la voie normale est `agent orchestrateur -> sous-agents redacteurs -> scripts d'integration`
- le maillage automatique WordPress peut ensuite etre complete par `post_linking.py`

Workflow agent-first **sans** s'appuyer sur le pipeline multi-bloc pour la redaction : voir `00_Systeme/Workflow_plan_dossier_triptyques.md` (plan de dossier puis triptyques successifs).

Modes disponibles :
- `architecture_editoriale`
- `triptyque`
- `mini_encyclopedie`

Profils de sortie disponibles :
- `triptyque_minimal`
- `dossier_2_triptyques`
- `dossier_3_triptyques`
- `reseau_5_contenus`

Le mode `triptyque` genere :

- generation d'un manifest editorial `triptyque`
- generation de 3 articles locaux :
  - `ACTU`
  - `TF`
  - `SENTIER`
- ajout dans `index_editorial.csv`
- duplication dans `07_A_Publier`
- push optionnel vers WordPress en brouillons

Le mode `mini_encyclopedie` genere :

- generation d'un manifest editorial `mini_encyclopedie`
- generation d'un dossier unique de type `DOSSIER`
- ajout dans `index_editorial.csv`
- duplication dans `07_A_Publier`
- push optionnel vers WordPress en brouillons

Le pipeline technique optionnel s'appuie sur :
- `00_Systeme/Instructions_editoriales_officielles.md`
- les prompts de `00_Systeme/Prompts`
- en priorite, sur `00_Systeme/Prompts/Prompt_actualite_vers_architecture_editoriale_v1.md` pour le cadrage conceptuel
- un backend LLM compatible OpenAI API

## Fichiers

- `tools/editorial_pipeline.py`
- `tools/editorial_config.example.json`
- `tools/wp_push_draft.py`

## Prerequis

Pour le workflow par defaut :
- l'agent redige directement les contenus
- les scripts servent surtout a l'integration locale, au push WordPress et au maillage

Pour le pipeline API optionnel :

- Python 3 installe localement
- un acces API LLM compatible OpenAI
- un fichier de config local pour le LLM
- optionnel : un fichier `tools/wp_config.local.json` pour pousser les brouillons WordPress

## Configuration LLM

Copier :

`tools/editorial_config.example.json`

vers un fichier local, par exemple :

`tools/editorial_config.local.json`

Puis renseigner :

- `base_url`
- `api_key`
- `model`
- `temperature`

Alternative :

utiliser les variables d'environnement :
- `LP_LLM_BASE_URL`
- `LP_LLM_API_KEY`
- `LP_LLM_MODEL`
- `LP_LLM_TEMPERATURE`

## Ce que fait le pipeline

### 1. Manifest editorial

Le script genere un fichier JSON dans :

`00_Systeme/Manifests`

Ce manifest contient :
- la question du cycle
- la posture active du Sentier
- le role du triptyque
- les 3 articles a produire

Dans cette V1 :
- le manifest peut deja etre enrichi en mode `architecture_editoriale`
- le script Python peut encore generer plusieurs blocs en mode API explicite
- mais l'orchestration reelle par workers GPT-5.4 releve de l'agent, pas du script

### 2. Generation locale

Le script genere ensuite 3 fichiers `.md` dans l'arborescence editoriale :
- `01_Actualites/...`
- `04_Textes_fondateurs/Auteurs`
- `05_Sentier/...`

Puis il :
- ajoute les lignes correspondantes a `index_editorial.csv`
- copie les fichiers dans un dossier dedie sous `07_A_Publier`

En mode `architecture_editoriale` multi-triptyques :
- l'orchestrateur produit d'abord un manifest global enrichi
- l'agent peut ensuite deleguer un brief par triptyque a des sous-agents redacteurs
- chaque sous-agent genere son bloc `ACTU + TF + SENTIER` de facon coherente
- une consolidation finale enrichit les metadonnees des articles avec les informations de triptyque et d'architecture

### 3. Push WordPress

Si l'option `--publish-drafts` est fournie, le script appelle ensuite :

`tools/wp_push_draft.py`

sur le dossier cree dans `07_A_Publier`.

## Usage

### Generer seulement le manifest d'architecture editoriale via API

```bash
python tools/editorial_pipeline.py "L'usage de l'IA generative dans les services publics europeens" --mode architecture_editoriale --output-profile triptyque_minimal --config "tools/editorial_config.local.json" --use-api-llm --manifest-only
```

### Generer un manifest de mini-encyclopedie via API

```bash
python tools/editorial_pipeline.py "Guerre usa israel iran" --mode mini_encyclopedie --config "tools/editorial_config.local.json" --use-api-llm --manifest-only
```

### Generer le triptyque minimal local depuis l'architecture editoriale via API

```bash
python tools/editorial_pipeline.py "L'usage de l'IA generative dans les services publics europeens" --mode architecture_editoriale --output-profile triptyque_minimal --config "tools/editorial_config.local.json" --use-api-llm
```

### Generer puis pousser en brouillons WordPress via API

```bash
python tools/editorial_pipeline.py "L'usage de l'IA generative dans les services publics europeens" --mode architecture_editoriale --output-profile triptyque_minimal --config "tools/editorial_config.local.json" --use-api-llm --publish-drafts --wp-config "tools/wp_config.local.json"
```

### Generer une mini-encyclopedie puis la pousser en brouillon WordPress via API

```bash
python tools/editorial_pipeline.py "Guerre usa israel iran" --mode mini_encyclopedie --config "tools/editorial_config.local.json" --use-api-llm --publish-drafts --wp-config "tools/wp_config.local.json"
```

### Generer un dossier de 2 triptyques via API

```bash
python tools/editorial_pipeline.py "L'usage de l'IA generative dans les services publics europeens" --mode architecture_editoriale --output-profile dossier_2_triptyques --config "tools/editorial_config.local.json" --use-api-llm
```

### Forcer un theme editorial via API

```bash
python tools/editorial_pipeline.py "L'usage de l'IA generative dans les services publics europeens" --theme TECH --config "tools/editorial_config.local.json" --use-api-llm
```

## Sorties attendues

Le pipeline produit :
- un manifest JSON
- 1 ou plusieurs fichiers markdown prets a relire selon le mode
- 1 ou plusieurs nouvelles lignes dans `index_editorial.csv`
- un dossier de publication dans `07_A_Publier`
- optionnellement : 1 ou plusieurs brouillons WordPress

## Limites actuelles

- pas d'ingestion automatique d'URL ou de sources web
- pas de verification factuelle automatique des sources
- pas de validation editoriale bloquante avant publication
- pas d'image uploadee vers WordPress
- le script local ne sait pas lancer des sous-agents GPT-5.4 de lui-meme
- `dossier_3_triptyques` reste plus ambitieux et devra etre davantage eprouve en conditions reelles
- `reseau_5_contenus` n'est pas encore pleinement execute comme sortie distincte
- la consolidation reste legere : elle prepare surtout le terrain pour le maillage et l'ordre editorial

## Evolution conseillee ensuite

1. accepter un article source ou une URL en entree
2. ajouter une etape de validation editoriale automatique
3. etendre la logique de `dossier_2_triptyques` vers `dossier_3_triptyques`
4. faire evoluer `post_linking.py` vers un maillage inter-triptyques
5. conserver `triptyque` comme mode simple de production rapide
6. ajouter la publication finale automatique
