# README - Prompts editoriaux

## Objectif

Ce document clarifie quels prompts sont actuellement :
- canoniques
- utiles mais secondaires
- herites ou redondants

Le but n'est pas de supprimer brutalement les anciens prompts, mais de rendre le systeme lisible.

---

## 1. Prompt canonique principal

### `Prompt_actualite_vers_architecture_editoriale_v1.md`

Statut :
- canonique
- point d'entree principal pour transformer une actualite en systeme editorial

Role :
- fusionne la logique de graphe editorial et de reseau editorial
- distingue une couche de connaissance et une couche de publication
- extrait un triptyque minimal a partir d'une architecture plus large
- articule le tout avec le Sentier du Savoir et la Memoire du Phare

A utiliser quand on veut :
- partir d'une actualite
- structurer les noeuds du sujet
- choisir les types d'articles a produire
- definir un parcours editorial coherent

Commandes courtes associees :
- `architecture editoriale`
- `graphe editorial`
- `reseau editorial`

Memo associe :
- `00_Systeme/Memo_prompt_court_architecture_editoriale.md`

---

## 1 bis. Workflow plan dossier + triptyques successifs (recommande pour multi-triptyques leger)

Fichiers :
- `00_Systeme/Workflow_plan_dossier_triptyques.md`
- `00_Systeme/Templates/Plan_dossier_triptyques_TEMPLATE.md`

Role :
- simuler l'architecture editoriale par un **plan une page** puis **un triptyque a la fois** (`Prompt_triptyque_v6.md`)
- reduire la charge de tokens et garder la main sur le decoupage

A utiliser quand :
- le sujet merite **plusieurs triptyques** lies (nombre a arbitrer selon le sujet ; article pivot optionnel pour relier le dossier)
- on prefere eviter le mode pipeline `architecture_editoriale` pour la production redigee

---

## 2. Prompts actifs et utiles

### `Prompt_triptyque_v6.md`

Statut :
- actif
- utile

Role :
- produire un triptyque dans une logique de cycle editorial
- garder le lien avec une posture du Sentier

A utiliser quand on veut :
- rediger un triptyque comme cellule de base
- rester dans une logique de cycle deja cadre

### `Prompt_article_actualite_quotidien.md`

Statut :
- actif
- utile

Role :
- produire un article d'actualite structure selon la methode Le Phare

A utiliser quand on veut :
- rediger un seul article
- travailler un sujet sans enclencher toute l'architecture editoriale

### `Prompt_cycle_editorial_creation.md`

Statut :
- actif
- utile

Role :
- definir un cycle editorial de comprehension
- poser une question centrale et une progression sur le Sentier

A utiliser quand on veut :
- construire un cycle avant de produire les contenus

### `Prompt_cadrage_cycle_editorial_v6.md`

Statut :
- actif
- utile

Role :
- cadrer plus brievement un cycle editorial
- poser un cadre avant detail de production

A utiliser quand on veut :
- fixer l'intention d'un cycle sans entrer dans tous les details

---

## 3. Prompts utiles mais secondaires

### `Prompt_actualite_vers_5_contenus.md`

Statut :
- secondaire
- encore utile comme format borne

Role :
- produire rapidement un petit ensemble editorial predetermine

Limite :
- moins souple que l'architecture editoriale
- moins bon pour penser les noeuds et la reutilisation

### `Prompt_actualite_vers_10_contenus.md`

Statut :
- secondaire
- encore utile comme format borne

Role :
- produire un ensemble plus large de contenus deja typologises

Limite :
- logique de liste plus que logique d'architecture

### `Prompt_actualite_vers_ecosysteme_15_20_contenus.md`

Statut :
- secondaire
- utile pour exploration large

Role :
- pousser un sujet vers un ecosysteme editorial etendu

Limite :
- plus lourd
- a ne pas utiliser par defaut

### `Prompt_actualite_vers_mini_encyclopedie_30_50_pages.md`

Statut :
- secondaire
- usage exceptionnel

Role :
- produire un dossier tres vaste sur un sujet a fort potentiel

Limite :
- trop lourd pour le quotidien
- ne doit pas remplacer l'architecture editoriale courante

---

## 4. Prompts herites ou redondants

### `Herites/Prompt_actualite_vers_graphe_de_savoir.md`

Statut :
- herite
- conceptuellement absorbe

Pourquoi :
- la logique de graphe existe maintenant dans `Prompt_actualite_vers_architecture_editoriale_v1.md`
- utile surtout comme trace d'evolution du systeme

### `Herites/Prompt_reseau_editorial_depuis_actualite.md`

Statut :
- herite
- conceptuellement absorbe

Pourquoi :
- la logique de reseau editorial existe maintenant dans `Prompt_actualite_vers_architecture_editoriale_v1.md`
- utile surtout comme antecedent historique

### `Herites/Prompt_actualite_vers_graphe_et_reseau_editorial_v2.md`

Statut :
- intermediaire
- conserve comme etape de transition

Pourquoi :
- ce prompt a servi de pont entre les deux notions
- il est maintenant remplace, conceptuellement, par `Prompt_actualite_vers_architecture_editoriale_v1.md`

### `Herites/Prompt_editorial_final_triptyque.md`

Statut :
- herite ou experimental

Pourquoi :
- prompt plus massif, plus demonstratif, plus charge en modules
- utile comme reserve d'idees ou version etendue
- moins lisible comme standard courant que `Prompt_triptyque_v6.md`

### `Herites/Prompt_avance_moteur_editorial_du_phare.md`

Statut :
- herite ou transversal

Pourquoi :
- document interessant pour comprendre l'intention du moteur editorial
- moins net comme prompt standard d'usage quotidien

---

## 5. Regle simple d'usage

Utiliser par defaut :
- `Prompt_actualite_vers_architecture_editoriale_v1.md` pour penser un sujet comme systeme editorial
- `Prompt_triptyque_v6.md` pour produire un triptyque
- `Prompt_article_actualite_quotidien.md` pour produire un seul article
- `Prompt_cycle_editorial_creation.md` ou `Prompt_cadrage_cycle_editorial_v6.md` pour penser un cycle

Garder comme bibliotheque secondaire :
- `Prompt_actualite_vers_5_contenus.md`
- `Prompt_actualite_vers_10_contenus.md`
- `Prompt_actualite_vers_ecosysteme_15_20_contenus.md`
- `Prompt_actualite_vers_mini_encyclopedie_30_50_pages.md`

Garder comme historique ou transition :
- `Herites/Prompt_actualite_vers_graphe_de_savoir.md`
- `Herites/Prompt_reseau_editorial_depuis_actualite.md`
- `Herites/Prompt_actualite_vers_graphe_et_reseau_editorial_v2.md`
- `Herites/Prompt_editorial_final_triptyque.md`
- `Herites/Prompt_avance_moteur_editorial_du_phare.md`

---

## 6. Prochaine etape possible

Si besoin, on pourra faire un second niveau de menage documentaire :
- les prompts herites sont maintenant regroupes dans `Herites`
- ajouter en tete de chaque ancien prompt une ligne de statut
- mettre a jour les documents systeme qui parlent encore seulement de `triptyque` ou de `mini_encyclopedie`

Pour l'instant, les prompts herites ont ete deplaces dans `Herites` pour alleger la racine du dossier `Prompts`.
