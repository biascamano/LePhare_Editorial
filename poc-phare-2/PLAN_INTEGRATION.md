# Plan d'intégration

Rien de ce plan n'est engagé. Il attend la validation du POC. `tools/phare.py`, les skills et les routines n'ont pas été modifiés.

## 1. Étapes proposées

| # | Étape | Contenu | Touche à l'existant ? |
|---|---|---|---|
| 0 | Validation du POC | Lecture des pages, arbitrage des décisions du §4 | Non |
| 1 | Corrections de contenu, indépendantes du front | Voir le détail ci-dessous | **Oui** : `tools/` et WordPress, chacune sur décision séparée |
| 2 | Source unique | Remplacer l'instantané par une lecture directe du dépôt au build, sous la forme d'un loader de contenu Astro qui lit `index_editorial.csv` et les .md. Le mock actuel en est le prototype | Non (lecture seule) |
| 3 | Images | Choisir la politique (§4), puis l'ajouter au contrat (`Article.image`) | Non |
| 4 | Préproduction | Déploiement statique sur `test.le-phare.info` (multisite OVH Perso, dossier `poc-phare-2`), `noindex` et mot de passe : outillé, voir DEPLOIEMENT_OVH.md | DNS : **décision du fondateur** |
| 5 | Branchement sur la chaîne | Voir le §2 | **Oui** : routines |
| 6 | Bascule | Mêmes URLs `/<slug>/` : canonical, sitemap, redirections des hubs décalés (AUDIT §6.4) | Hébergement et DNS |

Détail des corrections de l'étape 1 :
- italiques dans `wp_push_draft.py` : 92 pages concernées ;
- h1 dans les contenus ;
- ancres `href="#"` ;
- fermeture de `/wp/v2/users` ;
- hub de l'étape 1.

## 2. Impact sur l'orchestrateur

**Aujourd'hui : aucun.** Le POC lit le dépôt et l'API ; il n'écrit nulle part hors de `poc-phare-2/`.

À l'étape 5, l'impact serait le suivant. Ce sont des propositions, rien n'est codé :

- **Publication** : l'étape « publier » de chaque routine (`daily_run.py --publish-existing`) resterait inchangée tant que WordPress est le site public. Ensuite, il suffirait d'ajouter **après** elle une étape « reconstruire le front » (`npm run build` puis un dépôt des fichiers statiques). Un build complet prend environ 0,5 s pour 52 pages et environ 10 s pour 290 pages depuis l'API ; depuis le dépôt, il serait plus rapide.
- **`phare.py`** :
  - pas de nouvelle activité ; la reconstruction serait une conséquence de `close` avec le statut `publie` ;
  - une option : une étape `front` dans `ETAPES`, pour que le journal trace l'échec d'un build ;
  - `test_phare.py` (36 tests) serait à compléter en conséquence.
- **Mode brouillons** : tant que `00_Systeme/Mode_brouillons.md` existe, la reconstruction se ferait en préproduction seulement.
- **`verify_publication.py`** : la règle `a-la-une` (D15) ne serait plus nécessaire au front, qui pourrait lire le `Statut` du registre. Elle reste en vigueur tant que WordPress affiche le site.
- **Rédaction** : aucun changement de format. Le front s'appuie sur les blocs déjà normés : chapeau, `##`, « Repères de sources », « La question suivante », « Pour aller plus loin », « Sur le Sentier du Savoir ». Il en tirerait parti si `Objectif` et la question du Phare restaient renseignés systématiquement.

## 3. Risques

| Risque | Parade |
|---|---|
| Deux sites divergent pendant la transition | Une seule source (le dépôt) et un build déclenché par la publication |
| Explorer grossit avec le corpus (410 Ko à 290 articles) | Index JSON chargé à la demande ou pagination par famille, avant la bascule |
| Contenus anciens hétérogènes (sans chapeau ni sections) | La rénovation (`routine renovation`) les remet au format ; le front les affiche déjà en mode dégradé, sans casse |
| Perte de fonctions WordPress (commentaires, recherche, Rank Math, newsletter) | À inventorier avant l'étape 6 ; aucune n'est reprise dans le POC |

## 4. Décisions ouvertes

1. **Source du front** : le dépôt (recommandé, ARCHITECTURE §2) ou l'API WordPress.
2. **Devise** : « Le Phare éclaire l'actualité autrement » (V5, reprise dans le POC), « Éclairer sans éblouir » ou celle du logo.
3. **Charte** : seul le teal `#008d7f` est relevé. Les fonds, l'ambre, l'encre et les polices sont à valider ou à remplacer.
4. **Images** : aucune (sobriété), images à la une par thème (le mécanisme actuel), ou image par article.
5. **Accueil** : deux portes sans chronologie (POC) ou maintien d'un flux récent court. La V5 et la mission divergent.
6. **Titres préfixés** (« Texte fondateur - … ») : à garder, ou à retirer à la source en laissant l'étiquette porter le format.
7. **Hubs du Sentier** : corriger les slugs décalés (avec redirections) ou les garder tels quels.
8. **Hébergement** : statique (CDN ou hébergeur actuel), et place de WordPress ensuite (back-office seul ou retrait).
9. **Typographie** : ajouter les espaces insécables françaises au build, ou à la rédaction.
