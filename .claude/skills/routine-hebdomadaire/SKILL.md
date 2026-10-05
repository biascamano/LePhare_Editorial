---
name: routine-hebdomadaire
description: Routine hebdomadaire Le Phare — relire les articles de la semaine, dégager le fil rouge, publier « Le Fil du Phare » (catégorie cycle), auditer les fils éditoriaux et préparer la semaine suivante dans la mémoire éditoriale. Déclenché par « routine hebdomadaire », « fil du phare » ou /routine-hebdomadaire.
---

# Routine hebdomadaire — Le Fil du Phare

**Question de la semaine : « Qu'est-ce que nos articles racontent ensemble ? »**

L'hebdomadaire crée les connexions. Il ne cherche pas de nouveaux sujets d'actualité et ne restructure ni dossiers ni Sentier (→ mensuelle).

Autonomie totale, comme la quotidienne : pas de confirmation intermédiaire. Variante `brouillons seulement` → `--no-publish-final`.

## 1. Relire les publications de la semaine

`00_Systeme/Memoire_editoriale.md` §1 : lignes des 7 derniers jours (+ §2, §4). Pour chaque article (fichier canonique via `index_editorial.csv`) : sujet, type, Question du Phare, concepts, dossier, Sentier, penseurs. Si moins de 3 articles dans la semaine : ne pas publier de Fil du Phare, faire seulement les étapes 5 à 7.

## 2. Chercher les connexions

Questions récurrentes, tensions communes, événements différents qui parlent du même phénomène, contradictions, thèmes émergents.

## 3. Formuler UNE grande question

Une seule question qui résume la semaine (ex. « Sommes-nous devenus plus libres ou simplement plus dépendants ? »).

## 4. Rédiger Le Fil du Phare

Titre : `Le Fil du Phare — [question]`. ~900–1400 mots. Sections :

- **Cette semaine** — présentation très courte des événements (liens vers chaque article).
- **Le lien invisible** — ce qu'ils ont en commun.
- **La grande question** — développement.
- **Un penseur pour regarder autrement** — uniquement si pertinent, pas un cours de philosophie.
- **Ce que ces événements nous apprennent** — relier les domaines.
- **Ce que nous ne savons pas encore** — limites, questions ouvertes.
- **Où poursuivre ?** — dossier, textes fondateurs, Sentier (URLs réelles de l'index / `sentier_fondamentaux.csv`).

Métadonnées :
```bash
python tools/new_article.py create --type fil-du-phare --theme <THEME dominant> --title "…" --slug <kebab-case> --question "…" --linked "<IDs de la semaine>" --keywords "…" --summary "…" --objective "…" --tags "<concept>;…"
```
Le script calcule ID, fichier `06_Syntheses/Fil_du_Phare/`, type `SYNTHESE`, catégorie `cycle`, tags `fil-du-phare`/`question-du-phare`/`synthese-hebdomadaire`, slug `fil-du-phare-<slug>` et la ligne d'index. Rédiger le corps dans le `path` renvoyé, compléter navigation et `# SEO`. Sources en `[libellé](url)`.

Puis `python tools/new_article.py stage <ID>`. `stage` lance le contrôle v3 (`validate_index_editorial.py --ids`) : s'il est KO, corriger le fichier ou la ligne d'index et relancer — jamais `--force` en routine. Ensuite :
```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder --force
```
(`--force` car `daily_run` refuse un second run réussi le même jour.)

## 5. Auditer les fils éditoriaux

Mettre à jour §2 de la mémoire :
- **à poursuivre** — questions assez riches pour d'autres articles (+ prochaine piste) ;
- **à clôturer** — suffisamment traitées ;
- **à mettre de côté** — intéressantes mais il manque de l'actualité ou de la connaissance (+ condition de reprise).

## 6. Préparer la semaine suivante

3 à 5 pistes : articles à poursuivre, nouveaux domaines où tester les mêmes questions, textes fondateurs éventuellement nécessaires. Ne **pas** fixer un programme de sept articles : l'actualité doit pouvoir le modifier.

Reporter les pistes durables dans `00_Systeme/Articles_a_creer.md` (§1 suivis datés, §2 questions en attente ; P1 réservé aux échéances fixes, sinon P2/P3) et retirer les entrées réalisées dans la semaine. Ne pas toucher aux §3–§5 de ce fichier (textes fondateurs, dossiers, Sentier → mensuelle).

## 7. Mettre à jour la mémoire éditoriale

- §1 : ajouter la ligne du Fil du Phare (type `Fil du Phare`).
- §2 : fils (étape 5).
- §3 : nouvelle ligne **en haut** — semaine, grande question, ID Fil du Phare, concepts apparus, dossiers renforcés, pistes.

Optionnel (si l'utilisateur le demande) : rétro de la routine via `00_Systeme/Retro_routine_hebdo_TEMPLATE.md`.

## Rapport final

```
Routine hebdomadaire — semaine du … au …
Fil du Phare : [question] — URL
Articles reliés : N (IDs)
Fils : +X actifs / Y clôturés / Z de côté
Pistes semaine suivante : …
```

## Ne pas faire

- Chercher le sujet d'actualité du jour.
- Créer/réorganiser un dossier, un texte fondateur ou un atelier Sentier (→ mensuelle).
- Résumé chronologique sans lien invisible.
