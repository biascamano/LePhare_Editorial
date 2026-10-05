---
name: routine-quotidienne
description: Routine quotidienne Le Phare — UN article à partir de l'actualité du jour, qui poursuit les fils ouverts et se termine par une Question du Phare ; publication WordPress puis mise à jour de la mémoire éditoriale. Déclenché par « routine quotidienne » ou /routine-quotidienne. (L'ancien triptyque ACTU+TF+SENTIER = /routine-triptyque.)
---

# Routine quotidienne — Le Phare Info

**Question du jour : « Qu'est-ce qu'on publie aujourd'hui et quelle question cela ouvre ? »**

Le quotidien produit les briques. Il ne fait PAS : restructuration des dossiers, synthèse de la semaine, architecture du Sentier, analyse du mois, création systématique de texte fondateur ou d'atelier Sentier → routines hebdomadaire / mensuelle.

## Variantes du prompt

- **Sujet imposé** (`routine quotidienne — sujet : …, thème TECH`) : respecter sujet/angle/thème.
- **Brouillons seulement** : `--no-publish-final`.
- **Type imposé** (`… type question` / `application` / `texte fondateur`) : respecter.

Autonomie totale : pas de validation du sujet, pas de confirmation intermédiaire, exécution jusqu'au rapport final.

## 1. Lire la mémoire éditoriale

`00_Systeme/Memoire_editoriale.md` : §1 (15 dernières lignes), §2 fils actifs, §3 dernier Fil du Phare, §4 cap du mois. Identifier sujets récents, Questions du Phare ouvertes, dossiers actifs, penseurs récents, étapes du Sentier sollicitées, prolongements envisagés. Ne pas répéter un sujet sans raison.

L'ID est attribué à l'étape 8 par `tools/new_article.py` (ne pas le calculer à la main).

## 2. Analyser l'actualité (24–72 h)

Veille web (presse sérieuse, sources institutionnelles). Retenir 5 à 10 sujets ayant des conséquences réelles, compréhensibles au-delà de l'événement, ou prolongeant une question / un dossier existant, ou faisant émerger une question durable. Écarter buzz, polémique sans conséquence, fait divers isolé, sensationnel.

## 3. Choisir UN sujet

Critères : importance, durabilité, intérêt intellectuel, originalité, connexion avec les publications précédentes, potentiel de Question du Phare. Tenir compte des catégories sous-représentées (§4 de la mémoire) sans forcer.

## 4. Déterminer le type

| Type | Question principale | Code index | Dossier canonique | Categorie_WP |
|------|---------------------|------------|-------------------|--------------|
| **A. Actualité** | Que vient-il de se passer et pourquoi est-ce important ? | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **B. Question du Phare** | Qu'est-ce que cet événement révèle de plus fondamental ? (prolonge une question ouverte) | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **C. Application** | Une question déjà étudiée, vue sur un autre terrain | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **D. Penseur / texte fondateur** | Seulement si un concept devient nécessaire pour comprendre les articles précédents — jamais artificiel | `TF` | `04_Textes_fondateurs/Auteurs/` | `textes-fondateurs` |

Tag de type obligatoire : `type-actualite` | `type-question` | `type-application` | `type-texte-fondateur`, + `question-du-phare`.

## 5. Fiche de préparation (interne, non publiée)

Sujet / titre provisoire · Pourquoi aujourd'hui (2–4 phrases) · Faits essentiels (5–10) · Type · **Question du Phare (une seule)** · Connexion précédente (quel article y mène) · Dossier existant éventuel · Penseur/concept (si pertinent) · Sentier (étape ou fondamental, via `00_Systeme/Manifests/sentier_fondamentaux.csv`, jamais `wiki-du-phare`) · Prolongement possible.

## 6. Rédiger

Qualité cible : `00_Systeme/Instructions_editoriales_officielles.md` (slow journalism, §3.0 titres adaptés au sujet, §3.8 si institutionnel, gras parcimonieux). Rédiger soi-même (pas d'API / Ollama). ~800–1300 mots. L'article doit pouvoir être lu seul.

Structure indicative (intertitres **adaptés au sujet**, pas cette grille littérale) : chapô · ce qui s'est passé / la question posée · ce que l'on sait · pourquoi cela compte · ce que cela révèle · une autre manière de regarder · ce que nous pouvons en retenir · la question laissée ouverte.

Micro-édition + calibrage automatiques.

## 7. Navigation finale (avant `# SEO`)

```markdown
---

**Repères de sources**

- Source : [libellé](url)

**La question suivante**

[Question du Phare, une phrase]

**Pour aller plus loin**

- [Titre article précédent ou dossier](url)

**Sur le Sentier du Savoir**

- [Titre du fondamental](url_canonique)
```

Liens Markdown obligatoires (pas d'URL nue). Liens internes : uniquement des URLs réelles lues dans `index_editorial.csv` / `sentier_fondamentaux.csv`. Pas de section `Dans ce triptyque`.

## 8. Fichier, index, WordPress

Créer l'article **avant** de rédiger le corps (ID, dossier, nom de fichier, catégorie, tags et ligne d'index sont calculés par le script) :
```bash
python tools/new_article.py create --type <actualite|question|application|texte-fondateur> --theme <THEME> --title "…" --slug <kebab-case> --pillar <pilier> --question "…" --previous <ID> --linked "<ID>;…" --prolongement "…" --keywords "…;…" --summary "…" --objective "…" --tags "<concept>;<concept>" [--dossier "<ID de la page principale ou nom du sous-dossier>"] [--routine quotidienne]
```
(`--routine quotidienne` obligatoire pour un texte fondateur.) Le script renvoie `id` et `path` : écrire le corps à la place de `[Corps de l'article à rédiger]`, compléter la navigation finale, `Sources principales` et le bloc `# SEO` (meta description). En-tête (`00_Systeme/Modele_Entete_Article.md`) déjà rempli, dont :

```
Type article : Actualité | Question | Application | Texte fondateur
Question du Phare : …
Dossier : … (ou vide)
Article precedent (ID) : YYYY-NNN
Prolongement envisage : …
```

`Articles lies (IDs)` = article précédent (+ éventuels). Bloc `# SEO` : mot-clé, meta description, `Slug propose`. Une fois l'article rédigé : `python tools/new_article.py stage <ID>` (copie dans `07_A_Publier/<date>_<slug>/`). `stage` lance le contrôle v3 (`validate_index_editorial.py --ids`) : s'il est KO, corriger le fichier ou la ligne d'index et relancer — jamais `--force` en routine. Ne jamais écrire l'index à la main ni via `csv.writer`.

Publication :
```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder
```
(`post_linking.py` accepte un dossier à article unique : il publie sans injecter de bloc triptyque.) Extraire seulement `status`, `error`, `wordpress_id`, `link` des sorties JSON.

Fournir dans le rapport : idée d'image, légende, texte alternatif (pas de génération d'image).

## 9. Mettre à jour la mémoire éditoriale

Ajouter **une ligne** à la fin du tableau §1 de `00_Systeme/Memoire_editoriale.md` : date, ID, `[titre](url WP)`, type, catégorie/thème, Question du Phare, dossier, penseur, Sentier, article précédent, prolongement envisagé. Ne pas toucher §2–§5.

**La routine s'arrête ici.**

## Rapport final

```
Routine quotidienne — [date]
Article : [titre] (ID YYYY-NNN, type …)
URL : …
Question du Phare : …
Prolongement envisagé : …
Image : idée / légende / alt
À vérifier : WordPress
```

## Économie de tokens

Ne pas relire un fichier après une édition réussie. Résumer les sorties JSON. Lire la mémoire par sections, pas l'index entier (utiliser `tail` / filtres Python).

## Ne pas faire

- Produire un triptyque ou un atelier Sentier (→ `/routine-triptyque` ou `/routine-mensuelle`).
- Modifier `02_Fonds/`, `03_Dossiers/`, les §2–§5 de la mémoire.
- Inventer une URL interne.
- `editorial_pipeline.py` sans demande explicite `api`.
