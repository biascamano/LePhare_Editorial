# Réponse de Claude — Message 4/6 (actualité, savoir durable, rénovation)

**Date : 12 octobre 2026.** Constats tirés du dépôt (index, skills, `plan.md`, scripts) au commit `5ef6fd5`. Rien n'a été modifié : ni routine, ni index, ni WordPress.

Statistiques recalculées pour cette réponse à partir de `index_editorial.csv` et des fichiers locaux. Leurs limites sont signalées au fil du texte.

---

## 0. Trois corrections préalables

1. **« La V5 prévoit » les relations `issu-de`, `prolonge`, `contredit`, etc. (VII) : c'est inexact.** Aucune de ces relations n'existe dans le dépôt. Le seul lien typé réel est `Article precedent (ID)` (en-tête et `--previous`), qui correspond à `issu-de`. Il s'y ajoute `--dossier` et le lien Sentier de la navigation. `Articles_lies` est une liste non typée (cf. réponse 3). Ces neuf relations sont donc une **proposition nouvelle**, à juger comme telle (§3 ci-dessous).
2. **« Aucune politique de maintenance n'a été formellement validée » (III.A) : c'est partiellement inexact.** La décision D17 (`plan.md` §19, 2026-10-06) organise la rénovation du stock :
   - une routine dédiée ;
   - trois lots ;
   - la règle « même ID, même URL, même slug » ;
   - les faits anciens gardés datés, avec un encadré « Depuis » sourcé ;
   - toute dépublication ou suppression soumise à décision humaine.

   Cette politique porte sur la **forme** (navigation, format, doublons). Elle ne dit rien de la **validité des faits**. C'est là le vrai manque.
3. **Le dossier Inflation compte 11 brouillons et non 10.** Il y a les 10 articles (419 à 428), auxquels s'ajoute 435 (Ormuz), classé DOSSIER mais rattaché à la mini-encyclopédie Iran (cf. réponse 3).

---

## 1. Question 14 — points E1 à E7

| # | Point | Constat |
|---|---|---|
| E1 | Répartition réelle | **Stock publié** (hors copies wiki) : 452 articles, dont 259 fondamentaux, 77 SENTIER, 67 ACTU, 44 TF, 2 synthèses, 2 briefings et 1 dossier (559). **Depuis la V5** (5 au 12 octobre, IDs 531 à 566) : 23 Actualités, 8 Questions, 0 Application, 1 TF, 1 Dossier, 1 atelier et 2 synthèses, soit **36 publications en 8 jours**. |
| E2 | Quotas | **Aucun.** La quotidienne interdit le type « pour équilibrer ». La mensuelle ne fixe que des plafonds (« 0 est une réponse valide », ateliers de 0 à 2). Le « cap du mois » signale les catégories sous-représentées « sans forcer ». |
| E3 | Déclenchement des TF | Dans la quotidienne, un TF est **exceptionnel** : seulement quand « un concept devient nécessaire à plusieurs articles ». Il relève surtout de la mensuelle. Aucun critère n'est mesurable : c'est un jugement de la routine. |
| E4 | Création des Questions | Chaque Actualité se termine sur une Question du Phare, qui entre au **Radar, bloc 2**. La quotidienne peut ensuite la développer (sorte B, ou prompt `type question — sur <ID>`). La variante `paire` produit les deux le même jour. Mécanisme réel et actif : 8 Questions en une semaine. |
| E5 | Liens actualité ↔ dossiers | Mécanisme réel mais **à peine utilisé** : option `--dossier` à la création, recherche `index_lookup.py --dossier`. Un seul dossier est publié (559). Pas de colonne « dossier » dans l'index (cf. réponse 3). |
| E6 | Critères des contenus durables | « Durabilité » est l'un des cinq critères de notation de la quotidienne (Faible / Moyen / Fort). Pour la mensuelle, un dossier se justifie quand « plusieurs articles différents convergent vers une même question durable ». Ces critères sont qualitatifs, et il n'existe pas de grille plus précise. |
| E7 | Contradictions entre la quotidienne et la V5 | **Pas de contradiction de fond.** Les trois horizons de ChatGPT recoupent l'existant : Événement = Actualité ; Phénomène = Question, Application, Dossier, synthèses ; Connaissance = TF, Sentier. Trois écarts de pratique : (a) **aucune Application** depuis la V5 ; (b) le rythme (36 en 8 jours) dépasse « un article par jour », sujet du message 5 ; (c) le dossier mensuel est publié dans la catégorie `dossier-hebdomadaire`, nom hérité. |

**Accord** sur l'absence de quotas, sur le refus des essais abstraits (« l'actualité ancre la pensée ») et sur les trois horizons, qui servent de grille de lecture. Je ne propose pas d'en faire un champ supplémentaire : le type suffit à les déduire.

---

## 2. Politique existante : ce qui est réel, ce qui est documenté, ce qui manque

| Sujet | Réel (outillé ou pratiqué) | Seulement documenté | Absent |
|---|---|---|---|
| **Corrections** | Le texte est corrigé dans la copie locale, puis `wp_refresh_body.py` remplace le corps sur WordPress. | — | **Aucune mention publique de correction** (déjà signalé en réponse 1). Pas de distinction entre coquille et erreur de fond. |
| **Actualisations** | Lot 3 : réécriture ; faits anciens gardés datés ; encadré « Depuis » seulement s'il est sourcé. 4 articles rénovés à ce jour. | « Depuis » est défini dans `plan.md` §19.3 et dans le skill. | Rien ne **déclenche** une actualisation pour des raisons factuelles : l'inventaire classe selon les liens et le format, jamais selon le risque d'erreur. |
| **Dates** | La date de publication WP n'est jamais modifiée (le refresh n'envoie que le corps et, au besoin, le titre). WordPress met à jour sa date de modification à chaque refresh. `Date_derniere_maj` existe dans l'index. | — | Pas de « Mis à jour le … » visible pour le lecteur. On ne sait pas si le thème affiche la date de modification. |
| **Archivage** | `Statut=archive` dans l'index (15 brouillons), qui les retire des inventaires. | — | Rien côté WordPress : ces brouillons restent des brouillons. Il n'y a pas d'archivage d'un article **publié**. |
| **Suppressions** | Lot 1 : sur décision humaine, 28 fichiers wiki identiques supprimés **en local** et leurs lignes d'index retirées. | Le skill exige un accord explicite pour toute dépublication ou suppression. | Aucune suppression WordPress n'a été faite par les routines. |
| **Redirections** | Aucune. | `Sentier_dedoublonnage_wiki.md` : 301 « action éditoriale WP, pas automatisée ». | Pas d'inventaire des redirections existantes, et je n'ai pas accès au plugin. |
| **Historique** | Git, pour chaque fichier local, avec les messages de commit. Remarque `Rénové (Routine rénovation) YYYY-MM-DD` dans l'index. Révisions WordPress, à condition qu'elles soient activées, ce que je ne peux pas vérifier. | — | Pas de journal public, et pas de motif de modification lié à un article ailleurs que dans git. |
| **Signalement** | `Signalements_renovation.md` : les routines signalent sans rénover (plan v5.6). `Propositions_fonds/` : les propositions pour les fondamentaux sont remises à l'éditeur (v5.7). | — | — |

**Conséquence** : les propositions VI (la quotidienne signale sans rénover) et VIII cas 6 (fondamental → proposition sous contrôle humain) **existent déjà**. Ce qui manque :
- un déclencheur factuel ;
- une trace publique des changements substantiels ;
- une action « contextualiser » distincte de « réécrire ».

---

## 3. Évaluation du stock

**Volume et dates** (date de publication WP ; total 452) : une première vague entre mars et avril 2025 (89 articles, surtout des fondamentaux), une deuxième entre septembre et octobre 2025 (135), puis décembre 2025 à janvier 2026 (74), l'ère triptyque en mai et juin 2026 (86) et la V5 en octobre 2026 (36). **Hors fondamentaux**, 193 articles, dont 120 publiés en 2026.

**Dossiers** : un seul publié (559, « Mesurer ou juger »). Onze brouillons : Inflation (419 à 428) et 435.

**Articles isolés** (aucun lien entrant depuis un autre fichier local, fondamentaux exclus de la cible) : **61**, soit 35 SENTIER, 14 ACTU, 11 TF et 1 briefing. Ce chiffre est **surestimé** :
- environ 70 copies locales sont tronquées par rapport à WordPress, donc des liens entrants manquent ;
- les menus et pages WordPress ne sont pas vus ;
- 566 date d'hier, il est isolé par nature ;
- les pages rubriques (058 à 066) sont isolées par construction.

Il ne faut donc pas le lire comme une liste d'articles à traiter.

**Besoin d'actualisation** : il **ne peut pas être mesuré** honnêtement à partir des données. Un filtre grossier (chiffres + marqueur de présent comme « aujourd'hui » ou « actuellement ») retient 18 articles hors fondamentaux : 9 ACTU, 5 TF, 2 SENTIER, 2 synthèses. C'est un repère, pas un diagnostic : beaucoup de ces présents sont légitimes dans un article daté.

**Inventaire de rénovation (aujourd'hui)** : 48 au format actuel, 87 à refaire, 61 à remettre à niveau, 0 à trier, 0 signalé. Le lot « Refaire » est passé de 53 à 87 depuis le 6 octobre. Une cause probable : la règle « cité par un article actuel → Refaire » fait monter les anciens articles que les nouveaux citent. **Plus la quotidienne relie, plus le lot 3 grossit.** C'est un signal de coût à garder en tête (§6).

---

## 4. Détection des contradictions

**Aujourd'hui** : rien. Aucun script ni aucune routine ne compare des affirmations entre articles.

**Ce qui est faisable à coût raisonnable** :
- **Au moment de l'écriture.** La quotidienne relit déjà jusqu'à 5 articles liés avant de rédiger. Si l'un d'eux est démenti, nuancé ou dépassé par les faits du jour, elle peut :
  - l'écrire **dans l'article** (« Contrairement à ce que nous écrivions le … ») ;
  - le signaler dans `Signalements_renovation.md`, avec la nature du constat.

  Le coût est quasi nul, car la lecture a déjà lieu.
- **Dans l'hebdomadaire.** Il relit les articles de la semaine pour le Fil du Phare. Il peut repérer une tension entre eux et la mentionner dans le Fil. C'est un contenu éditorial, pas un audit.

**Ce que je déconseille** : une détection automatique sur tout le stock (comparaison deux à deux, embeddings, appels modèle). Avec environ 450 articles, cela représente des dizaines de milliers de paires. Le coût est élevé et les faux positifs sont massifs :
- deux chiffres de dates différentes, qui relèvent d'une évolution et non d'une contradiction ;
- des périmètres différents (zone euro / France) ;
- un article qui expose une thèse pour la réfuter ;
- deux penseurs mobilisés en opposition volontaire ;
- des sujets voisins, mais pas la même question.

**Typologie de ChatGPT** (factuelle / interprétative / évolution) : je suis d'accord, et j'ajoute une quatrième catégorie, « différence de périmètre ». Seule la contradiction **factuelle** appelle une action de maintenance. Les deux autres sont des contenus à écrire.

**Sur les neuf relations** : je recommande de **ne pas** les introduire comme métadonnées. Ce qui compte pour le lecteur, c'est la phrase et le lien **dans le texte**. Une relation `contredit` dans l'index, invisible sur le site et non maintenue, serait une dette de plus. Si on veut une trace, la colonne `Origine` proposée en réponse 3 suffit pour `issu-de`, et le signalement suffit pour `contredit`.

---

## 5. Compatibilité avec les routines

Les six statuts de ChatGPT recoupent largement l'existant. Je propose de **les faire correspondre aux lots** plutôt que de créer un champ nouveau :

| Statut proposé | Équivalent existant | Écart |
|---|---|---|
| CONSERVER | « Format actuel » / hors lot | — |
| ACTUALISER | Lot 3 + encadré « Depuis » | Déclencheur factuel absent |
| CONTEXTUALISER | — | **À créer** : note datée en tête ou en pied d'article, sans réécriture. C'est l'action la moins chère et la plus honnête pour un article d'actualité ancien. |
| RELIER | Lot 2 (navigation v3) | — |
| CONSOLIDER | Doublons de titre fusionnés au lot 3 | Pas de procédure pour un groupe de plus de deux articles (cas Inflation) |
| ARCHIVER / RETIRER | Lot 1 (`Statut=archive`, décision humaine) | Rien pour un article publié : dépublication, 301 |

**Répartition proposée**, sans alourdir les routines :
- **Quotidienne** : aucune tâche nouvelle, hormis le point du §4 (écrire la nuance dans l'article et signaler). Correction prioritaire : en cas d'erreur grave découverte, la quotidienne la **signale en tête de rapport**, et l'utilisateur décide si une session de rénovation ciblée (`routine renovation — <ID>`) passe avant l'article du jour. Je ne veux pas que la quotidienne corrige elle-même.
- **Hebdomadaire** : rien de nouveau, sauf mentionner dans le Fil une tension entre articles de la semaine quand elle existe. Le tri des signalements revient à la rénovation, pas au comité.
- **Mensuelle** : elle audite déjà la navigation et les articles isolés du mois. On y ajoute **trois lignes** au rapport : compteurs de l'inventaire avant et après, signalements ouverts, décisions humaines en attente. Je ne propose pas de « rapport de santé » plus large : il deviendrait une obligation mensuelle de produire des constats.
- **Rénovation** : la seule à exécuter. Ajouter l'action « contextualiser » et faire passer les signalements factuels en tête (c'est déjà le cas pour les signalés).

**Appels modèle** : aucun supplément, puisque tout se passe dans des lectures déjà faites. **Opérations WordPress** : uniquement `wp_refresh_body.py` article par article, avec `verify_publication.py` ; aucune opération en masse.

---

## 6. Analyse critique

- **Faut-il conserver toutes les versions publiques ?** Non. Git conserve toutes les versions locales et WordPress garde ses révisions. Pour le public, une ligne datée suffit en cas de changement substantiel (« Mis à jour le … : [nature] »). Pas de version archivée consultable.
- **Quel degré de traçabilité ?** Trois niveaux suffisent pour un petit média :
  - la coquille : rien ;
  - le changement de fond : une ligne publique et la `Remarque` d'index ;
  - la suppression ou la dépublication : décision humaine notée dans `plan.md` ou dans les signalements.

  Les 16 métadonnées du §IX sont disproportionnées. La moitié existe déjà (ID, URL, titre, type, thème, dates, Question, Sentier). Le reste (concepts, relations, statut de maintenance, prochaine vérification) ne serait pas maintenu.
- **Comment éviter que la maintenance coûte plus que la production ?** C'est un risque **réel et déjà visible** : le lot 3 est passé de 53 à 87 en six jours, et sa durée estimée est de 20 à 30 sessions. Je propose :
  1. une maintenance **déclenchée par l'usage** plutôt que par l'âge : un ancien article n'est examiné que s'il est cité par un nouvel article, s'il est signalé, ou si un fait attendu (Radar `à échéance`) est survenu ;
  2. **revoir la règle « cité → Refaire »**, pour qu'une citation déclenche « Remettre à niveau » et non une réécriture ;
  3. un **plafond** : par exemple, une session de rénovation pour quatre à cinq articles produits.
- **Quelles mises à jour automatiser ?** Celles qui sont déjà automatisées : tag `a-la-une`, liens `?p=`, navigation. On peut y ajouter, à faible risque, un contrôle des **liens externes morts** dans les Repères de sources, sous forme de rapport et non de correction, car certains sites bloquent les robots (faux positifs). Les faits, eux, ne doivent jamais être mis à jour automatiquement.
- **Une durée de validité par type ?** Non, en tant que calendrier : il produirait exactement les faux « obsolète » que ChatGPT veut éviter. Tout au plus une indication par horizon : une Actualité vaut à sa date, sans échéance ; une Question ou une Application, tant que les exemples tiennent ; un TF ou un Sentier, sans échéance. Le déclencheur reste l'usage (point 3).
- **Comment éviter les faux « obsolète » ?** Trois règles :
  - un article n'est jamais qualifié d'obsolète sans **un fait précis, sourcé et daté** qui le contredise ;
  - un article d'actualité ancien est **daté**, pas obsolète : on le contextualise, on ne le réécrit pas ;
  - le constat est un signalement, et la décision revient à la rénovation, voire à l'humain pour un retrait.
- **Comment vérifier les sources anciennes sans parcourir tout le web ?** On ne vérifie que **l'affirmation qui pose question**, au moment où l'article est cité ou signalé, par une recherche ciblée sur ce fait. Jamais un balayage du stock. Pour les chiffres réguliers (inflation, emploi, climat), il vaut mieux renvoyer à la source primaire (INSEE, Eurostat, BCE) qu'actualiser le nombre.

---

## 7. Chantier pilote : Inflation

C'est le bon pilote, pour trois raisons : un groupe fermé, des brouillons jamais publiés (donc **aucun risque public** tant que rien n'est publié), et il teste à la fois actualiser, consolider et archiver. La proposition de consolidation (10 articles → 5 ou 6 contenus) figure en réponse 3. J'y ajoute le protocole :

1. **Inventorier** (lecture seule) : pour chacun des 10 articles, préciser la version retenue (V1 / V2), le nombre de mots, la question traitée, les chiffres datés ou non, les sources avec ou sans URL, et les recoupements avec 005, 559 et 560. Livrable : un tableau.
2. **Vérifier l'angle** : « inflation en recul en Europe » (419) est-il encore vrai en octobre 2026 ? Une recherche ciblée (Eurostat, BCE) suffit.
3. **Plan soumis à l'utilisateur** : pour chaque article, conserver, fusionner, transformer ou archiver. Aucune écriture avant accord.
4. **Exécution un par un** : réécriture au format actuel, publication, `verify_publication.py`. Les articles archivés passent en `Statut=archive` ; leurs brouillons WordPress ne sont pas supprimés.
5. **Réversibilité** : tant qu'un brouillon n'est pas publié, tout est réversible (git et brouillon WP). Après publication, un retour en arrière consiste à dépublier, sur décision humaine.
6. **Bilan** : temps passé, nombre de contenus produits, règles confirmées ou à revoir. Ce bilan sert à décider si la consolidation devient une procédure du lot 3.

Ce pilote ne teste **pas** la contextualisation d'un article publié. Je propose un second micro-pilote : **un seul** article d'actualité de 2025 cité par un article récent, qui reçoit une note « Depuis » datée et sourcée, sans réécriture.

---

## 8. Désaccords et réserves

- **Les neuf relations typées** (VII) : non, ni comme métadonnées ni comme principe d'implémentation. Une phrase et un lien dans le texte valent mieux (§4).
- **Les 16 métadonnées** (IX) : non. Au plus, les trois colonnes proposées en réponse 3 (`Dossier`, `Origine`, `Fondamental`).
- **La priorité 3 « audience »** (V) : je n'ai **aucune donnée de trafic**, ni accès aux statistiques WordPress ou à Search Console. Elle reste inapplicable tant que le fondateur ne fournit pas un export.
- **Le « rapport de santé mensuel »** (VI) : à réduire aux trois lignes du §5.
- **La correction prioritaire déclenchée par la quotidienne** (VI) : elle doit être signalée, pas exécutée (§5).

---

## 9. Questions au fondateur

1. **Mention publique des mises à jour** : acceptes-tu une ligne « Mis à jour le … : [nature] » en pied d'article pour les changements substantiels ? Et le thème affiche-t-il la date de modification WordPress ?
2. **Statistiques d'audience** : peux-tu fournir un export (WordPress, Jetpack ou Search Console) des articles les plus consultés ? Sinon, on abandonne la priorité 3.
3. **Règle « cité → Refaire »** : acceptes-tu qu'une citation par un article récent déclenche « Remettre à niveau » au lieu d'une réécriture, pour contenir le lot 3 ?
4. **Pilote Inflation** : feu vert pour l'étape 1 (inventaire en lecture seule) dès la fin de l'alignement ? Et pour le micro-pilote de contextualisation : as-tu un article de 2025 en tête ?
5. **Révisions WordPress** : sont-elles activées, et combien en garde-t-on ? C'est la seule trace de l'état antérieur sur le site.
