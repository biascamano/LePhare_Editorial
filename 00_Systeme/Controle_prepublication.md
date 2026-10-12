# Contrôle prépublication — Le Phare Info

Lu **au moment du contrôle seulement** : quotidienne (étape 9, entre `stage` et `daily_run`) et rattrapage (toute réécriture ou note « Depuis »). `plan.md` D20 ; grille issue du cadrage consolidé §3.1–3.5.

**Sur quoi** : le texte rédactionnel final, après `stage` OK. Le maillage ajouté ensuite (`post_linking`, « relier en retour ») est déterministe et couvert par `verify_publication.py`.

## Deux niveaux

- **a. Auto-contrôle** (le rédacteur) : chaque point de la grille, avec sa **preuve** (« vérifié dans [source] », « reformulé », « sans objet : … »). Un point sans preuve compte comme non vérifié.
- **b. Relecture indépendante** (agent `relecteur-prepublication`) : **pilote = tous les articles**. Il reçoit le chemin du fichier final et cette grille, rien d'autre (ni fiche, ni candidats, ni raisonnement du rédacteur), et examine les affirmations une à une contre leurs sources.

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

## Décision

| Décision | Condition | Suite |
|---|---|---|
| **PUBLIER** | a et b sans défaut bloquant | `daily_run` normal |
| **CORRIGER** | Défaut remédiable | Corriger, relancer `stage`, refaire a **puis** b sur le texte corrigé. **2 cycles au plus** |
| **BROUILLON** | Risque important, vérification essentielle non résolue, ou 3ᵉ cycle nécessaire | `daily_run --no-publish-final` ; **la séance s'arrête** (pas d'autre sujet) ; difficulté tracée. Le fondateur publie ensuite avec `verify_publication.py --publish-drafts <ID>` |

**Désaccord a / b** : une réserve de b se traite comme CORRIGER, sauf si le rédacteur la réfute **par la source** (passage cité dans la trace). Toute divergence est tracée : la rétro décidera si la relecture b devient permanente ou ciblée (personnes mises en cause, chiffre central à source unique).

## Trace

Ligne **Contrôle** du bloc de séance (`06_Syntheses/Retros/README.md`) : points relevés par a, par b (codes), divergences, nombre de cycles, corrections importantes, décision.
