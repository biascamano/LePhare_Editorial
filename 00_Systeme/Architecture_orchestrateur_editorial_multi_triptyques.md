# Architecture technique - Orchestrateur editorial multi-triptyques

## Objectif

Definir une architecture technique ou `architecture_editoriale` devient le cerveau du systeme.

Son role n'est pas d'ecrire directement tous les contenus.
Son role est de :
- lire un sujet
- construire une architecture editoriale
- identifier plusieurs axes fertiles
- decouper ces axes en triptyques coherents
- lancer plusieurs producteurs en parallele
- consolider ensuite l'ensemble

Autrement dit :

`architecture_editoriale = orchestrateur`

`triptyque = unite de production`

`edition finale = unite de consolidation`

---

## Principe general

Le systeme doit distinguer 3 niveaux.

### 1. Niveau orchestration

Le mode `architecture_editoriale` :
- analyse le sujet
- extrait les noeuds
- repere les tensions
- choisit une strategie de couverture
- produit un manifest d'architecture

Ce niveau ne produit pas encore forcement tous les articles finaux.

### 2. Niveau production

Chaque triptyque planifie devient une tache autonome.

Chaque tache produit un bloc coherent de 3 contenus :
- `ACTU`
- `TF`
- `SENTIER`

Chaque triptyque couvre un sous-ensemble clair de noeuds.

### 3. Niveau consolidation

Une passe finale verifie :
- les recouvrements
- les contradictions inutiles
- le ton general
- les liens internes
- l'ordre de publication

---

## Pourquoi plusieurs triptyques

Le systeme ne doit pas passer trop vite de :
- 1 actualite
- a 1 dossier geant

Le bon niveau intermediaire est :
- 1 architecture editoriale
- 2 ou 3 triptyques relies

Cela permet :
- une production modulaire
- une relecture plus simple
- une publication progressive
- une meilleure reutilisation des contenus

---

## Cas d'usage cibles

### Cas 1 - Mode quotidien

Entree :
- une actualite

Sortie :
- 1 triptyque minimal

But :
- garder une routine legere

### Cas 2 - Mode dossier

Entree :
- une actualite a fort potentiel

Sortie :
- 2 ou 3 triptyques relies

But :
- couvrir plusieurs angles sans fabriquer un dossier monolithique

### Cas 3 - Mode exceptionnel

Entree :
- un sujet tres structurant

Sortie :
- 3 triptyques ou plus
- ou une autre forme composee

But :
- construire un dossier majeur ou un cycle dense

---

## Architecture logique

### Etape A - Orchestrateur

Input :
- sujet
- theme
- angle optionnel
- profil de sortie

Sortie :
- manifest d'architecture editoriale

Le manifest doit contenir :
- le cadrage general
- la couche de connaissance
- la couche de publication
- les triptyques candidats
- l'ordre de production

### Etape B - Selection

L'orchestrateur choisit ensuite :
- 1 triptyque si profil minimal
- 2 a 3 triptyques si profil dossier
- plus si profil etendu

### Etape C - Execution parallele

Chaque triptyque selectionne est envoye a un worker.

Un worker recoit :
- les noeuds qu'il doit couvrir
- la tension principale
- les liens vers les autres triptyques
- sa fonction precise dans l'ensemble

### Etape D - Consolidation

Le consolidateur recupere :
- les manifests partiels
- les articles produits
- les liens prevus

Puis il :
- detecte les doublons
- harmonise le vocabulaire
- verifie les renvois croises
- construit un ordre editorial final

---

## Schema de manifest recommande

Le mode `architecture_editoriale` doit produire un manifest plus riche que le manifest triptyque actuel.

### Schema cible

```json
{
  "source_topic": "string",
  "requested_mode": "architecture_editoriale",
  "output_profile": "triptyque_minimal|dossier_2_triptyques|dossier_3_triptyques|reseau_5_contenus",
  "theme_code": "MONDE|POL|ECON|TECH|CLIMAT|SCIENCE|CULTURE",
  "category_label": "string",
  "question_centrale": "string",
  "cycle_status": "exploratoire|critique|fondateur",
  "active_posture": "Observer|Questionner|Comprendre|Analyser|Relier",
  "architecture_summary": "string",
  "knowledge_layer": {
    "central_nodes": [],
    "nodes": [],
    "relations": [],
    "editorial_tensions": [],
    "durable_pivots": []
  },
  "publication_layer": {
    "recommended_entrypoint": "ACTU|CLE|ANALYSE",
    "content_candidates": [],
    "triptych_candidates": [],
    "recommended_triptychs": [],
    "publication_sequence": []
  },
  "guardrails": {
    "max_triptychs": 3,
    "max_overlap_ratio": 0.35,
    "require_distinct_function": true,
    "require_sentier_link": true
  }
}
```

### Format d'un noeud

```json
{
  "node_id": "string",
  "label": "string",
  "node_type": "Evenement|Concept|Acteur|Systeme|Temporalite|Tension|Reference|Piste",
  "definition": "string",
  "editorial_role": "string",
  "reuse_potential": "faible|moyen|fort"
}
```

### Format d'une relation

```json
{
  "source": "node_id",
  "relation": "explique|revele|cause|aggrave|depend_de|s_oppose_a|prolonge|historise|incarne|ralentit|accelere",
  "target": "node_id"
}
```

### Format d'un candidat contenu

```json
{
  "content_id": "string",
  "type_code": "ACTU|TF|SENTIER|CLE|ANALYSE|CHRONO|ACTEURS",
  "title": "string",
  "question": "string",
  "covered_nodes": ["node_id"],
  "editorial_function": "porte_entree|clarification|approfondissement|mise_en_tension|historicisation|exercice_critique|ouverture"
}
```

### Format d'un triptyque candidat

```json
{
  "triptych_id": "string",
  "label": "string",
  "function": "minimal|structurel|temps_long|acteurs|prospectif",
  "core_tension": "string",
  "covered_nodes": ["node_id"],
  "articles": [
    {
      "type_code": "ACTU|TF|SENTIER",
      "title": "string",
      "objective": "string",
      "summary": "string",
      "etape_sentier": "Observer|Questionner|Comprendre|Analyser|Relier"
    }
  ],
  "links_to_triptychs": ["triptych_id"],
  "recommended_order": 1
}
```

---

## Profils de sortie recommandes

Le mode `architecture_editoriale` ne doit pas tout produire de la meme facon.
Il doit accepter un profil de sortie.

### Profil 1 - `triptyque_minimal`

Sortie :
- 1 triptyque

Usage :
- mode quotidien

### Profil 2 - `dossier_2_triptyques`

Sortie :
- 2 triptyques lies

Usage :
- actualite importante
- besoin de distinguer evenement et structure

### Profil 3 - `dossier_3_triptyques`

Sortie :
- 3 triptyques lies

Usage :
- sujet avec vrai potentiel dossier

### Profil 4 - `reseau_5_contenus`

Sortie :
- 5 contenus selectionnes depuis l'architecture

Usage :
- quand le format triptyque n'est pas suffisant

---

## Modes CLI recommandes

### Etat cible

```bash
python tools/editorial_pipeline.py "Sujet..." --mode architecture_editoriale
```

Equivalent implicite :
- profil par defaut : `triptyque_minimal`

### Variantes

```bash
python tools/editorial_pipeline.py "Sujet..." --mode architecture_editoriale --output-profile triptyque_minimal
python tools/editorial_pipeline.py "Sujet..." --mode architecture_editoriale --output-profile dossier_2_triptyques
python tools/editorial_pipeline.py "Sujet..." --mode architecture_editoriale --output-profile dossier_3_triptyques
python tools/editorial_pipeline.py "Sujet..." --mode architecture_editoriale --output-profile reseau_5_contenus
```

### Compatibilite

Les anciens modes restent possibles :

```bash
python tools/editorial_pipeline.py "Sujet..." --mode triptyque
python tools/editorial_pipeline.py "Sujet..." --mode mini_encyclopedie
```

Mais a terme :
- `triptyque` devient un raccourci technique
- `architecture_editoriale` devient l'entree normale

---

## Comment lancer plusieurs agents

Oui, c'est faisable.

Il faut distinguer :
- l'orchestrateur
- les workers

### Orchestrateur

Un seul agent ou appel LLM produit le manifest d'architecture.

### Workers

Ensuite, le pipeline cree une tache par triptyque recommande.

Chaque worker recoit un sous-prompt strict :
- question centrale
- fonction du triptyque
- noeuds a couvrir
- tension principale
- etape du Sentier visee
- liens vers les autres triptyques

### Consolidateur

Une fois les workers termines :
- lire les sorties
- verifier les recouvrements
- imposer les liens croises
- preparer l'ordre de publication

---

## Deux strategies techniques possibles

### Strategie A - Multi-appels LLM dans le meme script

Le script Python :
- genere le manifest
- boucle sur les triptyques recommandes
- appelle le LLM plusieurs fois
- consolide ensuite

Avantages :
- plus simple
- plus facile a maintenir
- pas besoin d'infrastructure agent plus complexe

Limites :
- parallellisme limite
- pas de separation forte des roles

### Strategie B - Orchestrateur + sous-processus workers

Le pipeline :
- cree un manifest global
- cree un manifest par triptyque
- lance un sous-processus ou worker par triptyque
- attend les resultats
- consolide a la fin

Avantages :
- vrai parallélisme
- architecture plus propre pour monter en puissance

Limites :
- plus de code
- plus de points de reprise et de logs a gerer

### Recommandation

Commencer par la strategie A.

Pourquoi :
- elle permet deja 2 ou 3 triptyques
- elle est compatible avec l'existant
- elle limite le risque technique

Ensuite, seulement si besoin :
- passer a la strategie B

---

## Regles de decoupage en triptyques

L'orchestrateur ne doit pas inventer plusieurs triptyques au hasard.

Il doit respecter des regles.

### Regle 1 - Fonction distincte

Chaque triptyque doit avoir une fonction intellectuelle propre.

Exemples :
- triptyque 1 : evenement et lecture immediate
- triptyque 2 : causes structurelles
- triptyque 3 : temps long et reference

### Regle 2 - Recouvrement limite

Deux triptyques ne doivent pas couvrir les memes noeuds centraux au meme niveau.

Recouvrement recommande :
- inferieur a 35 %

### Regle 3 - Triptyque lisible seul

Chaque triptyque doit rester publiable seul.

### Regle 4 - Maillage obligatoire

Chaque triptyque doit savoir :
- ce qui le precede
- ce qu'il prolonge
- vers quel autre triptyque il renvoie

---

## Ordre de publication recommande

Par defaut :

1. triptyque d'entree
2. triptyque structurel
3. triptyque de temps long ou d'ouverture

Exemple :

1. `ACTU + TF + SENTIER` sur le choc immediat
2. `ACTU + TF + SENTIER` sur les causes profondes
3. `ACTU + TF + SENTIER` sur les transformations a long terme

---

## Maillage interne a prevoir

Le systeme actuel de post-linking pense surtout le triptyque unique.

Il faudra ajouter un niveau supplementaire :

### Niveau 1 - Liens internes du triptyque

Dans chaque article :
- liens vers les 2 autres contenus du meme triptyque

### Niveau 2 - Liens inter-triptyques

Dans chaque triptyque :
- un bloc "Dans cette architecture editoriale"
- liens vers les autres triptyques du dossier

### Niveau 3 - Liens pivots

Dans chaque contenu :
- 1 concept pivot
- 1 texte fondateur pivot
- 1 etape du Sentier

---

## Plan d'implementation progressif

### Palier 1 - Ce qui existe deja

- `architecture_editoriale` comme mode conceptuel par defaut
- execution technique encore resolue en `triptyque`

### Palier 2 - A faire ensuite

Creer un vrai `manifest d'architecture editoriale`.

Sans encore lancer plusieurs workers.

Sortie :
- architecture globale
- triptyque recommande

### Palier 3 - A faire apres

Ajouter `--output-profile`.

Permettre :
- `triptyque_minimal`
- `dossier_2_triptyques`
- `dossier_3_triptyques`

### Palier 4 - A faire ensuite

Produire plusieurs triptyques depuis le meme manifest.

Dans un premier temps :
- execution sequentielle

### Palier 5 - A faire ensuite

Passer a une execution parallele reelle.

### Palier 6 - A faire ensuite

Ajouter un consolidateur final :
- dedoublonnage
- ordre de publication
- maillage inter-triptyques

---

## Recommendation finale

Oui, `architecture_editoriale` peut devenir un orchestrateur multi-triptyques.

Mais la bonne trajectoire est :

1. `architecture_editoriale` comme cerveau
2. `triptyque` comme unite de production
3. `2 ou 3 triptyques` comme premier niveau de dossier
4. `consolidation finale` avant publication

Le meilleur prochain pas technique n'est donc pas de lancer tout de suite beaucoup d'agents.

Le meilleur prochain pas est :

- creer le manifest d'architecture editoriale
- ajouter `--output-profile`
- puis faire `dossier_2_triptyques`

C'est le point d'equilibre le plus robuste entre ambition et simplicite.
