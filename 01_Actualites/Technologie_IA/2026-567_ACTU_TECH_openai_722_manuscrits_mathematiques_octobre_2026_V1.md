ID article : 2026-567
Titre : OpenAI publie 722 démonstrations mathématiques, en retire trois le lendemain : qui dit qu'une preuve est vraie ?
Type : ACTU
Type article : Actualite
Theme : TECH
Statut : brouillon
Version : V1
Date de creation : 2026-10-12
Date de derniere mise a jour : 2026-10-12
Auteur : Le Phare Info
Etape du Sentier liee :
Fondamental lie (ID) :
Fondamental numero :
Type Sentier :
Posture Sentier : Observer
Articles lies (IDs) : 2026-565;2026-558;2026-561
Question du Phare : Quand une machine produit plus de démonstrations que les mathématiciens ne peuvent en lire, qu'est-ce qui fait qu'un résultat devient un savoir ?
Dossier :
Article precedent (ID) :
Prolongement envisage : Bilan des vérifications indépendantes des manuscrits non formalisés ; publication ou non du modèle et des conditions de calcul
Mots-cles : OpenAI mathématiques;démonstration IA;Lean formalisation;vérification preuve;Retraction Watch
Resume court (500 caracteres max) : Le 6 octobre 2026, OpenAI a déposé 722 manuscrits mathématiques produits par un modèle interne ; trois ont été retirés le lendemain pour une erreur de signe. Ce que l'on sait, ce qui reste à vérifier.
Objectif de l'article : Établir les faits de la publication massive d'OpenAI et poser la question de ce qui transforme un résultat en savoir établi.
Sources principales : Retraction Watch (8 octobre 2026) ; Scientific American (6 octobre 2026) ; dépôt GitHub openai/math
URL WordPress (si publie) :

---

# OpenAI publie 722 démonstrations mathématiques, en retire trois le lendemain : qui dit qu'une preuve est vraie ?

Le 6 octobre 2026, à 18 heures (heure de l'Est américain, selon Scientific American), OpenAI a déposé dans un dépôt public de la plateforme GitHub 722 manuscrits de mathématiques. Tous ont été produits par un modèle interne que l'entreprise ne rend pas public. Selon Retraction Watch, ces textes revendiquent des avancées sur 372 problèmes, en géométrie, en algèbre, en informatique théorique et dans d'autres domaines. Le lendemain, 7 octobre, OpenAI retirait trois de ces manuscrits. L'épisode est bref, mais il pose une question que les mathématiques avaient rarement eu à se poser à cette échelle : que faire de résultats produits plus vite qu'on ne peut les lire ?

## Ce qui a été publié

Le dépôt, intitulé `openai/math`, présente aujourd'hui un catalogue de 719 manuscrits regroupés en 372 « familles ». D'après sa page de présentation, le modèle s'est vu soumettre environ 4 000 problèmes au cours de l'évaluation ; seuls les résultats jugés suffisamment significatifs ont été retenus. Parmi les résultats annoncés, Scientific American cite une solution de la conjecture de Kakeya en dimension quatre, des améliorations d'algorithmes importants et des avancées en direction de l'hypothèse de Riemann. Selon un porte-parole d'OpenAI cité par le magazine, presque tous ces résultats proviennent d'une seule consigne donnée à un seul agent d'IA, certains ayant pu demander plusieurs tentatives.

Ces affirmations ne sont pas toutes au même niveau. La page du dépôt indique qu'environ 42 % des résultats principaux sont accompagnés d'une formalisation en Lean, un langage informatique qui vérifie mécaniquement chaque étape d'une démonstration. Elle avertit aussi que certains des résultats non formalisés « pourraient comporter des problèmes ». Un porte-parole d'OpenAI a reconnu auprès de Retraction Watch qu'environ la moitié des résultats avaient été publiés sans confirmation.

## L'erreur de signe et les trois retraits

Le 7 octobre, OpenAI a annoncé le retrait de trois manuscrits à cause d'une erreur de signe. Selon l'annonce rapportée par Retraction Watch, cette erreur invalidait un argument dans un premier manuscrit, et la construction que deux autres textes empruntaient à celui-ci. L'entreprise dit avoir repéré ces erreurs lors d'un audit interne. Elle a en outre révisé quatorze autres manuscrits : réparations de preuves, énoncés corrigés, hypothèses et dépendances clarifiées, et une référence obsolète remplacée.

Le dépôt précise que les corrections sont enregistrées comme de nouvelles versions, les précédentes restant accessibles. Un porte-parole d'OpenAI a déclaré à Retraction Watch que l'entreprise accueillait les critiques de la communauté mathématique et s'engageait à corriger les erreurs identifiées, ou à retirer les textes qu'on ne pourra pas réparer.

L'enchaînement montre une chose simple : dans une démonstration, une erreur locale peut se propager. Un résultat n'est pas une pièce isolée ; d'autres s'appuient sur lui. Quand des centaines de textes sont publiés en même temps, une seule faille peut en entraîner plusieurs, et il faut quelqu'un pour la trouver.

## Ce que la vérification par machine garantit, et ce qu'elle ne garantit pas

La formalisation en Lean apporte une garantie forte : un résultat qui y est vérifié est considéré comme quasi certain sur le plan de la logique. Mais, souligne Scientific American, il revient encore aux mathématiciens de juger si ces preuves contiennent des idées nouvelles et importantes, et il leur faudra des mois pour le faire. Une formalisation suppose d'ailleurs que l'énoncé formel corresponde bien à la question posée en langage mathématique ordinaire, ce qu'un expert doit encore vérifier.

Il y a donc au moins trois étages : la preuve est-elle correcte, le résultat est-il celui qu'on annonce, et apporte-t-il quelque chose ? La machine peut répondre au premier, pour environ 42 % des résultats principaux selon le dépôt. Les deux autres restent l'affaire de lecteurs humains.

## Des réactions partagées

La publication intervient dans un climat déjà tendu. Retraction Watch rappelle l'annonce par OpenAI, le 8 septembre, d'une résolution du problème de Navier-Stokes par un système d'IA, et les critiques qui ont suivi : plus de 8 000 chercheurs ont soutenu une prise de position critique sur la manière dont elle avait été faite. Le 21 septembre, selon Scientific American, OpenAI a annoncé la création d'un groupe consultatif indépendant de mathématiciens sur la publication de résultats produits par IA. Selon le magazine, ce groupe recommande aux entreprises de publier le modèle, les consignes exactes et le temps de calcul de chaque résultat ; OpenAI dit ne vouloir divulguer que le temps de calcul moyen et quelques statistiques, sans les consignes.

Les avis divergent. Une association de mathématiciens, l'Association for Human Mathematics, a jugé le 7 octobre que publier plus de 700 fichiers d'un coup relevait d'une démonstration de puissance plutôt que d'un travail savant. Alex Townsend, de l'université Cornell, estime qu'OpenAI aurait dû annoncer d'abord les manuscrits vérifiés en Lean, puis demander de l'aide pour les autres. Andrew Sutherland, du MIT, demandait dès le 6 octobre, dans Scientific American, de tenir pour non vérifiées les affirmations sur des solutions obtenues en une seule fois, tant que le modèle ne serait pas publié et les résultats reproduits ; après les retraits, il a jugé auprès de Retraction Watch que la réaction rapide d'OpenAI était responsable. Daniel Litt, de l'université de Toronto, voit au contraire dans cette publication une bonne chose pour les mathématiques, et ne voit pas de raison de demander à l'entreprise de garder ces résultats secrets.

## Ce qui reste incertain

Plusieurs points ne sont pas établis à ce jour. On ignore combien des résultats non formalisés résisteront à la lecture des spécialistes. On ne sait pas non plus quelle part des 372 familles constitue une avancée réelle, ni ce que les annonces les plus spectaculaires valent une fois examinées en détail. Faute d'accès au modèle et aux consignes, personne en dehors d'OpenAI ne peut reproduire la manière dont ces textes ont été obtenus. Enfin, les chiffres circulant dans la presse varient selon ce qu'ils comptent : manuscrits, problèmes, résultats principaux ou formalisations.

## Quand la production dépasse la lecture

En mathématiques, un résultat devient un savoir à l'issue d'un long processus : des spécialistes lisent la preuve, la discutent, la reprennent, l'enseignent, s'en servent pour aller plus loin. Ce processus suppose un rythme humain. La publication d'OpenAI ne remet pas en cause la vérité d'une démonstration correcte, mais elle dissocie deux choses qui allaient jusqu'ici ensemble : produire un résultat et le faire reconnaître. La vérification par machine couvre une partie du chemin, pas sa totalité. Reste à savoir qui, et à quel rythme, accomplira le reste.

---

**Repères de sources**

- Source : [Retraction Watch, « OpenAI withdraws three preprints a day after releasing 722 manuscripts on unsolved math problems » (8 octobre 2026)](https://retractionwatch.com/2026/10/08/openai-withdraws-preprints-722-manuscripts-unsolved-math-problems/)
- Source : [Scientific American, « OpenAI unleashes hundreds more math results upon a field already in shock » (6 octobre 2026)](https://www.scientificamerican.com/article/openai-unleashes-hundreds-more-math-results-upon-a-field-already-in-shock/)
- Source : [OpenAI, dépôt GitHub openai/math (page de présentation)](https://github.com/openai/math)

**La question suivante**

Quand une machine produit plus de démonstrations que les mathématiciens ne peuvent en lire, qu'est-ce qui fait qu'un résultat devient un savoir ?

**Pour aller plus loin**

- [Influence : OpenAI dit avoir démasqué des campagnes russe et iranienne, et reste seule à le vérifier](https://le-phare.info/openai-operations-influence-russie-iran-octobre-2026/)
- [Combien de temps faut-il chercher avant d'admettre qu'on ne trouvera pas ?](https://le-phare.info/question-du-phare-chercher-avant-admettre-echec/)
- [Comment informer sur un accident de laboratoire quand le diagnostic n'est pas confirmé ?](https://le-phare.info/question-du-phare-informer-accident-laboratoire-diagnostic/)

**Sur le Sentier du Savoir**

- [La falsifiabilité selon Popper](https://le-phare.info/la-falsifiabilite-selon-popper/)

# SEO

Mot-cle principal : OpenAI mathématiques
Meta description : OpenAI a publié 722 manuscrits mathématiques produits par IA, puis en a retiré trois. Ce qui est vérifié, ce qui ne l'est pas, et ce que cela change.
Slug propose : openai-722-manuscrits-mathematiques-octobre-2026
