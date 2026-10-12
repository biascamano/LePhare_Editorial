# Réponse de Claude au cadrage consolidé (message 7)

**Date : 12 octobre 2026**

**Objet** : le document `Le_Phare_Info_Cadrage_Editorial_Consolide_2026-10-12.docx`, archivé sous `07_Message_7_cadrage_consolide_ChatGPT_2026-10-12.md`.

**Ce qui n'a pas été fait** : rien n'est modifié ni publié, comme le demande le §10 du cadrage. Ce document propose une **première modification minimale et testable**.

**Marquage** : [V] vérifié dans le dépôt · [D] déduit · [P] proposé · [A] à arbitrer.

---

## 1. Ce que je prends comme décidé

Les cinq « SOUHAITS EXPRIMÉS » du §11 sont des décisions du fondateur. Je ne les rediscute pas :
- trois articles par jour ;
- rattrapage quotidien ;
- autonomie après un contrôle complet ;
- rétrospectives contradictoires ;
- place des curiosités du fondateur.

Ma recommandation antérieure (tension 1, option c : 5 à 7 articles par semaine) est **remplacée**. Une seule garantie demeure, et le cadrage la prévoit déjà : la rétrospective peut corriger la cadence au vu des faits.

**Convergences nouvelles avec mes réponses 1 à 6**

| Point du cadrage | Ce qu'il remplace ou confirme |
|---|---|
| Porte de contrôle PUBLIER / CORRIGER / BROUILLON (§3.5) | Remplace ma liste fixe de sujets sensibles (R6 É2) par un examen au cas par cas. C'est **meilleur** : le risque est jugé sur le texte, pas sur la rubrique |
| Actualité générale « non enfermée dans le Radar » (§2.1) | Répond au biais de continuité (R6 tension 2) |
| Rétro distincte du Fil (§4.3) | Le Fil reste un produit public ; la rétro comble l'absence de trace d'arbitrage (R6 É12) |
| Suivi des décisions dans la rétro mensuelle (§5.2) | Complète `plan.md` §3 sans créer de nouveau fichier |
| Pas de graphe, lien justifié par une phrase (§7) | Identique à R6 tension 4 |
| Atelier avec un parent principal ; atelier ≠ Question ≠ Application (§7) | Identique à R6 §4.5 A |

---

## 2. Points à corriger ou préciser dans le cadrage

### 2.1 Le Radar va déborder mécaniquement [D]

Le calcul est simple :
- chaque Actualité ajoute aujourd'hui sa question au bloc 2 du Radar (skill quotidienne, étape 10) ;
- avec 2 Actualités et 1 Question par jour, le bloc 2 reçoit **+2 entrées et en perd 1** ;
- soit +1 entrée nette par jour, environ +30 par mois.

Or le Radar compte déjà 34 entrées pour un plafond de 30 [V].

**[P]** Une question d'Actualité n'entre au Radar que si la routine lui attribue P1 ou P2. Sinon, elle reste dans l'article et dans la mémoire §1, où elle est retrouvable par l'hebdomadaire. L'article de curiosité n'alimente le Radar que par exception.

### 2.2 Le contrôle « final » ne l'est pas tout à fait [V]

Deux étapes modifient le texte **après** la décision de publier :
- `daily_run` (maillage par `post_linking`) ;
- le « relier en retour » sur l'article d'origine.

Ces modifications sont **déterministes** : elles ajoutent des liens de navigation lus dans l'index, et `verify_publication.py` les contrôle déjà.

**[P]** La porte de contrôle porte sur le texte rédactionnel juste avant `daily_run`. Les ajouts automatiques qui suivent restent couverts par `verify_publication`. La formule du §3.5 devient : « après les dernières modifications **rédactionnelles** ».

### 2.3 Un contrôle fait par le rédacteur n'est pas indépendant [D]

Si c'est la même session qui a écrit l'article qui le contrôle, elle partage ses angles morts. C'est vrai en particulier pour une source mal comprise, un chiffre mal relu ou un cadrage biaisé.

Deux niveaux sont possibles :

| Niveau | Fonctionnement | Coût |
|---|---|---|
| a. Auto-contrôle par liste | Pour chaque article, la grille §3.1–3.4 est remplie point par point dans la fiche, avec une preuve pour chaque point (« vérifié dans [source] ») | Faible |
| b. Relecture à contexte vierge | Un agent séparé reçoit seulement le texte final, les sources et la grille ; il ne connaît pas le raisonnement du rédacteur | Environ une demi-session par article |

**[P]** Le niveau **a** pour tous les articles. Le niveau **b** seulement si (a) a coché un point §3.1 (personnes, accusations, groupes) ou si un chiffre central repose sur une seule source.

**[A]** Le fondateur peut préférer **b** pour tous les articles pendant la journée pilote, afin de comparer les deux niveaux.

### 2.4 Vérification des liens externes : une limite pratique [D]

Certains sites refusent l'accès automatique : paywall, erreur 403, contenu chargé en JavaScript.

**[P]** Ces sources ne sont pas exclues d'office :
- une source essentielle inaccessible doit être **confirmée par une deuxième source accessible** ;
- à défaut, le fait est reformulé avec prudence (« selon [source], non consultée intégralement ») ;
- ou bien il passe en BROUILLON s'il porte l'article.

### 2.5 Images et droits [V partiel]

Les routines n'insèrent aucune image dans le corps de l'article. L'image à la une vient d'une correspondance tag → média, gérée localement par le fondateur et utilisée par `wp_push_draft.py` et `daily_run.py`.

**[D]** Le contrôle des licences porte donc sur cette médiathèque une fois pour toutes, et non sur chaque article. Le point §3.3 peut être réduit à : « aucune image ajoutée au corps sans licence vérifiée ».

### 2.6 « Actualité de curiosité » : un critère de choix, pas un nouveau type [P]

Pour le lecteur, c'est une Actualité ; ce qui change, c'est la raison du choix.

Je propose de ne rien changer dans la taxonomie WordPress, ni dans les catégories, ni dans les codes de l'index. Il suffit d'un champ **« Regard : général / curiosité »** :
- dans l'en-tête de l'article ;
- dans la ligne de la mémoire §1.

La rétro hebdomadaire mesure l'équilibre entre les deux regards à partir de ce champ.

### 2.7 Charge [D]

Le volume passe à 3 articles, 3 contrôles et 1 rattrapage par jour, soit environ 90 articles par mois avant rénovation. Une session de rédaction complète consomme aujourd'hui une bonne part du contexte disponible, avec la veille, la fiche, la rédaction et la publication.

**[P]** Prévoir **une conversation par exécution** (`/clear` entre deux), soit quatre exécutions par jour.

Elles restent cohérentes entre elles sans mémoire de conversation : `build_etat_courant.py` est relancé à la fin de chaque exécution, et l'exécution suivante voit donc les articles du jour.

**Mesure** : je n'ai pas accès à ma consommation de tokens. Pendant la journée pilote, le fondateur note pour chaque exécution la durée et l'indicateur de coût ou de contexte de Claude Code.

---

## 3. Cartographie des modifications

Chaque ligne indique le fichier touché et l'ampleur de la modification. Rien n'est implémenté.

| # | Fichier | Modification | Ampleur |
|---|---|---|---|
| 1 | `.claude/skills/routine-quotidienne/SKILL.md` | Trois variantes : `— generale`, `— curiosite`, `— question` (la dernière existe déjà sous `type question`). Pour `generale`, la veille est **toujours** complète, et les échéances du Radar ne sont que des candidats parmi d'autres. Pour `curiosite`, les candidats viennent du bloc Curiosités du Radar et d'une veille ciblée. La règle anti-doublon est l'étape 1 existante : on relit l'état courant, qui contient les articles du jour | Moyenne |
| 2 | Même skill, nouvelle étape entre `stage` et `daily_run` | **Contrôle prépublication**, avec trois issues : PUBLIER → `daily_run` normal ; CORRIGER → correction, puis nouvel examen (2 cycles au plus, sinon BROUILLON) ; BROUILLON → `daily_run --no-publish-final` et signalement dans le rapport. Le fondateur publie ensuite avec `verify_publication.py --publish-drafts <ID>`, qui existe déjà [V] | Moyenne |
| 3 | `00_Systeme/Controle_prepublication.md` (**nouveau**, environ 40 lignes) | La grille §3.1–3.4, lue **uniquement** au moment du contrôle. Un fichier à part évite d'alourdir le skill et sert à la quotidienne comme à la rénovation. C'est le seul fichier nouveau ; il répond à une fonction absente aujourd'hui | Petite |
| 4 | `tools/memoire_append.py` | Deux options : `--regard general\|curiosite` et `--controle "PUBLIER" \| "CORRIGER×n : motif" \| "BROUILLON : motif"`. Elles ajoutent deux colonnes à la mémoire §1, qui devient la **trace d'arbitrage et de contrôle** (R6 É12) sans nouveau journal. Un BROUILLON y figure aussi | Petite |
| 5 | `00_Systeme/Radar_editorial.md` | Nouveau bloc 6 **Curiosités** (question personnelle, ancrage possible, champs, priorité, statut), plafonné à 8 entrées hors plafond général. Règle du §2.1 ci-dessus pour les questions d'Actualité. Semence : la liste d'intérêts du §2.2 du cadrage | Petite |
| 6 | `tools/build_etat_courant.py` | Compteur du Radar par bloc, plafond signalé ; nombre d'articles du jour par regard | Petite |
| 7 | `.claude/skills/routine-renovation/SKILL.md` | Variante `— rattrapage` : **une** action par jour, dans cet ordre de priorité : signalements, articles cités par une publication récente, lot ouvert. Nouvelle action **Contextualiser** (note datée « Depuis », sourcée). La porte de contrôle s'applique à toute réécriture | Moyenne |
| 8 | `.claude/skills/routine-hebdomadaire/SKILL.md` | Nouvelle section **Rétro interne**, après la vérification du Fil : les 8 questions du §4.1, à partir de la mémoire §1 (colonnes regard et contrôle), du Radar et des signalements. Les doutes de Claude sont exposés. Trois actions au plus, chacune avec un critère observable | Moyenne |
| 9 | Sortie de la rétro hebdomadaire | Fichier **non publié** `06_Syntheses/Retros/YYYY-Snn.md`, au format court de transmission à ChatGPT (R6 §4.4). Seules les 3 actions vont en mémoire, et les arbitrages vont dans `plan.md` §3 | Petite |
| 10 | `.claude/skills/routine-mensuelle/SKILL.md` | Le rapport mensuel existant (`06_Syntheses/Rapports_mensuels/`) reçoit trois rubriques : **Suivi des décisions** (actions des rétros et D18+ : appliqué, utile, abandonné, à revoir), **Apprentissages**, **Cap** (3 à 5 priorités). Pas de second rapport | Petite |
| 11 | `plan.md` §3 | D18 et suivantes avec les colonnes Justification et Statut (R6 §4.3), ainsi que les décisions du présent cadrage | Petite |
| 12 | `CLAUDE.md` | Tableau des déclencheurs : les trois variantes quotidiennes et `routine renovation — rattrapage` | Petite |

**Inchangés** :
- l'index et ses colonnes ;
- la taxonomie WordPress ;
- le Sentier ;
- `02_Fonds/` ;
- `daily_run.py` : `--force` reste nécessaire à partir du 2ᵉ article du jour, ce que le skill prévoit déjà [V].

---

## 4. Modification minimale proposée : le lot 1, puis une journée pilote

### Lot 1, implémenté en une fois

Il comprend les lignes **1 à 6 et 12** : les trois variantes, la porte de contrôle, la grille, les deux colonnes de la mémoire, le bloc Curiosités et la règle d'entrée au Radar, le compteur.

Les rétros (lignes 8 à 10) et le rattrapage (ligne 7) viennent ensuite. Ce sont des routines déjà existantes, que l'on teste à leur prochaine échéance.

### Journée pilote

On enchaîne quatre exécutions, chacune dans une conversation séparée :

| Ordre | Déclencheur | À observer |
|---|---|---|
| 1 | `routine quotidienne — generale` | Veille complète ; issue du contrôle et motif |
| 2 | `routine quotidienne — curiosite` | Ancrage vérifiable ; pas de recoupement avec 1 |
| 3 | `routine quotidienne — question` | Question distincte des deux premiers articles ; pas de doublon avec le Radar ni avec l'index |
| 4 | `routine renovation — rattrapage` | Une action réelle, contrôlée |

### Critères de réussite, observables le soir même

1. Trois articles distincts, chacun avec une ligne de contrôle dans la mémoire §1.
2. Au moins un point CORRIGER ou une réserve réellement écrite. Un contrôle qui ne trouve jamais rien est suspect.
3. `verify_publication.py` sans erreur.
4. Taille du Radar ≤ plafond.
5. Durée et coût notés pour chaque exécution.

**Retour arrière** : un `git revert` du commit du lot 1. Aucun changement sur WordPress n'est lié au lot lui-même.

---

## 5. Arbitrages nécessaires avant le lot 1

| # | Question | Ma recommandation |
|---|---|---|
| 1 | Niveau de contrôle pendant le pilote : auto-contrôle (a) ou relecture à contexte vierge pour tous les articles (b) ? | **b** pendant le pilote, pour comparer ; puis **a + b ciblé** (§2.3) |
| 2 | Liste de curiosités initiale : celle du §2.2 du cadrage telle quelle ? | Oui, en ajoutant pour chaque entrée la « question personnelle », que seul le fondateur peut formuler. À défaut, je propose une question par domaine, à corriger |
| 3 | Une question d'Actualité entre au Radar seulement si P1/P2 (§2.1) ? | Oui |
| 4 | Fichier de rétro hebdomadaire dans `06_Syntheses/Retros/` (non publié) ? | Oui |
| 5 | En cas de BROUILLON, l'exécution du jour est-elle terminée, ou l'exécution choisit-elle un autre sujet ? | Terminée : un deuxième sujet dans la même session double le coût et pousse à publier coûte que coûte |

**Toujours ouverts**, et non bloquants pour le lot 1 : mention publique « Mis à jour le … », transparence sur l'IA, étape 9, protection par le rôle, export WordPress, pilote Inflation (R6 Partie 6).
