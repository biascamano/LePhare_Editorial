---
name: routine-renovation
description: Routine de rénovation Le Phare — remettre l'ancien stock (ères triptyque et import) au format actuel, lot par lot, sans changer ni ID, ni URL, ni slug : trier (décisions humaines), remettre à niveau la navigation, refaire les articles les plus reliés. Déclenché par « routine renovation » ou /routine-renovation.
---

# Routine de rénovation — le stock ancien

**Question de la session : « Quel ancien article mérite le plus d'être remis au niveau du Phare actuel ? »**

Référence : `plan.md` D17 et §19. La rénovation ne publie **rien de nouveau** : même ID, même URL, même slug. Elle ne touche ni la mémoire §1, ni le Radar, ni `Etat_editorial_courant.md`. La quotidienne ne rénove pas, et la rénovation ne produit pas l'article du jour.

Autonomie : lots 2 et 3 jusqu'au rapport, sans confirmation intermédiaire. **Lot 1 : décisions humaines**. Proposer et attendre la réponse avant toute suppression, dépublication ou retrait de ligne d'index.

## Variantes du prompt

- `routine renovation` : lot ouvert le plus bas (étape 2).
- `routine renovation — lot 2` / `lot 3` : lot imposé.
- `routine renovation — <ID> [<ID> …]` : articles imposés (le niveau de l'inventaire décide du traitement).
- `routine renovation — à blanc` : inventaire et proposition seulement, aucune écriture.

## 1. Régénérer l'inventaire

```bash
python tools/build_inventaire_renovation.py
```
Lire `00_Systeme/Inventaire_renovation.md`, en commençant par l'en-tête (compteurs par niveau), puis seulement la section du lot traité. Colonnes utiles : score, liens entrants, marqueur « copie locale tronquée », action proposée.

## 2. Choisir le lot

Lot 1 jusqu'à épuisement. Ensuite, alterner d'une session à l'autre : lot 2 (5 à 10 articles), puis lot 3 (1 à 3 articles). Pour savoir quel lot a été traité en dernier, regarder la colonne `Remarques` de l'index (`Rénové (Routine rénovation) …`) ou le dernier commit de rénovation. Dans un lot, prendre les articles par score décroissant.

## 3. Garde-fous (lot 0, à chaque article)

- `02_Fonds/` : **jamais** (ni pull, ni refresh). Les scripts le refusent d'eux-mêmes ; ne pas les forcer (`--allow-fonds` interdit).
- Copie « tronquée » (ou dès que WP compte nettement plus de mots que le local) : resynchroniser **d'abord** :
  ```bash
  python tools/wp_pull_body.py <ID>            # à blanc : local / WP / retour / pertes
  python tools/wp_pull_body.py <ID> --apply
  ```
  Si `retour` s'écarte de `WP` de plus de quelques mots, ou si des images, iframes ou tableaux sont signalés, **ne pas appliquer**. Noter l'article dans le rapport, et le traiter à la main ou le laisser de côté. Les italiques perdus sont acceptés : les remettre en `**gras**` seulement s'ils portent du sens (titres d'œuvres → guillemets « »).
- Ne jamais lancer `wp_refresh_body.py` sur une copie non resynchronisée : cela écraserait la version en ligne, qui est la plus complète.

## 4. Traiter

### Lot 1 — Trier (décisions humaines)

Présenter les sous-lots de `plan.md` §19.3 sous forme de tableau court (IDs, constat, proposition), puis demander la décision (AskUserQuestion, une question par sous-lot). Exécuter ensuite uniquement ce qui est décidé :
- Lignes d'index en double : retirer la ligne via `index_editorial_utils` (`read_index` puis `write_index`, jamais `csv.writer`). Supprimer le fichier seulement s'il est identique au jumeau ou s'il n'est référencé nulle part (`grep` de l'ID et du nom de fichier). Puis `python tools/validate_index_editorial.py`.
- Brouillons jamais publiés : archiver ou supprimer selon la décision. Un DOSSIER à publier passe au lot 3 (réécriture avant publication).
- Doublons de titre : la fusion se fait dans l'article le mieux relié (lot 3). Une dépublication sur WP = action publique : la décrire et attendre l'accord explicite.
- Pages rubriques : retirer le tag `a-la-une` seulement après accord.

### Lot 2 — Remettre à niveau (sans réécriture)

Pour chaque article :
1. Resynchroniser si nécessaire (étape 3).
2. Navigation v3 (`plan.md` §5.4) à la place de « Dans ce triptyque » ou de la navigation ancienne :
   ```markdown
   ---

   **Repères de sources**

   - Source : [libellé](url)

   **La question suivante**

   [une phrase, rédigée à partir de l'article]

   **Pour aller plus loin**

   - [Titre](url)

   **Sur le Sentier du Savoir**

   - [Titre du fondamental](url_canonique)
   ```
   Liens internes : uniquement des URLs lues via `python tools/index_lookup.py <IDs>` ou `--search "<mot>"`, et pour le Sentier via `00_Systeme/Manifests/sentier_fondamentaux.csv` (jamais `wiki-du-phare`). Les sources nues deviennent `[libellé](url)`.
3. Liens `?p=` : remplacer par l'URL de l'index, sinon retirer le lien (le texte reste).
4. Titre : retirer l'emoji de `Titre :` dans l'en-tête, puis refresh avec `--title`. Pas de préfixe D16 rétroactif.
5. Refresh :
   ```bash
   python tools/wp_refresh_body.py "<chemin canonique>" [--title]
   ```

### Lot 3 — Refaire (réécriture)

1–3 articles, par score décroissant. Pour chaque article :
1. Resynchroniser (étape 3) : la version WP est la base de travail.
2. Choisir le type actuel qui correspond (Actualité / Question / Application / TF ; un SENTIER devient l'atelier d'un fondamental existant). Rédiger soi-même, selon `00_Systeme/Instructions_editoriales_officielles.md` et le socle, comme dans la routine quotidienne étape 7 (gabarits et longueurs).
3. Faits anciens : les garder **datés** et ne pas les présenter comme actuels. Si la suite est connue et vérifiable, ajouter une courte section « Depuis » sourcée (veille web) ; sinon, ne rien ajouter.
4. Conserver **ID, URL et slug** : ne pas changer `Slug propose`, ni le nom de fichier, ni `Slug_WordPress` / `URL_WordPress` dans l'index. Compléter l'en-tête au format v3 (Question du Phare, Type, Sentier…), navigation v3 (lot 2, point 2) et bloc `# SEO` final (mot-clé, meta description, `Slug propose` inchangé).
5. Index : `Remarques` = `Rénové (Routine rénovation) YYYY-MM-DD`, via `index_editorial_utils` ; les autres colonnes v3 sont complétées si elles sont vides. Puis `python tools/validate_index_editorial.py --ids <ID>`.
6. Refresh : `python tools/wp_refresh_body.py "<chemin canonique>" --title`.
7. Liens entrants : les articles actuels qui citaient l'ancien gardent la même URL, il n'y a rien à faire.

## 5. Vérifier

```bash
python tools/verify_publication.py <IDs traités>
```
En cas d'erreur sur le tag ou sur un lien `?p=` : `--fix`. Toute autre erreur : la signaler, sans forcer.

## 6. Clore

1. `python tools/build_inventaire_renovation.py` : compteurs après la session.
2. Mémoire : rien en §1. La mensuelle condense les sessions de rénovation en §5, d'après les `Remarques` de l'index.
3. Pas de commit sans demande de l'utilisateur.

## Rapport final

```
Routine rénovation — [date] — lot N
Traités : ID titre (action : resync / nav / titre / réécrit) — URL
Écartés : ID (raison : pertes au pull, écart retour, décision attendue…)
Décisions lot 1 : … (ou sans objet)
verify_publication : OK / erreurs
Inventaire : Trier X · Remettre à niveau Y · Refaire Z (avant → après)
Prochaine session : lot …, IDs …
À vérifier : WordPress (articles traités)
```

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `cd … &&`, `;`, `|`, ni `python -c` multiligne. Read / Grep / Edit plutôt que `cat` / `grep` / `sed`. Ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande, ni lire ces fichiers.

## Ne pas faire

- Toucher `02_Fonds/`, ou utiliser `--allow-fonds`.
- Refresh WP d'une copie tronquée non resynchronisée.
- Changer un ID, un slug, une URL ou un nom de fichier.
- Supprimer, dépublier ou retirer une ligne d'index sans décision humaine (lot 1).
- « Actualiser » un fait ancien sans source, ou inventer une URL interne.
- Ajouter une ligne en mémoire §1, toucher le Radar ou publier un nouvel article.
