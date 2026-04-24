# Protocole manuel - Publication WordPress (Le Phare)

## Objectif

Publier les articles de facon fiable sans automatisation, tout en gardant l'index editorial synchronise.

## Regle de decision : quand publier ?

Publier un article uniquement quand les 5 conditions suivantes sont vraies :

1. Contenu relu et valide editorialement.
2. Sources citees et datees dans le brouillon.
3. Liens internes du dossier poses (2 a 4).
4. SEO minimal renseigne (mot-cle + meta-description).
5. Statut du fichier source = `pret_a_publier`.

Si une condition manque : garder le statut `en_cours`.

## Workflow pas a pas

0. Prendre l'article dans `07_A_Publier/...` (file de publication).
1. Ouvrir le fichier source dans l'arborescence editoriale.
2. Copier le contenu vers l'editeur WordPress.
3. Definir :
   - Titre
   - Slug
   - Categorie
   - Tags
   - Meta description
4. Verifier liens internes et externes.
5. Mettre l'image de tete (1792x1024, jpg).
6. Previsualiser en desktop + mobile.
7. Publier.
8. Supprimer le fichier correspondant de `07_A_Publier/...`.

## Mise a jour obligatoire apres publication

Dans `index_editorial.csv`, renseigner pour l'article :

- `Statut` -> `publie`
- `Date_publication_WP`
- `URL_WordPress`
- `Slug_WordPress` (si ajuste)
- `Date_derniere_maj`

Optionnel mais recommande :
- `Remarques` (ex. corrections de derniere minute)

## Logique du repertoire `07_A_Publier`

- Ce repertoire sert de file d'attente visuelle.
- Si le fichier est present : article non encore publie.
- Si le fichier est supprime : article publie (et index deja mis a jour).

## Ordre recommande pour le dossier Inflation Europe

1. 2026-419 (porte d'entree)
2. 2026-420 (cle de comprehension)
3. 2026-422 (biais et perceptions)
4. 2026-421 (analyse approfondie)
5. 2026-423 (concept cle)
6. 2026-424 (texte fondateur)
7. 2026-425 (perspective historique)
8. 2026-426 (sentier)
9. 2026-427 (questions ouvertes)
10. 2026-428 (explorer plus loin)

## Controle final hebdomadaire

Une fois par semaine :
- verifier que tous les articles publies ont une URL dans l'index,
- verifier qu'aucun article `pret_a_publier` n'est oublie,
- verifier que les liens internes renvoient vers des URLs actives.
