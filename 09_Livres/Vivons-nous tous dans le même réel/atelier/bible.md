# Bible — Vivons-nous tous dans le même réel ?

Canon du livre. Amorcée le 2026-10-13 depuis `Srategie.docx`, `critiques.docx` (lecture de la V1) et la V3. Les points marqués **[à valider]** attendent l'auteur ; une fois validés, ils ne changent que par une décision (`decisions.md`).

## Place dans la collection

Livre 1 de la collection (nom en réflexion : « Les Grandes Questions » / « La Carte des Grandes Questions » ; voir `../../carte_des_questions.md`). Territoire principal : **le Réel**, abordé par la perception.

## Promesse

> Question d'entrée : **Vivons-nous tous dans le même réel ?**
> Question de sortie : **Comment construisons-nous notre expérience du monde ?**

Ce que le lecteur emporte : ce qu'il voit n'est pas le monde mais *sa* rencontre avec le monde ; chaque espèce, chaque personne en rencontre une part différente ; la science, le langage et l'art sont nos moyens de mettre ces parts en commun. Il referme le livre plus curieux, pas plus sûr de lui.

(Section recopiée telle quelle dans le prompt du `lecteur-critique`.)

## Lecteur cible

Adulte curieux, non spécialiste, de 16 à 80 ans ; lit le soir, par chapitres courts ; n'a jamais lu de neurosciences. **[à valider]** : lecture possible dès 13–14 ans ?

## Périmètre

| Dans le livre 1 | Hors livre 1 (→ `reserve.md`) |
|---|---|
| Les sens, leurs limites, les illusions | Cerveau prédictif, Friston, inférence active → Livre 2 |
| Les autres espèces : chien, abeille, chauve-souris, serpent, pieuvre ; Umwelt (von Uexküll), Darwin | Mémoire détaillée, reconstruction des souvenirs → Livre 2 |
| Les autres humains : culture, éducation, attention, premières notions de mémoire, émotions (sans le fonctionnement cérébral) | Damasio, marqueurs somatiques, intéroception détaillée → Livre 2 |
| Le jardin commun : science, langage, art, monde partagé | Libet, libre arbitre, conscience, émergence → Livre 3 |
| | Le soi, l'identité, le sujet ; Jung → Livre 4 |
| | IA (« nouvel interlocuteur ») → Livre 3 ; silhouette dans l'épilogue seulement (D6) |

Architecture indicative (stratégie) : Prologue · P1 Nous croyons voir le monde · P2 Les autres espèces · P3 Les autres humains · P4 Le jardin commun · Épilogue (le portail).

## Dispositif

- **Lieu** : un jardin ordinaire derrière un portail de bois. Il reste le même d'un livre à l'autre : presque un personnage. Repères fixes : le portail, le gravier, le vieux chêne, le ruisseau, le banc, la mousse, la cabane.
- **Le vieil homme** : guide qui pose des questions plus qu'il ne répond ; ramasse des objets (feuille, pierre…) pour faire voir. Ne fait jamais de cours magistral.
- **Le lecteur** (« vous ») : personnage qui marche, doute, répond ; bascule finale vers le « je » (« Je crois… »).
- **Yuki** (D8) : le chien du narrateur, venu de la V0. C'est lui qui s'arrête devant le portail et fait entrer « vous » ; il flaire, s'immobilise, revient sur ses pas, trouve ce que vous ne voyez pas (la plume). Il ne parle jamais, n'est jamais un sage déguisé : seulement un vrai chien, que le lecteur apprend à regarder. Présent au prologue, au 010 et à l'épilogue ; ailleurs, une phrase de passage au plus un chapitre sur trois.
- **Figures secondaires** : le peintre, la botaniste, l'enfant, la petite fille et son grand-père ; le renard, les abeilles, le merle. Le musicien et l'étudiante sont retirés (PLAN v4).
- **Objets** : la plume (trouvée grâce à Yuki), la loupe, la boussole, la graine, posées sur la table de pierre ; la clé du portail à l'épilogue.
- Le jardin ne fait pas de magie : tout ce qui s'y voit existe dans un vrai jardin.

## Voix

- Deuxième personne (« vous »), présent, phrases simples ; le vieil homme tutoie (D7).
- **En paragraphes** (D9) : la narration avance par paragraphes de 3 à 6 phrases, qui tiennent ensemble un geste, une perception et une pensée. Pas une phrase par ligne. La ligne isolée est un effet, réservé aux bascules : 3 au plus par chapitre, hors dialogues.
- Les dialogues restent brefs et vivants, mais une réplique du vieil homme peut tenir plusieurs phrases : il raconte, il ne lance pas des aphorismes.
- Ton : émerveillement sans mièvrerie, honnêteté sur ce qu'on ne sait pas.
- Science racontée par des scènes et des expériences réelles ; le vieil homme nomme et date le savant en une phrase (D5) ; jamais d'argument d'autorité.

## Règles mesurables (contrôlées par `tools/livre.py stats`)

Issues de la critique de la V1 et des mesures de la V3 (`mesures/v3.md`).

| Règle | V3 | Cible |
|---|---|---|
| Longueur totale | 43 500 mots | 45 000–55 000 mots (180–220 pages en mise en page aérée) (D4) |
| Paragraphes ≤ 6 mots (répliques comprises) | 69 % | ≤ 25 % (D9) |
| Plus longue suite de paragraphes courts | jusqu'à 33 | ≤ 4, et 3 lignes isolées de bascule par chapitre au plus (D9) |
| Formule de 4 mots présente dans ≥ 5 chapitres | « le vieil homme reprend » : 35 | aucune au-delà de 12 chapitres |
| Fins de chapitre sur une question | 7 / 91 | varier : question, image, coupe nette, enchaînement — aucun type > 50 % |
| Nombre de chapitres | 91 (≈ 480 mots) | 30–45 (D4) |

Règles non mesurées, vérifiées en critique :
- Pas de transition-résumé (« Depuis le début de ce livre… ») plus de 2 fois dans tout le livre.
- Niveaux épistémiques visibles : *établi* / *exploré* / *hypothèse*, signalés par une formule légère et récurrente (ou un encadré) **[à valider : forme]**.
- Chaque partie se termine par « Pour aller plus loin » (3–6 références), tirées de `sources.md`.
- Une idée n'est développée qu'une fois ; ensuite on y renvoie en une phrase.
- Le staccato est réservé aux bascules : il frappe parce qu'il est rare.

## Points forts à protéger (critique V1 et V3)

L'arc qui part du jardin et y revient ; le jardin comme fil ; l'honnêteté épistémique ; des références bien dosées, sans name-dropping ; la bascule vers le « je » à la fin ; le prologue (« Du moins… c'est ce que vous croyez »).

## Questions ouvertes pour l'auteur

1. Nom de la collection et place du titre « Vivons-nous tous dans le même réel ? » sur la couverture.
2. Le vieil homme : a-t-il un nom, une histoire, apparaît-il dans les livres suivants ?
3. ~~Le « nouvel interlocuteur » (IA)~~ → tranché (D6).
4. Encadrés (niveaux, expériences) : oui ou non ?
5. Notes de bas de page ou seulement « Pour aller plus loin » par partie ?
