# Memo - prompts courts `architecture editoriale`, `graphe editorial` et `reseau editorial`

## Principe

Le projet doit pouvoir reconnaitre des commandes editoriales tres courtes, sans obliger l'utilisateur a reexpliquer tout le systeme.

Les commandes :

- `architecture editoriale`
- `graphe editorial`
- `reseau editorial`

doivent etre interpretees comme l'appel au prompt :

- `00_Systeme/Prompts/Prompt_actualite_vers_architecture_editoriale_v1.md`

sans modifier la logique de `routine quotidienne`.

Les trois commandes sont liees :
- `architecture editoriale` est l'entree conceptuelle principale
- `graphe editorial` insiste sur la cartographie des noeuds
- `reseau editorial` insiste sur la traduction de ces noeuds en contenus

Mais elles renvoient au meme moteur editorial.

---

## Intention

Les commandes `architecture editoriale`, `graphe editorial` et `reseau editorial` ne demandent pas simplement :
- un article
- un triptyque isole
- ou une mini-encyclopedie

Elles demandent de transformer une actualite en architecture editoriale progressive :

1. identifier les noeuds du sujet
2. cartographier leurs relations
3. traduire ces noeuds en types d'articles
4. proposer un reseau editorial complet
5. extraire un triptyque minimal pertinent
6. indiquer ce qui doit enrichir la Memoire du Phare

---

## Defauts a appliquer

Quand l'utilisateur ecrit `architecture editoriale`, `graphe editorial` ou `reseau editorial`, appliquer par defaut :

- lecture de l'actualite ou du sujet fourni
- extraction de 8 a 15 noeuds maximum
- distinction entre evenement, concept, acteur, systeme, temporalite, tension, reference et piste
- proposition d'un reseau editorial de 5 a 8 contenus
- extraction d'un triptyque minimal
- articulation avec le Sentier du Savoir
- articulation avec la Memoire du Phare

Ne pas appliquer par defaut :

- la routine quotidienne complete
- la production d'une mini-encyclopedie
- la publication WordPress
- la creation immediate de tous les contenus rediges

---

## Sortie attendue

La sortie attendue pour `architecture editoriale`, `graphe editorial` ou `reseau editorial` doit contenir clairement :

1. resume editorial du sujet
2. question centrale
3. place dans le Sentier
4. couche de connaissance : noeuds
5. couche de connaissance : relations
6. couche de publication : correspondance noeuds -> types d'articles
7. parcours editorial complet
8. triptyque minimal recommande
9. prolongements pour la Memoire du Phare

---

## Variantes utiles

Peuvent etre interpretees dans le meme esprit :

- `architecture editoriale`
- `architecture editoriale sur ...`
- `architecture editoriale a partir de ...`
- `graphe editorial sur ...`
- `graphe editorial a partir de ...`
- `reseau editorial`
- `reseau editorial v2`
- `reseau editorial sur ...`
- `reseau editorial a partir de ...`

Si l'utilisateur veut ensuite passer a la redaction, l'assistant peut proposer une suite du type :

- `genere le triptyque`
- `redige le reseau de 5 contenus`
- `developpe seulement la cle de comprehension`

---

## Rappel

Le but de ce memo est :
- de conserver un prompt court et naturel
- d'eviter de reexpliquer la logique du systeme
- de garder le triptyque comme cellule de base
- de faire de `architecture editoriale` la notion principale
- de conserver `graphe editorial` et `reseau editorial` comme deux focales du meme moteur
- sans confondre ce moteur avec la routine quotidienne

---

## Variante economique : plan de dossier puis triptyques successifs

Si l'objectif est un **dossier multi-triptyques** sans passer par un enchainement technique lourd ou un gros contexte automatise :

1. Produire un **plan de dossier** court avec le gabarit `00_Systeme/Templates/Plan_dossier_triptyques_TEMPLATE.md` (voir `00_Systeme/Workflow_plan_dossier_triptyques.md`). Le nombre de triptyques n'est pas plafonne : il depend du sujet. Un **article pivot** optionnel peut relier tous les triptyques.
2. Rediger **chaque triptyque separement** avec le prompt triptyque habituel.

Cela **simule** l'architecture editoriale (question centrale, roles des blocs, liens) tout en gardant la **cellule de production** : le triptyque. Les commandes `architecture editoriale` / `graphe editorial` / `reseau editorial` restent valables pour la **phase de reflexion** ; la production peut suivre ce workflow plan + triptyques.
