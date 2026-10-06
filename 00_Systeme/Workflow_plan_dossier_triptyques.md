# Workflow - Plan de dossier par triptyques (simulation legere de l'architecture editoriale)

## Objectif

Produire un **dossier multi-triptyques** sans passer par le mode technique `architecture_editoriale` du pipeline ni par des enchainements automatiques lourds.

Le principe :

1. **Une fois** : poser un **plan de dossier** court (question centrale, roles des triptyques, liens).
2. **Ensuite** : lancer **un triptyque a la fois** avec le prompt triptyque habituel (`Prompt_triptyque_v6.md` + consignes du sujet).

Cela **simule** l'architecture editoriale (couche de sens + parcours) tout en gardant la **cellule de production** minimale : le **triptyque**.

Avantages typiques :

- moins de tokens qu'un gros run multi-contenus automatise
- decisions editoriales visibles et stables avant redaction
- reutilisation du flux deja maitrise (triptyque + index + publication)

---

## Quand utiliser ce workflow

- Sujet qui merite **plusieurs triptyques** lies (deux, trois, ou davantage selon le sujet), sans besoin immediat de manifest JSON ni de pipeline multi-bloc.
- Dossiers **larges** : prevoyez souvent un **article pivot** (entree de dossier) qui reference tous les triptyques ; ce n'est pas obligatoire mais clarifie le parcours.
- Fin de mois / **budget tokens** serre : plan court puis executions ciblees.
- Volonte de **garder la main** sur le decoupage (fonction de chaque triptyque).

---

## Ce que ce workflow n'est pas

- Ce n'est pas une suppression du concept `architecture editoriale` : le plan reprend la **meme idee** (question, tensions, parcours), sous forme **manuelle**.
- Ce n'est pas la `routine quotidienne` : on peut l'utiliser **en plus** ou **a la place** d'un gros mode technique selon le besoin.

---

## Pipeline automatique toujours disponible (option explicite)

Si plus tard tu veux **tout generer via le script** (manifest + articles + index + copie `07_A_Publier`), le chemin technique reste :

- `tools/editorial_pipeline.py`
- `--mode architecture_editoriale` avec `--output-profile` (`triptyque_minimal`, `dossier_2_triptyques`, etc.)
- `--use-api-llm` obligatoire pour activer la generation API

Details et exemples : `00_Systeme/Automatisation_editoriale_v1.md`.

Le workflow **plan + triptyques** documente ici est la voie **agent-first** ; le pipeline est la voie **API optionnelle**, pas un remplacement supprime.

---

## Etapes

### Etape 1 - Plan de dossier (une page max)

Remplir le gabarit :

`00_Systeme/Templates/Plan_dossier_triptyques_TEMPLATE.md`

Exemple de plan deja rempli (test / inspiration) :

`00_Systeme/Templates/Plan_dossier_triptyques_EXEMPLE_rempli.md`

Minimum a figer :

- sujet source et angle
- question centrale du dossier
- **nombre de triptyques** justifie par le sujet (pas de maximum dans le gabarit)
- optionnel : **article pivot** qui reference tous les triptyques (voir section 2 bis du template)
- pour **chaque triptyque** : role intellectuel distinct, tension, ordre de lecture souhaite
- liens entre triptyques (ce que chaque bloc ajoute, ce qu'on evite de dupliquer)

### Etape 2 - Article pivot (si prevu dans le plan)

Rediger en premier ou en dernier selon ce que tu as choisi dans le plan (cadre avant redaction vs synthese apres).  
Type et ton : alignes sur `00_Systeme/Instructions_editoriales_officielles.md` et sur le type d'article retenu (ACTU synthese, entree DOSSIER, etc.).

### Etape 3 - Triptyque 1, puis triptyques suivants

Pour **chaque** triptyque, demander explicitement en citant :

- le plan (resume ou copie des lignes utiles)
- `00_Systeme/Prompts/Prompt_triptyque_v6.md`
- `00_Systeme/Instructions_editoriales_officielles.md`

Sujet du triptyque = formulation **precise** derivee du plan (pas seulement le titre general du dossier).

A chaque nouveau triptyque, rappeler :

- la question centrale du dossier
- ce que les triptyques **deja rediges** ont couvert
- ce que **ce** triptyque doit **seul** porter

### Etape 3 bis - Ancrage atelier (chaque triptyque)

Apres redaction du SENTIER :

- choisir le fondamental parent dans `00_Systeme/Manifests/sentier_fondamentaux.csv`
- marquer le SENTIER comme **atelier** (en-tete + Instructions 3.9)
- ajouter une ligne dans `## Ateliers (applications sur l'actualite)` en fin du fichier du fondamental parent

Voir `00_Systeme/Sentier_fondamentaux_referentiel.md`.

### Etape 4 - Integration

- IDs uniques dans `index_editorial.csv`
- Dossier sous `07_A_Publier` avec sous-dossiers par triptyque si besoin
- `post_linking.py` sur le dossier racine du dossier pour intra- et inter-triptyques selon votre configuration actuelle

### Etape 5 - Micro-edition

Passage de coherence transversal : ton, doublons, fil conducteur du dossier.

---

## Lien avec les prompts existants

| Besoin | Fichier |
|--------|---------|
| Cadrage large d'une actualite (noeuds, tensions) | `Prompts/Prompt_actualite_vers_architecture_editoriale_v1.md` |
| Redaction d'un triptyque | `Prompts/Prompt_triptyque_v6.md` |
| Memo commandes courtes | `Memo_prompt_court_architecture_editoriale.md` |

Pour le **plan de dossier** seul, le gabarit template suffit ; on peut optionnellement s'inspirer du prompt architecture pour la **phase de reflexion**, sans enclencher la production de tous les contenus.

---

## Formulation courte pour l'agent

Tu peux ecrire par exemple :

> Plan dossier triptyques : [coller ou resumer le template rempli]. Article pivot oui/non. Ensuite triptyque 1 seulement selon Prompt_triptyque_v6.

Puis un message par triptyque suivant :

> Meme plan, triptyque N avec les contraintes suivantes : ...

Optionnel : un message dedie a l'article pivot avant ou apres les triptyques.

Cela limite le contexte recharge a chaque fois et garde des sessions plus legeres.
