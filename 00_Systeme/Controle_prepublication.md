# Contrôle prépublication — Le Phare Info

Lu **au moment du contrôle seulement** : quotidienne (étape 9, entre `stage` et `daily_run`), rattrapage (toute réécriture ou note « Depuis »), Fil du Phare (hebdomadaire A5) et productions de consolidation (mensuelle B6). Rien n'est publié sans décision PUBLIER. `plan.md` D20 ; grille issue du cadrage consolidé §3.1–3.5.

**Sur quoi** : le texte rédactionnel final, après `stage` OK. Le maillage ajouté ensuite (`post_linking`, « relier en retour ») est déterministe et couvert par `verify_publication.py`.

## Deux niveaux

- **a. Auto-contrôle** (le rédacteur) : chaque point de la grille, avec sa **preuve** (« vérifié dans [source] », « reformulé », « sans objet : … »). Un point sans preuve compte comme non vérifié.
- **b. Relecture indépendante** (agent `relecteur-prepublication`) : **pilote = tous les articles**. Il reçoit le chemin du fichier final et cette grille, rien d'autre (ni fiche, ni candidats, ni raisonnement du rédacteur), et examine les affirmations une à une contre leurs sources. Seule exception : au cycle 2, la liste des passages modifiés (voir « Cycles »).

En mode brouillons (`00_Systeme/Mode_brouillons.md`), les deux niveaux restent obligatoires pour chaque article et chaque rattrapage : le fait que rien ne soit publié n'allège pas le contrôle. Une validation de forme ne suffit pas (faits, sources ouvertes, citations, liens, droits humains, risques discriminatoires). La trace et le bilan de pilote séparent ce qu'a trouvé le rédacteur et ce qu'a trouvé le relecteur.

## Grille

**A. Droits humains et dignité**
- A1 Aucune approbation ni banalisation de propos racistes, sexistes, homophobes, transphobes, antisémites, discriminatoires ou déshumanisants. Description, citation critique et analyse se distinguent lisiblement de l'adhésion.
- A2 Aucun stéréotype (origine, sexe, genre, orientation, religion, handicap, âge…).
- A3 Dignité, vie privée, présomption d'innocence : une accusation non jugée est attribuée et formulée comme telle.
- A4 Les personnes concernées sont décrites avec précision ; leurs droits et leur humanité restent visibles.

**B. Faits**
- B1 Chaque affirmation importante (chiffre, date, citation, lien de cause) renvoie à une source réellement consultée ; confirmation indépendante si le fait porte l'article ou s'il est contesté.
- B2 Chiffres, dates, unités, périmètres et bases de comparaison exacts ; faits d'actualité datés ; aucune estimation ancienne présentée comme actuelle.
- B3 Guillemets seulement pour une formulation retrouvée dans la source ; sinon, paraphrase.
- B4 Constat, hypothèse, interprétation et opinion distingués ; corrélation ≠ causalité.
- B5 Point essentiel invérifiable : reformulé, retiré, ou BROUILLON.

**C. Sources, liens, propriété**
- C1 Chaque lien des « Repères de sources » est ouvert : accessible, bon destinataire, date, et il soutient bien l'affirmation (une page qui répond ne suffit pas).
- C2 Source inaccessible (paywall, 403, JavaScript) : confirmée par une deuxième source accessible ; sinon « selon [source], non consultée intégralement » ; si elle porte l'article : BROUILLON.
- C3 Liens internes lus dans l'index ou le manifeste ; aucun lien vers un brouillon ni vers `wiki-du-phare`.
- C4 Citations courtes et attribuées. Aucune image dans le corps : l'image à la une vient de la médiathèque par tag, dont le fondateur vérifie les licences une fois pour toutes.
- C5 Aucun lien trompeur, aucune redirection douteuse, aucune référence insuffisante.

**D. Intégrité éditoriale**
- D1 Question utile et distincte des contenus existants (état courant ; `index_lookup.py --search`).
- D2 Titre précis, non sensationnaliste, fidèle au contenu.
- D3 Contre-arguments sérieux présents, sans fausse équivalence entre preuves inégales.
- D4 Penseurs et concepts utilisés comme outils d'examen, jamais comme argument d'autorité ; aucun dans une Actualité.
- D5 La conclusion sépare acquis, limites et question ouverte.
- D6 SEO, catégorie, type, extrait et navigation corrects (`stage` OK).

## Gravité des défauts (bilan de pilote du 2026-10-13)

Chaque défaut relevé, par a ou par b, est classé :
- **Bloquant** : fait faux OU fait contredit par sa source OU affirmation contestée présentée comme établie OU citation déformée (sens changé) OU fait qui porte l'article non confirmé OU point A en défaut.
- **Mineur** : tout le reste, notamment attribution imprécise (citation qui déborde des guillemets, structure prêtée à une source), datation à préciser, source à ajouter dans les Repères pour un fait juste, formulation de titre ou de meta.

## Cycles

- **Cycle 1 exhaustif.** L'auto-contrôle a dresse le **tableau des citations et attributions** (chaque phrase entre guillemets ET chaque « selon… » face au passage de la source) ; les Repères sont complets dès la V1 : un fait repris d'un article interne garde au moins une source externe. Le relecteur b vérifie **toutes** les affirmations attribuées, chiffrées ou datées, pas un échantillon.
- **Ajouts en corrigeant.** Toute phrase ajoutée ou réécrite pendant une correction est vérifiée à sa source par a avant de relancer b. Une correction n'ajoute pas de fait nouveau sans nécessité.
- **Cycle 2 ciblé.** b reçoit le chemin du fichier **et** la liste des passages modifiés (citations exactes du nouveau texte, sans motif ni raisonnement). Il vérifie ces passages et seulement eux, sauf défaut bloquant aperçu ailleurs.

## Décision

| Décision | Condition | Suite |
|---|---|---|
| **PUBLIER** | a et b sans défaut bloquant, défauts mineurs corrigés | `daily_run` normal. Les mineurs corrigés après le dernier passage de b sont listés dans la trace (passage, correction, source) |
| **CORRIGER** | Au moins un défaut bloquant remédiable | Corriger, relancer `stage`, auto-contrôle des passages modifiés, puis b ciblé. **2 relectures b au plus** |
| **BROUILLON** | Risque important (personne mise en cause, droits humains, discrimination) OU vérification essentielle non résolue (fait porteur introuvable à la source) | `daily_run --no-publish-final` ; **la séance s'arrête** (pas d'autre sujet) ; difficulté tracée ; orchestrateur : `close … --statut brouillon --note "<motif>"`. Le fondateur publie ensuite avec `verify_publication.py --publish-drafts <ID>` |

**Après le cycle 2, on publie** (décision du fondateur, 2026-10-13) : jamais de 3e relecture. Les défauts relevés au cycle 2, bloquants ET mineurs, sont corrigés par le rédacteur, chaque correction vérifiée à la source ; un passage qui ne peut pas être sourcé est retiré. Puis décision **PUBLIER**, corrections listées dans la trace. Seuls les cas de la ligne BROUILLON empêchent la publication.

Des défauts seulement mineurs ne déclenchent ni nouveau cycle ni BROUILLON : ils sont corrigés et tracés.

**Désaccord a / b** : une réserve de b se traite comme CORRIGER, sauf si le rédacteur la réfute **par la source** (passage cité dans la trace). Toute divergence est tracée : la rétro décidera si la relecture b devient permanente ou ciblée (personnes mises en cause, chiffre central à source unique).

## Trace

Ligne **Contrôle** du bloc de séance (`06_Syntheses/Retros/README.md`) : points relevés par a, par b (codes, avec **B** pour bloquant et **m** pour mineur, ex. `B2/m`), divergences, nombre de cycles, corrections importantes, défauts introduits par une correction, décision.
