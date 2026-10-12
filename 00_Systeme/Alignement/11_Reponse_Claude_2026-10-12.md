# Réponse de Claude au message 11 — validation conditionnelle du pilote (2026-10-12)

## 1. Article 2026-566

Conforme : Actualité (`ACTU`, thème MONDE, tags `type-actualite` et `a-la-une`, catégorie `actualites`), regard général, statut `publie`, créée et publiée sur WordPress le 2026-10-12, ligne « Actualité » du 2026-10-12 en mémoire §1. Le journal porte deux lignes `generale` cohérentes (période 2026-10-12, statut final `publie`, note « avant orchestrateur »).

Écart mineur : leur horodatage (15:10) est celui de l'amorçage du journal, pas de la publication.

Conséquence : l'objectif `generale` du 12 octobre est déjà tenu par un article publié hors pilote. Un pilote lancé aujourd'hui ne compterait que curiosité, question et rattrapage (deux articles). **Recommandation : lancer le pilote le 13 octobre**, pour les quatre activités et trois articles.

## 2. Mode brouillons

Analyse : `wp_push_draft` crée toujours en `draft`. La seule mise en ligne automatique est `post_linking.py --publish-final`, que `daily_run` passe sauf avec `--no-publish-final`. Deux autres chemins modifient un article déjà en ligne sans le publier : `wp_refresh_body.py` (« relier en retour », rattrapage) et `daily_run --refresh-body`. `verify_publication --fix` ne publie pas ; seul `--publish-drafts` publie, et il n'est jamais lancé sans demande.

Garde-fou, indépendant de la vigilance de la séance : la sentinelle `00_Systeme/Mode_brouillons.md`. Tant qu'elle existe :
- `post_linking.py --publish-final` est refusé, donc même après le maillage rien n'est publié ;
- `daily_run.py` force `--no-publish-final` et refuse `--refresh-body` ;
- `wp_refresh_body.py` est refusé, sauf `--hors-pilote`, réservé au fondateur ; le « relier en retour » est donc différé et noté dans la trace ;
- le rattrapage dépose sa version révisée dans `07_A_Publier/` sans toucher le canonique ni WP ;
- `phare.py next` affiche « MODE BROUILLONS » ; `routine phare` passe d'elle-même en variante `brouillons seulement`.

Le passage en production consiste à supprimer ce fichier, par le fondateur seul (commit dédié). Aucune routine ne le supprime.

Publication manuelle d'un brouillon :
- `verify_publication.py --publish-drafts <ID>` met l'index à `publie` ;
- depuis l'admin WP, `verify_publication.py <ID> --fix` resynchronise l'index.

Le journal garde le statut `brouillon` décidé par la séance : c'est un fait historique, qui n'est pas réécrit. `phare.py contexte` croise journal et index, et affiche « publié ensuite par le fondateur » ainsi que le rappel du « relier en retour » à faire pour une Question ou une Application.

## 3. Contrôle indépendant

L'autocontrôle et l'agent `relecteur-prepublication` sont obligatoires pour chaque article et chaque rattrapage du pilote. Le relecteur reçoit le chemin du fichier, rien d'autre. Le contrôle porte sur le fond (grille A–D : faits, sources ouvertes, citations, liens, droits humains, risques discriminatoires). La trace de séance sépare « Autocontrôle » et « Relecteur », avec une rubrique « trouvé par le relecteur seul ». Le bilan reprend cette séparation dans un tableau.

## 4. Bilan de pilote

Variante `routine phare — bilan pilote` → `06_Syntheses/Retros/<jour>_bilan_pilote.md`, distinct de la rétro. `next` le signale comme dû tant qu'il manque en mode brouillons. Il s'appuie sur `phare.py contexte bilan_pilote` (statuts, tentatives, durées, publications ultérieures). Ses rubriques couvrent les dix points demandés et se terminent par une recommandation argumentée, sans passage en production.

## 5. Rétro du 19 octobre

Elle est maintenue : `next` la propose le lundi 19 sur 2026-S42. Elle lit les bilans de pilote de la semaine et reprend leurs recommandations dans sa table « Décisions » (retenues, ajournées ou écartées), avec le suivi des premières décisions.

## 6. Commit de référence

Il a été préparé avant le pilote, après vérification des modifications, des fichiers temporaires (aucun hors dépôt, pas de `__pycache__`) et de l'absence de secrets (aucun `*.local.json` suivi). Pas de push.

## 7. Mise en production

Elle n'a lieu qu'après le bilan, une recommandation argumentée et la validation du fondateur, qui supprime lui-même `00_Systeme/Mode_brouillons.md`.
