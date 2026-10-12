# Rapport d'alignement initial de Claude (réponse au message 6/6)

**Date : 12 octobre 2026**

**Méthode** : synthèse des réponses 1 à 5 (notées R1 à R5) et des lectures du dépôt. Rien n'a été modifié : ni routine, ni configuration, ni WordPress, ni commit.

**Marquage** : **[V]** vérifié · **[D]** déduit · **[P]** proposé · **[A]** à arbitrer. Les statuts du message 6 sont écrits en capitales : DÉCIDÉ, RECOMMANDÉ, À VÉRIFIER, À ARBITRER.

Ce document est aussi le **fichier consolidé** destiné à ChatGPT. Les détails et les preuves chiffrées restent dans R1 à R5 ; ils sont cités, pas recopiés.

---

## Préalable : ce qui passe de « À VÉRIFIER » à « vérifié »

Le message 6 classe sept points en À VÉRIFIER. Cinq ont été vérifiés dans le dépôt, deux ne peuvent pas l'être.

| Point | Résultat | Où |
|---|---|---|
| Implémentation de la V5 | **[V] Implémentée** (commit `16c3283`, 2026-10-06), skills et `new_article.py` | R3 §1, R5 §0 |
| Taxonomies | **[V] depuis l'index seulement**, pas d'export WP | R3 §4 |
| Statut du wiki | **[V] dans l'index** : 48 lignes en double sur 51. **Non vérifié en ligne** | R3 §2 |
| Fonctionnement de `02_Fonds` | **[V]** Protection par le chemin, avec une faille dans `wp_push_draft.py` | R2 §3 |
| Dossier Inflation | **[V]** 10 brouillons WP depuis le 8 avril, format d'avant la V5 | R3 §3 |
| Publication et validation | **[V]** Publication directe, contrôles de forme seulement | R5 §1 |
| Coûts des routines | **Non mesurable** : aucune donnée de tokens ; tailles en lignes seulement | R5 §5 |

---

## Partie 1 — Points de convergence

Sur chacun de ces points, la philosophie et le système sont déjà cohérents **[V]** :

1. **Actualité comme ancrage, question comme moteur.** Le choix du jour part de la veille et du Radar. Une Actualité fait émerger une seule Question du Phare, qui entre au Radar (skill quotidienne, étapes 7 et 10).
2. **Architecture non rigide.** Un article par déclenchement, dont le type est choisi après le sujet. Le triptyque est archivé et aucun quota n'existe (D12, R4 §1).
3. **Penseurs sans argument d'autorité.** Aucun penseur dans une Actualité ; le gabarit Question demande de « tester » une intuition, puis contient une section « Ce qui résiste » (R1 §2).
4. **Séparation des trois routines.** Elle est réelle, et chaque routine a ses lectures (R3 §5, R5 §1–3).
5. **Mémoire et sobriété.** L'état courant est généré, le Radar est partagé et la quotidienne se limite à trois lectures (R5 §4).
6. **Connexions justifiées au moment où elles apparaissent.** Elles passent par le Fil du Phare et le comité hebdomadaire. Les dossiers suivent la règle « un mot qui revient ne suffit pas » (R5 §2–3).
7. **« 0 est une réponse valide »** pour les dossiers, les TF et les ateliers. Le Fil n'est pas publié en dessous de 3 articles (R5 §2–3).
8. **Liens internes vérifiables.** Les URL sont lues dans l'index et contrôlées par `verify_publication.py` (R1 §2).
9. **Protection des fondamentaux.** Seul l'éditeur humain les modifie ; une routine ne peut que proposer une réécriture dans `Propositions_fonds/` (R2 §3).
10. **Patrimoine.** La rénovation garde le même ID et la même URL, et les faits anciens restent datés (D17, R4 §2).
11. **Rédaction sans API payante et déclenchement manuel** (D4, R5 §5).
12. **Traçabilité** : git, `plan.md` §3 (décisions) et §13 (évolutions), archives du Radar avec leur raison (R5 §0).

---

## Partie 2 — Écarts identifiés

### 2.A Écarts entre l'intention et le système

Les écarts sont classés par impact, du plus fort au plus faible. Les preuves détaillées figurent dans la réponse indiquée.

**É1 — Pas de droit de ne rien publier**
- **Domaine** : E. Routines, et tension 1.
- **Intention** : slow journalism, « ni une machine à produire quotidiennement ».
- **État réel [V]** : la quotidienne aboutit toujours à un article. Un mécanisme de report existe pour l'hebdomadaire et la mensuelle, pas pour la quotidienne.
- **Écart** : le critère final (« meilleur prochain article ») est **relatif**. Il désigne toujours un gagnant, jamais « aucun ».
- **Preuve** : skill quotidienne, étapes 4 et 9 ; R5 §1.
- **Impact** : fort.
- **Recommandation [P]** : ajouter un seuil absolu (par exemple, aucun candidat « Fort » sur l'importance **ou** sur la compréhension), une sortie « report motivé » et une ligne dans la mémoire §1.
- **Statut** : À ARBITRER.

**É2 — Publication sans relecture humaine, y compris sur les sujets sensibles**
- **Domaine** : G, F, et tension 3.
- **Intention** : « décisions sensibles traçables et contrôlées ».
- **État réel [V]** : l'article part en statut publié dès la fin de la routine. Aucune liste de sujets sensibles n'existe.
- **Preuve** : `daily_run.py` (publication finale par défaut) ; R1 §3.2.
- **Impact** : fort.
- **Recommandation [P]** : brouillon obligatoire pour une courte liste de sujets sensibles, le reste publié directement (§4.1, tension 3).
- **Statut** : À ARBITRER.

**É3 — Vérification factuelle non outillée et non tracée**
- **Domaine** : F.
- **Intention** : principe 2 (« rattachée à une source vérifiable »).
- **État réel [V]** : seule la présence d'un lien est contrôlée. Il n'existe ni hiérarchie des sources, ni règle de citation, ni liste de sources de veille, ni trace de la veille.
- **Preuve** : `verify_publication.py`, R5 §1, R1 §3.3.
- **Impact** : fort.
- **Recommandation [P]** : inscrire 3 règles dans les Instructions :
  - hiérarchie primaire > institutionnelle > presse de référence ;
  - guillemets seulement si le texte exact a été lu ;
  - fait d'actualité daté.

  Aucun outil n'est à créer : une vérification automatique des faits produirait surtout des faux positifs.
- **Statut** : RECOMMANDÉ.

**É4 — Le Sentier contredit en partie la mission**
- **Domaine** : C.
- **Intention** : « ni un programme de développement personnel », autonomie intellectuelle.
- **État réel [V]** :
  - l'étape 9 et les séries Toltèques et hygiène de vie relèvent du développement personnel ;
  - trois présentations concurrentes du Sentier sont en ligne (007, 113, 217) ;
  - plusieurs slugs de hubs sont décalés.
- **Preuve** : R2 §1, §5.
- **Impact** : fort pour la crédibilité.
- **Recommandation [P]** : trancher l'étape 9 avant tout travail article par article.
- **Statut** : À ARBITRER.

**É5 — Protection par le chemin, et non par le rôle**
- **Domaine** : C.
- **Intention** : protéger les fondamentaux.
- **État réel [V]** :
  - 30 fondamentaux (étapes 2, 6 et 9, rangés dans `05_Sentier`) ne sont pas protégés, et 2 ont été poussés par la rénovation ;
  - 199 FOND anciens sans rôle pédagogique sont protégés ;
  - `wp_push_draft.py` n'a aucun garde-fou.
- **Preuve** : R2 §3.
- **Impact** : moyen.
- **Recommandation [P]** : protéger les 90 fondamentaux du manifeste, où qu'ils soient rangés, et ajouter le garde-fou dans `wp_push_draft.py`.
- **Statut** : À ARBITRER, car la règle de protection relève du fondateur.

**É6 — Lacune « institutions, droit, pouvoir »**
- **Domaine** : C.
- **État réel [V]** : aucun fondamental sur ce sujet, alors que deux fils actifs y renvoient sans cesse.
- **Écart** : la règle « pas de 11ᵉ fondamental » empêche de la combler.
- **Preuve** : R2 §4.
- **Impact** : moyen.
- **Statut** : À ARBITRER.

**É7 — La catégorie WordPress mélange cinq logiques**
- **Domaine** : D.
- **État réel [V, depuis l'index]** :
  - la catégorie WP mélange domaine, format, étape, posture et résidus ;
  - le domaine d'une Actualité n'apparaît pas dans sa catégorie ;
  - le dossier n'existe pas dans la taxonomie ;
  - on compte 323 tags.
- **Preuve** : R3 §4.
- **Impact** : moyen pour le lecteur, faible pour les routines.
- **Recommandation [P]** : catégorie = domaine, tag `type-*` obligatoire, pas de taxonomie de concepts (R3 §6). **Rien avant un export WP.**
- **Statut** : À VÉRIFIER, puis À ARBITRER.

**É8 — L'index ne porte pas les relations qui existent déjà**
- **Domaine** : D.
- **État réel [V]** : pas de colonne `Dossier`, `Origine` ni `Fondamental`. `Articles_lies` n'est pas typée et le wiki compte 48 lignes en double.
- **Preuve** : R3 §2, §4.
- **Impact** : moyen.
- **Recommandation [P]** : 3 colonnes, remplies par `new_article.py`, et un marquage `doublon_wiki`.
- **Statut** : RECOMMANDÉ.

**É9 — Contenus en attente depuis six mois**
- **Domaine** : B, F.
- **État réel [V]** : 11 brouillons DOSSIER, dont les 10 d'Inflation (au format d'avant la V5, sans accents, sans chiffres datés). Aucune raison de non-publication n'est documentée.
- **Preuve** : R3 §3, R4 §0.
- **Impact** : moyen. Il n'y a aucun risque public, mais c'est un patrimoine qui dort.
- **Recommandation [P]** : un pilote de consolidation (10 contenus → 5 ou 6), en lecture seule d'abord.
- **Statut** : À ARBITRER (feu vert).

**É10 — La maintenance grossit plus vite qu'elle n'est traitée, et aucune correction n'est rendue publique**
- **Domaine** : F, et tension 5.
- **État réel [V]** :
  - le lot 3 est passé de 53 à 87 articles en 6 jours ;
  - l'action « contextualiser » n'existe pas ;
  - aucune mention publique de correction ou de mise à jour.
- **Preuve** : R4 §5, §6.
- **Impact** : moyen.
- **Recommandation [P]** : maintenance déclenchée par l'usage ; règle « cité → Remettre à niveau » ; note datée « Depuis » ; ligne « Mis à jour le … ».
- **Statut** : RECOMMANDÉ, avec deux points À ARBITRER (la mention publique et la règle « cité »).

**É11 — Les résumés vieillissent et se contredisent**
- **Domaine** : E.
- **État réel [V]** : l'audition de Philadelphie est datée du 7 octobre dans le cap, mais du 26 octobre dans le Radar. Les échéances sont recopiées à trois endroits.
- **Preuve** : R5 §3, §4.
- **Impact** : moyen, car cela peut fausser le choix du jour.
- **Recommandation [P]** : le Radar devient la seule source des dates, et chaque résumé porte sa date.
- **Statut** : RECOMMANDÉ.

**É12 — Le choix du sujet n'est pas tracé et le Radar dépasse son plafond**
- **Domaine** : E, F.
- **État réel [V]** :
  - les candidats écartés et la raison du choix disparaissent avec la session ;
  - le Radar compte 34 entrées actives pour un plafond de 30 ;
  - une entrée `P?` n'a pas de priorité.
- **Preuve** : R5 §1, §2, §4.
- **Impact** : moyen. Sans cette trace, la tension 2 ne peut pas être contrôlée.
- **Recommandation [P]** : une ligne « Arbitrage » dans la mémoire §1 ; un compteur du Radar dans `build_etat_courant.py`.
- **Statut** : RECOMMANDÉ.

**É13 — Liste de penseurs orientée**
- **Domaine** : A.
- **Intention** : « impartialité méthodologique ».
- **État réel [V]** : le réservoir par défaut est dominé par la critique européenne de la technique (Weil, Ellul, Illich, Rosa).
- **Preuve** : R1 §1.4, `plan.md` §5.8.
- **Impact** : moyen, et cumulatif.
- **Recommandation [P]** : élargir la liste à d'autres traditions (épistémologie, institutions, économie).
- **Statut** : RECOMMANDÉ, à discuter avec ChatGPT.

**É14 — Trop de textes de référence**
- **Domaine** : G.
- **État réel [V]** :
  - le socle (.docx), les Instructions (254 lignes), `plan.md` (760 lignes) et `CLAUDE.md` se recouvrent ;
  - `00_Systeme/` compte 37 entrées, dont au moins 8 obsolètes ;
  - le socle s'interrompt à la section Weil (T12 ouvert).
- **Preuve** : R1 §3.9, R5 §4.
- **Impact** : moyen, car c'est un risque de divergence entre Claude et ChatGPT.
- **Recommandation [P]** : voir §4.3.
- **Statut** : RECOMMANDÉ.

**É15 — Transparence sur l'IA**
- **Domaine** : A, G.
- **État réel [V]** : le socle n'en dit rien et aucune mention n'apparaît sur le site, d'après le dépôt.
- **Impact** : à évaluer par le fondateur.
- **Statut** : À ARBITRER.

**Écarts mineurs [V]**
- Le dossier 559 est en catégorie `dossier-hebdomadaire` alors qu'il a été produit par la mensuelle.
- Le profil `triptyque_minimal` est le profil par défaut de la V5 (R3 §1).
- Le validateur rejette les fondamentaux rénovés (R2 §2).
- L'index ne compte que 4 tags `a-la-une`, alors que WordPress fait foi (R3 §4).
- Le fil « Le prix de l'invisible » regroupe 12 articles et n'a aucun critère de scission (R5 §2).

### 2.B Propositions de ChatGPT qui reposent sur un point contesté

Ces propositions **ne doivent pas être reprises telles quelles** dans le référentiel. Leur prémisse a été corrigée ou contestée par la vérification.

| Proposition (message) | Point contesté | Position de Claude |
|---|---|---|
| Neuf relations typées entre articles (4) | Une seule existe (`Article precedent`), et elle n'est pas affichée en tant que telle | Une phrase et un lien dans le texte. Au plus 3 colonnes structurelles (É8). R4 §8 |
| 16 métadonnées par article, durée de validité par type (4) | La moitié existe déjà ; le reste ne serait pas maintenu | Non. R4 §6 |
| Six statuts de maintenance comme champ nouveau (4) | Ils recoupent les lots existants | Les faire correspondre aux lots ; seule « contextualiser » est à créer. R4 §5 |
| 61 articles isolés (4) | Chiffre surestimé | R4 §3 |
| Gabarits du fondamental en 9 points et de l'atelier en 8 points (2) | Aucun gabarit n'existe ; ils seraient un canevas rigide, contraire aux Instructions §3 | Une liste de fonctions obligatoires, sans ordre imposé. R2 §6 |
| Versionner les dépendances de chaque fondamental (2) | Git suffit | Date de révision dans l'en-tête. R2 §6 |
| Taxonomie de concepts, graphe sémantique (3) | Coût de rétro-annotation de plusieurs dizaines de sessions ; le thème WP ne l'afficherait pas | Les dossiers et les TF portent le réseau. R3 §6 |
| Priorité « audience » (4) | Aucune donnée de trafic n'est accessible | Inapplicable sans export. R4 §8 |
| Rapport de santé mensuel (4) | Deviendrait une obligation de produire des constats | Trois lignes dans le rapport mensuel. R4 §5 |
| Validation humaine de chaque publication (1) | Contraire à l'autonomie retenue (D12) | Validation ciblée sur les sujets sensibles (É2) |
| Journal des décisions à créer, domaines à définir, structure du Fil à établir (5) | Ils existent déjà : `plan.md` §3, 7 codes thème, skill hebdomadaire | Compléter l'existant. R5 §0 |
| Monétisation par des services pédagogiques (1) | Le périmètre du Sentier n'est pas tranché (É4) | Prématuré |
| « Reporter quand les contrôles de qualité échouent » (6) | Quand un contrôle **technique** échoue, la routine corrige déjà et recommence. Le vrai manque est un **seuil éditorial** | Reformuler en « droit de ne rien publier » (É1) |

**Propositions acceptées avec un amendement** :
- un atelier peut mobiliser plusieurs fondamentaux, mais il garde un parent principal (R2 §6) ;
- la typologie des contradictions passe à quatre catégories, en ajoutant « périmètre » (R4 §4) ;
- les deux budgets, contexte d'un côté et vérification de l'autre (R5 §5, §7.6).

---

## Partie 3 — Zones d'incertitude

Ces points ne peuvent pas être confirmés depuis le dépôt. **[V]** Je n'ai pas d'accès en lecture à l'état réel de WordPress.

1. **État réel de WordPress.**
   - Les copies `/wiki-du-phare/` (environ 77 selon un document, 51 dans l'index) sont-elles encore en ligne ?
   - Catégories, menus, widgets et permaliens.
   - Révisions activées ou non.
   - Le thème affiche-t-il la date de modification ?
2. **Raisons historiques non documentées.**
   - Le motif de la protection de `02_Fonds` (« décision éditeur », sans justification écrite).
   - La non-publication du dossier Inflation.
   - L'origine de la règle « pas de 11ᵉ fondamental ».
3. **Exactitude actuelle de certains angles.** « Inflation en recul » (419) n'a pas été vérifié sur les données d'octobre 2026.
4. **Audience et usage réel.** Aucune donnée. Toute mesure d'utilité pour le lecteur est aujourd'hui impossible.
5. **Coûts.** Aucune mesure en tokens. Seule la taille des lectures en lignes est connue (R5 §5).
6. **Cadence voulue.** « Environ un article par jour » (message 6) contre le refus du calendrier (message 1). Le skill dit « un par jour ». Comme le déclenchement est manuel, la cadence réelle dépend des sessions du fondateur.
7. **Socle.** Il s'interrompt à la section Simone Weil (T12). La place exacte de Weil dans la ligne éditoriale n'est pas fixée.
8. **Recul.** La V5 a 6 jours. Deux Fils du Phare ont été produits pendant la mise en place et une seule mensuelle complète a eu lieu. **[D]** Aucune conclusion solide sur la tenue des cycles n'est encore possible.

---

## Partie 4 — Recommandations de convergence

### 4.1 Les six tensions

**Tension 1 — Cadence contre qualité**

| Option | Avantage | Limite |
|---|---|---|
| a. Un article par jour, obligatoire | Régularité visible | Publie le « moins mauvais » candidat certains jours |
| b. Cadence indicative avec droit de report | Cohérent avec le slow journalism | Risque de dérive vers la rareté |
| c. Cadence hebdomadaire cible (par exemple 5 à 7) avec report possible | Régularité et qualité | Un compteur à tenir |

- **Conséquence éditoriale** : un report motivé est un acte éditorial. Il doit être visible pour le fondateur, mais pas pour le lecteur.
- **Conséquence technique** : une sortie de plus dans le skill, une ligne en mémoire §1 et un compteur hebdomadaire dans l'état courant. Le coût est faible.
- **Recommandation [P]** : option **c**. Le seuil absolu est défini en É1, le report est tracé, et l'hebdomadaire signale plus de 2 reports dans la semaine.
- **[A]** La cible chiffrée revient au fondateur.

**Tension 2 — Continuité contre ouverture**
- **[D]** Le biais est structurel : si le Radar a un candidat fort, la veille se réduit à une vérification (skill, étape 3), et les fils actifs absorbent la majorité des articles.
- **Options** :
  - (a) un quota de sujets hors fils : c'est un quota, donc contraire au principe 9 ;
  - (b) au moins 1 candidat sur 5 sans lien avec un fil, noté sur ses seuls mérites ;
  - (c) un contrôle a posteriori.
- **Recommandation [P]** : **b + c**. On garantit qu'un candidat ouvert est examiné chaque jour, sans garantir qu'il gagne. L'hebdomadaire vérifie, grâce à la trace d'arbitrage (É12), si une actualité majeure a été écartée plusieurs jours de suite, et regarde la répartition par thème sur 30 jours.
- **Conséquence technique** : une ligne dans le skill et un compteur par thème. Aucun nouveau fichier.

**Tension 3 — Automatisation contre responsabilité**

| Niveau | Exemples | Contrôle proposé |
|---|---|---|
| Répétitif | ID, index, tags, maillage, `a-la-une`, `?p=`, état courant | Automatique, avec `verify_publication` |
| Courant | Choix du sujet, type, rédaction d'un sujet non sensible, ajout au Radar | Automatique, tracé (ligne « Arbitrage »), relu après coup par l'hebdomadaire |
| Sensible | Conflits armés, santé, élections, personnes nommées dans une affaire, procédure judiciaire en cours | **Brouillon** et publication par le fondateur **[A : liste]** |
| Structurel | Fondamentaux, Sentier, taxonomie, suppression ou dépublication, ligne éditoriale, routines | **Proposition seulement**, décision du fondateur, notée dans `plan.md` §3 |

- **Recommandation [P]** : ce tableau, qui constitue la rubrique 8 du référentiel.
- **Désaccord** avec une validation systématique : elle ferait du fondateur le goulot d'étranglement de la cadence.

**Tension 4 — Réseau contre simplicité**
- **Recommandation [P]** : le réseau est porté par le **texte**, c'est-à-dire une phrase qui justifie chaque lien. Seules **3 colonnes structurelles** sont ajoutées (É8). Le Fil du Phare et les dossiers sont les lieux où les connexions sont pensées.
- **Règle anti-rapprochement artificiel** : si l'on ne peut pas écrire la phrase qui dit *en quoi* deux articles se répondent, on ne fait pas de lien.
- Les positions détaillées figurent en R3 §6 et R4 §4.

**Tension 5 — Patrimoine contre obsolescence**
- **Recommandation [P]** :
  - un article ancien est **daté, pas obsolète** ;
  - trois gestes, du moins cher au plus cher : contextualiser (note « Depuis »), remettre à niveau, refaire ;
  - le déclencheur est l'usage (article cité, signalé, ou échéance survenue), jamais l'âge ;
  - un plafond d'une session de rénovation pour 4 à 5 articles produits.
- Le détail est en R4 §6.
- **[A]** Mention publique « Mis à jour le … » ; règle « cité → Remettre à niveau ».

**Tension 6 — Sobriété contre profondeur**
- **Recommandation [P]** : **deux budgets**.
  - Le contexte d'orientation est plafonné : état courant, Radar, liens au plus 5.
  - La vérification de l'article en cours n'est **jamais** plafonnée : sources des faits avancés, chiffres datés, citations.
- On économise sur les relectures (l'hebdomadaire lit l'en-tête et la conclusion avant le corps) et sur les recopies (É11), pas sur la vérification (R5 §5, §7.6).
- **[D]** Aujourd'hui, la séparation est respectée en pratique, mais elle n'est pas écrite.

### 4.2 Charte : avis sur les dix principes

Je n'ai pas de désaccord de fond. Je propose des **amendements de précision**, pour que chaque principe soit vérifiable.

| # | Principe | Amendement proposé |
|---|---|---|
| 1 | Compréhension | Aucun |
| 2 | Faits | « …à une source vérifiable, **et datée** lorsqu'il s'agit d'un fait d'actualité » |
| 3 | Incertitudes | S'en tenir à **certain / incertain / discuté**. La grille à 5 degrés n'est ni appliquée ni nécessaire |
| 4 | Indépendance | Ajouter : « …y compris par le choix des cadres intellectuels mobilisés » (É13) |
| 5 | Références | Aucun. C'est déjà la règle du gabarit Question |
| 6 | Révision | Ajouter : « …et la correction est **visible** pour le lecteur » (lié à la mention publique, [A]) |
| 7 | Patrimoine | « …lorsqu'une relation substantielle existe **et peut être énoncée dans le texte** » |
| 8 | Autonomie | Validable seulement après l'arbitrage sur l'étape 9 (É4) |
| 9 | Sobriété | Ajouter : « …ni pour tenir une cadence : **ne rien publier est une décision valide** » (É1) |
| 10 | Responsabilité | Renvoyer au tableau de la tension 3, qui définit « sensible » |

**[A]** Un 11ᵉ principe est possible : la **transparence sur l'usage de l'IA** (É15). Je ne le propose pas d'office : c'est un choix du fondateur.

**Statut de la charte** : RECOMMANDÉ. Rien n'est adopté avant validation.

### 4.3 Référentiel commun : consolider plutôt que créer

**[V]** Les 9 rubriques ont déjà un support, souvent dispersé. Je propose **de ne créer aucun nouveau document de référence**, mais de faire trois consolidations.

| Rubrique | Support actuel | Proposition |
|---|---|---|
| 1. Mission | Socle (.docx), message 6 §I | Une phrase en tête de la charte |
| 2. Principes | Socle, Instructions | **Charte** (§4.2) en **§0 des Instructions**, que les routines lisent déjà |
| 3. Types de contenus | Skills, `plan.md` §5 | Tableau unique dans le §0 des Instructions : 8 types, fonction en une ligne, routine productrice |
| 4. Architecture | `plan.md` §5, Taxonomie, manifeste Sentier | Inchangé jusqu'à l'export WP |
| 5. Processus de décision | Skills (source exécutable), D12 | Inchangé : le skill fait foi |
| 6. Qualité | Instructions, `verify_publication.py` | Ajouter les 3 règles d'É3 aux Instructions |
| 7. Maintenance | D17, `plan.md` §19 | Ajouter « contextualiser » et le déclencheur par l'usage |
| 8. Gouvernance | Dispersée (`CLAUDE.md` Interdits, skills) | **Nouvelle section courte dans `plan.md`** : le tableau de la tension 3 |
| 9. Journal des arbitrages | `plan.md` §3 (D1–D17) | **Ajouter 2 colonnes** : Justification, Statut (DÉCIDÉ / RECOMMANDÉ / À VÉRIFIER / À ARBITRER, avec qui a validé) |

**Ce qu'on transmet à ChatGPT** : le §0 des Instructions (charte et types) et `plan.md` §3 (journal), soit environ deux pages. Pas `plan.md` en entier (760 lignes).

**[P]** **Élagage** : un `README` de `00_Systeme/` qui liste les fichiers vivants, et les documents archivés regroupés dans un sous-dossier. Cette réorganisation de fichiers n'implique ni suppression ni changement de routine.

### 4.4 Collaboration : format de transmission

D'accord avec le format en 8 champs. Je propose trois ajustements :
- ajouter **« Réponse de ChatGPT »** entre la question et la décision humaine, sinon le contradictoire n'est pas conservé ;
- une fiche par sujet, dans `00_Systeme/Alignement/`, nommée `F-NNN_<sujet>.md`, au **Statut** pris parmi les 4 du message 6 ;
- une fiche n'est ouverte **que** pour un écart non couvert par une règle déjà DÉCIDÉE. Le reste se règle directement dans la routine.

### 4.5 Questions A à F

**A — L'architecture intellectuelle est-elle cohérente ?**
- **[V]** Il n'y a pas 5 niveaux mais 8 types : Actualité, Question, Application, TF, Fil, Dossier, fondamental, atelier. Le code index ne les distingue pas : `ACTU` couvre trois types, et `SENTIER` couvre à la fois des fondamentaux et des ateliers.
- **[D]** Fonctions mal séparées :
  - **Application et atelier** appliquent tous deux une grille à un terrain réel. L'un applique une question, l'autre une méthode.
  - **TF et fondamental** se chevauchent quand un TF expose une méthode.
- **[V]** Aucune Application n'a été publiée depuis la V5.
- **[P]** Distinguer par la finalité :
  - l'atelier fait **pratiquer** une méthode au lecteur (exercice) ;
  - l'Application **analyse** un terrain.

  Si cette distinction ne tient pas, il faut fusionner. C'est la question 1 adressée à ChatGPT.

**B — Le système peut-il apprendre de ses publications ?**
- **Oui, modestement**, par trois mécanismes qui reposent tous sur l'existant.
  1. La trace d'arbitrage (É12) permet de voir ce qui a été écarté et ce qui s'est révélé important ensuite.
  2. Le comité hebdomadaire mesure quelles Questions du Phare ont été reprises et lesquelles dorment au Radar.
  3. Le rapport mensuel ajoute trois lignes : signalements de correction, reports, répartition par thème.
- **[D]** La limite est l'absence de tout retour des lecteurs : le système apprend sa propre cohérence, pas son utilité.

**C — Comment introduire la contradiction ?**
- Au moment de l'écriture, la quotidienne relit déjà jusqu'à 5 articles liés ; elle écrit la nuance **dans l'article** et la signale. Dans l'hebdomadaire, la tension est mentionnée dans le Fil.
- Il faut 4 catégories : factuelle, interprétative, évolution, périmètre. Seule la contradiction factuelle déclenche une maintenance.
- Aucune comparaison automatique sur l'ensemble du stock (R4 §4).
- Contre les rapprochements artificiels : la règle de la phrase (tension 4).

**D — Comment mesurer la progression du savoir ?** Ce qui est réaliste, sans outil nouveau, à partir de l'index et de la mémoire :

| Mesure | Source | Mesurable aujourd'hui |
|---|---|---|
| Couverture : Questions du Phare reprises, ou en attente depuis plus de 30 jours | Radar, mémoire §1 | Oui |
| Diversité : répartition par thème sur 30 jours ; traditions des penseurs mobilisés | index, mémoire §1 (`--penseur`) | Oui (classement à la main pour les traditions) |
| Lacunes : domaines sans fondamental ; questions récurrentes sans dossier | manifeste, mémoire §2 | Oui |
| Cohérence des dossiers : articles rattachés, articles isolés | `build_hubs.py`, `verify_publication` | Oui |
| Utilité pédagogique des fondamentaux | — | **Non**, sans données lecteurs |

**E — Quel niveau d'autonomie est raisonnable ?** Voir le tableau de la tension 3. Les contrôles indispensables sont au nombre de trois :
- les contrôles de forme existants ;
- le brouillon pour les sujets sensibles ;
- la relecture a posteriori par l'hebdomadaire.

Rien de plus par article.

**F — Comment garder Le Phare simple ?**
- **Indispensable** :
  - l'index et ses scripts (`new_article`, `stage`, `daily_run`, `verify_publication`) ;
  - les skills quotidienne, hebdomadaire et mensuelle ;
  - l'état courant, le Radar et la mémoire ;
  - les Instructions et le socle ;
  - le manifeste du Sentier.
- **À simplifier** :
  - la triple copie des pistes et des échéances ;
  - les documents archivés de `00_Systeme/` ;
  - les 48 lignes wiki de l'index ;
  - les catégories à cinq logiques ;
  - le nommage `triptyque_minimal` ;
  - `plan.md`, à scinder entre décisions vivantes et historique.
- **À ne pas ajouter** :
  - les neuf relations typées et les 16 métadonnées ;
  - un graphe de concepts ;
  - un rapport de santé ;
  - des durées de validité ;
  - un nouveau fichier de référentiel.
- **Règle proposée** : toute nouvelle fonction doit remplacer ou fusionner une structure existante, ou répondre à un problème **observé** (R5 §7.8).

---

## Partie 5 — Questions à ChatGPT

Par ordre de priorité. Elles portent seulement sur ce qui demande un examen éditorial ; les faits sont établis plus haut.

1. **Application, atelier et Question** : leurs fonctions éditoriales sont-elles réellement distinctes pour le lecteur ? Si oui, quel critère les sépare ? Si non, lesquels fusionner ?
2. **Seuil de non-publication** : quels critères éditoriaux absolus font qu'aucun candidat ne mérite d'être publié un jour donné ? Comment éviter que ce droit devienne une pente vers la rareté ?
3. **Sujets sensibles** : quelle liste, courte et justifiable, doit passer par un brouillon validé par le fondateur ? Et sur quel critère : risque juridique, risque factuel ou atteinte à des personnes ?
4. **Étape 9 et développement personnel** : peut-on la recentrer sur « les conditions du jugement » (attention, fatigue, information) sans trahir la mission ? Ou doit-elle sortir du Sentier ?
5. **Diversité des cadres** : quelles traditions intellectuelles manquent au réservoir de penseurs pour que l'indépendance du principe 4 soit réelle et non déclarative ?
6. **Ouverture** : un candidat hors fil chaque jour, examiné sans obligation de gagner, suffit-il ? Que doit signifier « explorer un domaine nouveau » pour Le Phare ?
7. **Contextualiser ou actualiser** : quand une note datée « Depuis » suffit-elle, et quand l'honnêteté envers le lecteur exige-t-elle une réécriture ?
8. **Fils éditoriaux** : selon quels critères un fil trop large (12 articles, des sujets éloignés) doit-il être scindé ou clos ?
9. **Domaines** : quelle frontière entre `MONDE` et `POL` ? « Culture » doit-il devenir « Culture & Philosophie » ?
10. **Transparence sur l'IA** : quels arguments éditoriaux pour et contre une mention au lecteur ? La décision revient au fondateur.

---

## Partie 6 — Ordre de traitement proposé

Aucune étape n'est engagée avant l'accord du fondateur.

| # | Objectif | Dépendances | Risques | Résultat attendu | Validation |
|---|---|---|---|---|---|
| 0 | **Arbitrages bloquants** (liste ci-dessous) | Réponses de ChatGPT aux questions 1 à 4 et 10 | Décider sur des recommandations non examinées | D18 et suivantes dans `plan.md` §3, avec Justification et Statut | Fondateur |
| 1 | **Référentiel** : charte et tableau des types en §0 des Instructions ; section Gouvernance ; colonnes de `plan.md` §3 | Étape 0 | Modifier la ligne éditoriale par la bande | Deux pages transmissibles à ChatGPT | Fondateur (texte de la charte) |
| 2 | **Quotidienne** : report motivé ; ligne « Arbitrage » ; candidat hors fil ; brouillon pour les sujets sensibles ; Radar seule source des dates ; compteur du Radar ; avertissement de doublon | Étapes 0 et 1 | Alourdir le skill | Un skill de même taille ou plus court ; sorties tracées | Fondateur (liste des sujets sensibles) ; Claude (implémentation) |
| 3 | **Protection par le rôle** : 90 fondamentaux ; garde-fou dans `wp_push_draft.py` | Étape 0 | Bloquer la rénovation de 159 et 198 | Garde-fou fondé sur le manifeste | Fondateur |
| 4 | **Pilotes de maintenance** : Inflation (étape 1 en lecture seule, R4 §7) ; micro-pilote « Depuis » | Étape 0 (feu vert) | Coût en sessions ; angle périmé | Tableau d'inventaire, puis plan soumis | Fondateur à chaque publication |
| 5 | **Export WP** en lecture seule : catégories, tags, menus, wiki, révisions | Fourni par le fondateur, ou accès API en lecture | Aucun (lecture) | Décisions sur le wiki (301) et la taxonomie (É7) | Fondateur |
| 6 | **Sentier** : étape 9, présentations concurrentes, lacune « institutions » | Étape 0 et question 4 à ChatGPT | Dépublications ; liens cassés | Plan de recentrage par étape | Fondateur (structurel) |
| 7 | **Simplification** : `README` de `00_Systeme`, archives regroupées, lignes wiki marquées, scission de `plan.md` | Étapes 1 et 5 | Casser un renvoi interne | Moins de surface, rien de supprimé | Claude, puis contrôle du fondateur |

**Liste consolidée des arbitrages du fondateur** (questions de R1 à R5, sans doublon) :
1. Droit de ne rien publier, et cible de cadence (É1, tension 1).
2. Sujets sensibles en brouillon : principe et liste (É2).
3. Mention de l'IA au lecteur (É15).
4. Sentier :
   - 9 étapes, ou 8 plus un bonus ;
   - sort de l'étape 9 ;
   - présentations concurrentes 007, 113 et 217 (É4).
5. Fondamental « institutions et droit », ce qui suppose de lever la règle « pas de 11ᵉ fondamental » (É6).
6. Protection par le rôle, et sort des 199 FOND anciens (É5).
7. Wiki :
   - les copies sont-elles en ligne ;
   - redirections 301 ;
   - page 413 (R3).
8. Export WP, ou accès API en lecture seule (É7).
9. Colonnes `Dossier`, `Origine` et `Fondamental` dans l'index (É8).
10. Pilote Inflation, et article candidat pour le micro-pilote « Depuis » (É9).
11. Mention publique « Mis à jour le … » ; révisions WP (É10).
12. Règle « cité → Remettre à niveau » (É10).
13. Export d'audience, sinon abandon de ce critère (Partie 3).
14. Liste de sources de veille de référence, ou jugement de Claude (É3).
15. Trace d'arbitrage quotidienne, au prix d'une ligne par jour (É12).

**Ordre recommandé si le fondateur ne peut trancher que trois points d'abord** : 1, 2 et 4. Ils conditionnent la charte (principes 8, 9 et 10) et la quotidienne.
