# État des lieux du Phare — 12 octobre 2026

*Destiné à ChatGPT, avant les six messages du plan d'alignement. Les chiffres viennent de l'index éditorial, de l'inventaire de rénovation et du manifeste du Sentier.*

## 1. Volumes (528 lignes d'index, avril → octobre 2026)

- **Par type** : 259 fondamentaux (FOND), 132 SENTIER, 72 actualités (ACTU, qui regroupent Actualité, Question et Application), 49 textes fondateurs, 12 dossiers, 2 briefings, 2 synthèses.
- **Par thème** : Culture 175, Tech 87, Monde 78, Science 72, Politique 45, Économie 41, Climat 30.
- **Par statut** : 502 publiés, 15 archivés, 11 brouillons WordPress jamais publiés.
- **Sentier du Savoir** : 9 étapes, chacune avec un hub et 10 fondamentaux. Les étapes vont de la culture générale à l'équilibre corps-esprit, en passant par la pensée critique, l'argumentation, l'expertise, les langues, la méthode scientifique, la transmission et le lien entre les savoirs.

## 2. Fonctionnement actuel (plan v5.7)

- **Quotidienne** : un seul article par jour. Le type est choisi **après** le sujet : Actualité, Question du Phare, Application, et Texte fondateur à titre exceptionnel (D12). Elle s'appuie sur trois lectures : l'état courant (généré automatiquement), le Radar éditorial et la veille web.
- **Hebdomadaire** : le Fil du Phare (synthèse publiée, catégorie `cycle`), le suivi des fils éditoriaux et le comité du Radar, qui trie, fusionne et hiérarchise les suites.
- **Mensuelle** : dossiers, textes fondateurs, ateliers du Sentier (un atelier = la mise en pratique d'un fondamental existant), audit, synthèse du mois et cap du mois.
- **Rénovation** (D17) : met l'ancien stock au format actuel en gardant le même ID, la même URL et le même slug. Le lot 1 sert à trier (décisions humaines), le lot 2 à remettre à niveau la navigation, le lot 3 à réécrire.
- **Outils** :
  - un registre canonique (`index_editorial.csv`) ;
  - une mémoire éditoriale partagée par les routines ;
  - le Radar, qui compte 30 entrées actives au plus ;
  - `verify_publication`, qui contrôle les liens, le maillage et le tag `a-la-une`, sans lequel un article est invisible sur le site (D15).
- **Autres décisions** :
  - le triptyque ACTU + TF + SENTIER est archivé (D5) ;
  - `02_Fonds/` est réservé à l'éditeur humain (D8) ;
  - les titres portent des préfixes (« Question du Phare - », etc.) (D16) ;
  - le socle éditorial fait référence et tout écart est signalé (D10).
- **Fils actifs en octobre** :
  - « Le prix de l'invisible » ;
  - « Capacités proclamées ou démontrées » ;
  - « Mesurer ou juger » (dossier et atelier publiés) ;
  - « Qui contrôle le contrôleur ? » ;
  - « Héritages ».

  Les catégories Politique, Monde, Économie et Culture sont sous-représentées dans l'actualité récente.

## 3. Stock ancien (inventaire de rénovation)

- **Au format actuel** : 48 articles.
- **À remettre à niveau** : 61 articles, sans réécriture (navigation, emoji dans le titre, liens `?p=`).
- **À refaire** : 87 articles. Il s'agit surtout d'articles de l'époque triptyque, de 10 fondamentaux d'étape, de 6 textes fondateurs et de 5 paires de doublons à fusionner.
- **Hors périmètre** : 317 articles, soit 259 fondamentaux de `02_Fonds/` (éditeur humain), 50 pages du wiki et 8 pages de rubrique.
- **Mécanisme** : les routines signalent un ancien article sans le modifier. Pour un fondamental, la rénovation rédige une proposition que l'éditeur valide et pousse lui-même. Une première proposition est faite (2026-177).

## 4. Écarts et zones floues

1. **Fondamental d'étape ou atelier ?** Selon le plan, un ancien SENTIER doit devenir l'atelier d'un fondamental. Or les fondamentaux d'étape rénovés (159, 198) sont restés des fondamentaux, et le validateur les rejette : chemin `05_Sentier/<sous-dossier>`, catégorie différente de `sentier-du-savoir`, tag de thème absent.
2. **Méthodes ou bien-être ?** On présente le Sentier comme un apprentissage de méthodes. Pourtant, l'étape 9 et plusieurs séries (Accords toltèques, sommeil, méditation, hygiène de vie) relèvent du développement personnel.
3. **Numérotation des étapes** : plusieurs slugs ne correspondent pas au numéro de l'étape (l'étape 7 a pour slug `etape-5-…`, l'étape 9 `etape-8-…`, l'étape 3 reprend le slug de l'étape 4). Le hub de l'étape 1 n'a pas d'URL.
4. **Lacune institutions et droit** : aucun fondamental ne traite du fonctionnement des institutions, alors que l'actualité politique y renvoie sans cesse.
5. **Dossier Inflation** (11 articles, 419–428 et 435) : jamais publié. Il faudrait dater ses faits avant toute publication.
6. **Taxonomie hétérogène** : les catégories WordPress `non-classe` (11 articles) et `le-phare-info` (25) servent de fourre-tout, et certains thèmes ne concordent pas entre le fichier et l'index (198 est MONDE dans l'un, CULTURE dans l'autre).
7. **Poids de l'ancien** : 87 % du stock précède le format actuel. Au rythme d'une session de rénovation de temps en temps, le rattrapage prendra des mois.

## 5. Questions en retour

1. Le Sentier doit-il garder ses fondamentaux de bien-être, ou se recentrer sur les méthodes intellectuelles ? Faut-il ouvrir une étape ou un fondamental sur les institutions et le droit, alors que créer un 11e fondamental est aujourd'hui interdit ?
2. Un fondamental d'étape rénové reste-t-il un fondamental, ou devient-il un atelier ?
3. Le wiki du Phare (50 pages) a-t-il encore un rôle, ou doit-il se fondre dans le Sentier ?
4. Dossier Inflation : faut-il le publier après réécriture, l'archiver ou le fondre dans un dossier plus récent ?
5. Faut-il renuméroter les slugs des étapes, au prix de redirections, ou les laisser en l'état ?
6. Quelle part du temps éditorial accorder à la rénovation face à la production nouvelle ?
