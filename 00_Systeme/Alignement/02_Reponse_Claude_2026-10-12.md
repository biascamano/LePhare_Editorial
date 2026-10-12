# Réponse de Claude au message 2/6 (Sentier du Savoir) — 12 octobre 2026

*Audit en lecture seule. Aucune routine ni aucune configuration n'a été modifiée. Seuls le message et cette réponse sont archivés dans `00_Systeme/Alignement/`. Sources : `index_editorial.csv`, `00_Systeme/Manifests/sentier_fondamentaux.csv`, `00_Systeme/Sentier_fondamentaux_referentiel.md`, `plan.md`, les scripts de `tools/` et l'historique git.*

## 1. Cartographie réelle du Sentier

Le manifeste décrit 9 étapes. Chacune a un hub et 10 fondamentaux.

| Étape | Hub | Fondamentaux | Emplacement | Anomalies |
|---|---|---|---|---|
| 1 | 413 | 212 à 205, 203, 220 | `02_Fonds` | Le hub n'a **pas d'URL**. Le slug du 220 commence par « ia-philosophie… ». |
| 2 | 059 | 202 à 193 | **`05_Sentier/Critique_Analyse`** (type SENTIER) | — |
| 3 | 060 | 191 à 182 | `02_Fonds` | Le slug du hub est `etape-3-approfondir-…`, alors que l'étape 3 traite de l'argumentation. |
| 4 | 061 | 181 à 172 | `02_Fonds` | — |
| 5 | 062 | 171 à 162 | `02_Fonds` | Le slug du hub est `etape-4-…`. |
| 6 | 063 | 364 + 160 à 152 | **`05_Sentier/Science`** (type SENTIER) | Le #1 (364, « Qu'est-ce que la méthode scientifique ? ») est **manquant**. Seul existe le doublon ancien 161, qui est publié. |
| 7 | 064 | 151 à 141 (sans 144) | `02_Fonds` | Le slug du hub est `etape-5-…`. |
| 8 | 065 | 140 à 131 (sans 139) + #10 | `02_Fonds` | Le #10, « Érudition et sagesse », est **absent du dépôt**. Le slug du hub est `etape-7-…`. |
| 9 | 066 | 129 à 120 | **`05_Sentier/Equilibre`** (type SENTIER) | Le slug du hub est `etape-8-…`. |

**Bilan**
- Fondamentaux : 60 sont dans `02_Fonds` et 30 dans `05_Sentier` (étapes 2, 6 et 9). Il en manque 3 : l'URL du hub de l'étape 1, le 364 et le #10 de l'étape 8.
- `02_Fonds` contient 259 FOND, dont **60 seulement figurent au manifeste**. Les quelque 199 autres sont des imports WordPress anciens, sans rôle pédagogique : catégories `le-phare-info` (25), science-santé (15), géopolitique (13), `non-classe` (11), etc.

**Étape bonus « art de la mémoire »**
- Elle est citée dans les Instructions (l. 35) et dans `Arborescence_Sentier_par_etapes.md` : dossier `05_Sentier/Bonus_Art_de_la_memoire`, marqué « réserve, aucun article détecté ».
- **Aucun contenu n'existe.**

**Deux autres versions concurrentes figurent dans le stock**
- **2026-007, « Le Sentier du Savoir »** : il compte **8 étapes**, plus un bonus « devenir passeur de savoir », dans un autre ordre (culture, critique, approfondir, polyglotte, écrire, méthode scientifique, échanger, corps-esprit).
- **2026-217, « Étape Bonus 1 – Devenir Curateur & Éclaireur »** : son slug est `etape-9-bonus-…` et il se trouve dans `02_Fonds`.
- **2026-113, « Le rôle des Étapes du Sentier »** : un texte de présentation à mettre en cohérence.

Les slugs décalés viennent de cette ancienne numérotation en 8 étapes, avant l'ajout de l'étape « argumenter ». Le lecteur peut donc trouver en ligne trois présentations incompatibles du Sentier.

## 2. Fondamental et atelier : ce qui est réellement défini

**Définitions en vigueur** (`Sentier_fondamentaux_referentiel.md`)
- **Fondamental** : pilier intemporel d'environ 1200 mots, pris dans une liste fixe (le manifeste CSV).
- **Sous-fondamental** : il n'est créé que pour combler une lacune validée.
- **Atelier** : application d'un fondamental à l'actualité. Il porte deux métadonnées, « Fondamental lié (ID) » et « Type Sentier : atelier ». Il est listé dans la rubrique `## Ateliers` à la fin de son fondamental parent.
- **Règle d'or** : pas de 11e fondamental.

**Production des ateliers**
- Hier, un atelier par triptyque : 22 ateliers, du 468 au 530, du 19 mai au 25 juin 2026. S'y ajoutent des ateliers plus anciens, du 450 au 465.
- Aujourd'hui, la routine mensuelle les produit : un seul jusqu'ici, le 560 du 6 octobre.
- Les parents sont concentrés sur quelques fondamentaux (198, 196, 194, 182…).

**Écarts avec la proposition de ChatGPT**
1. **La dépendance au parent est plus stricte chez nous.** Chaque atelier a *un* parent obligatoire. ChatGPT admet qu'un atelier « mobilise plusieurs fondamentaux ». Les deux sont compatibles si l'on garde un parent principal (pour la rubrique `## Ateliers`) et qu'on ajoute des liens secondaires.
2. **Les structures en 9 points (fondamental) et en 8 points (atelier) n'existent dans aucun gabarit.**
3. **La frontière est floue dans l'index.** Les fondamentaux des étapes 2, 6 et 9 ont le type SENTIER, comme les ateliers. Seules les métadonnées internes les distinguent.
4. **Le validateur rejette les fondamentaux d'étape rénovés (159, 198).** Il attend d'un SENTIER qu'il soit un atelier (catégorie `sentier-du-savoir`, tag de thème).
5. **Le référentiel cite des parents erronés.** 2026-399, 397 et 382 sont des copies du wiki, pas les canoniques 198, 196 et 180.

## 3. Protection de `02_Fonds/`

**Règle écrite**
- `plan.md` D8 : jamais de push WordPress par une routine ; seule la rubrique `## Ateliers` peut être mise à jour en local ; le refresh WordPress revient à l'éditeur humain.
- Le `CLAUDE.md` (section Interdits) et le référentiel disent la même chose. Le référentiel justifie la règle par une « décision éditeur ».
- La plus ancienne trace dans git est le commit `9fab725` du 6 octobre 2026. Aucune motivation n'est documentée au-delà de cette décision.

**Garde-fous techniques**

| Outil | Comportement |
|---|---|
| `wp_refresh_body.py` | Refuse les chemins `02_Fonds/`, sauf avec `--allow-fonds` (introduit au commit `6d5e5ce`, v3.10) |
| `wp_pull_body.py` | Refuse `02_Fonds/` |
| `verify_publication.py` | Exclut `02_Fonds` |
| `build_inventaire_renovation.py` | Classe `02_Fonds` hors périmètre |
| **`wp_push_draft.py`, `daily_run.py`** | **Aucun garde-fou** : la création d'un article dans `02_Fonds` n'est empêchée que par la consigne |

**Ce qui est protégé, et ce qui ne l'est pas**
- Sont bloquées la publication et la modification sur WordPress. La rédaction locale reste permise : rubrique `## Ateliers`, propositions dans `Propositions_fonds/`.
- La protection est **fondée sur le chemin, pas sur le rôle**. Elle couvre donc les 60 fondamentaux d'étape *et* les 199 FOND anciens sans rôle pédagogique.
- En revanche, elle **ne couvre pas les 30 fondamentaux des étapes 2, 6 et 9**, rangés dans `05_Sentier`. Deux d'entre eux (159 et 198) ont d'ailleurs été réécrits et poussés par la routine de rénovation.

## 4. Couverture des besoins de compréhension

| Domaine | État | Contenus |
|---|---|---|
| Pensée critique | Bien couvert | Étape 2 entière |
| Méthode scientifique, statistiques | Bien couvert | 159, 157, 153, atelier 560 |
| Économie | Partiel | 207 « Économie pour non-économistes », 213 « Lire un indicateur économique » (FOND hors manifeste), dossier Inflation non publié |
| Systèmes | Partiel | 136 « La pensée systémique », 178, textes fondateurs Perrow et Smil |
| Récits médiatiques | Partiel | 186 (storytelling), 137, 194 (décryptage), 248, série slow journalism hors Sentier |
| **Institutions, droit, pouvoir** | **Lacune** | Aucun fondamental. Seulement des textes fondateurs (Arendt 109/476, Habermas 503, Scott 509, Strange 479, Hirschman 488) et le 163 « Langues et pouvoir » |

Cette lacune pèse d'autant plus que les fils actifs (« Qui contrôle le contrôleur ? », « Mesurer ou juger ») y renvoient sans cesse.

## 5. Contenus périphériques

Ce recensement va au-delà de la seule étape 9.

- **Accords toltèques** : SENTIER 090 à 095, et le FOND 096 qui s'y rattache (médiation sociale, « Ne faites pas de suppositions »).
- **Étape 9** (120 à 129) :
  - nutrition, sommeil (128), mouvement ;
  - méditation (126), émotions (125) ;
  - hygiène numérique (124), rituels (123), rythme (122) ;
  - philosophies du bien-vivre (121) ;
  - programme personnel (120).
- **Hygiène de vie** : 008, 015 et 050 (doublons entre eux), 079, et 026 « Hygiène de vie et débat démocratique ».
- **Stress** : 031, 036.
- **Sommeil** : 077, « Une heure de sommeil en moins, 20 % de discernement ».
- **Nussbaum** : 029 (texte fondateur) et 078 (SENTIER, doublon).
- **Atelier 510** : étape 9, sur l'attention.
- **Textes déjà critiques du discours bien-être** : 022, 054.

**Pistes de classement** (indicatives, pour la décision du fondateur)

| Proposition | Articles | Raison |
|---|---|---|
| Conserver et relier | 124, 510, 022, 054 | L'attention et l'hygiène numérique relèvent de l'autonomie intellectuelle ; 022 et 054 sont déjà critiques |
| Réorienter | 128, 126, 077 | Passer du conseil aux données de recherche et à leurs limites |
| Relier | 029, 121 | Philosophie du bien-vivre, avec une posture « Comprendre » |
| Fusionner ou archiver | 015, 050, 008, 079 ; 078 (face à 029) | Doublons |
| Un seul article critique, ou archivage | 090 à 095 (Toltèques) | Développement personnel sans base vérifiable |
| Réorienter ou archiver | 120, 123 | Développement personnel pur |

Toute dépublication relève d'une décision humaine. Aucune n'est proposée à cette étape.

## 6. Désaccords et réserves

1. **Structures en 9 et 8 points.** Imposées telles quelles, elles deviennent un canevas rigide, contraire au §3 des Instructions (« pas un canevas visuel figé »). Je propose une liste de *fonctions* obligatoires (définir, illustrer, limites, sources, exercice, liens), sans ordre imposé ni intertitres fixes.
2. **Un atelier lié à plusieurs fondamentaux.** J'y suis favorable, avec un parent principal, sans quoi la rubrique `## Ateliers` devient ingérable.
3. **Versionnement des dépendances par fondamental.** C'est lourd à maintenir. Git suffit à l'historique : il suffit de noter la date de révision dans l'en-tête et de signaler les ateliers liés quand le parent change.
4. **Protection par le rôle, non par le chemin.** C'est la recommandation la plus importante de cette étape :
   - protéger les 90 fondamentaux du manifeste, où qu'ils soient rangés ;
   - ajouter le garde-fou manquant dans `wp_push_draft.py` ;
   - décider à part du sort des 199 FOND anciens (rénovables ou non).
5. **Sources exigées dans les fondamentaux.** C'est juste. Mais pour les 60 textes de `02_Fonds`, cela veut dire 60 propositions à valider par l'éditeur. Il faut prévoir un rythme, par exemple une étape par mois.
6. **Recentrage du Sentier.** Il ne se décide pas article par article. Il faut d'abord trancher la question de l'étape 9 (voir les questions ci-dessous).

## Questions pour le fondateur (pas pour ChatGPT)

- **Étapes** : 9, ou 8 plus un bonus ? L'étape bonus (art de la mémoire, ou passeur, curateur et éclaireur) est-elle maintenue, et sous quel nom ?
- **Étape 9** : faut-elle la garder, la recentrer sur l'attention et les conditions du jugement, ou la retirer ?
- **Institutions et droit** : faut-il ouvrir une étape ou des fondamentaux, ce qui suppose de lever la règle « pas de 11e fondamental » ?
- **Protection** : faut-il passer à une protection par le rôle (les 90 fondamentaux du manifeste), et décider du sort des 199 FOND anciens ?
- **Présentations concurrentes** (007, 113, 217) : faut-il les réécrire, les fusionner ou les archiver ?
