---
name: routine-quotidienne
description: Routine quotidienne Le Phare — une PAIRE d'articles à partir de l'actualité du jour : A (Actualité, les faits) et B (Question du Phare, ce que l'événement révèle) ; publication WordPress puis deux lignes en mémoire éditoriale. Déclenché par « routine quotidienne » ou /routine-quotidienne. (L'ancien triptyque ACTU+TF+SENTIER = /routine-triptyque.)
---

# Routine quotidienne — Le Phare Info

**Question du jour : « Que s'est-il passé, et qu'est-ce que cela révèle ? »**

Le quotidien produit les briques : chaque jour, un article **A — Actualité** (« Voir ») et un article **B — Question du Phare** (« Interroger ») qui pose la question finale de A (`plan.md` D9–D11). Il ne fait PAS : restructuration des dossiers, synthèse de la semaine, architecture du Sentier, analyse du mois, création systématique de texte fondateur ou d'atelier Sentier → routines hebdomadaire / mensuelle.

Référence éditoriale : `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` (ligne éditoriale) et `00_Systeme/Instructions_editoriales_officielles.md` (qualité rédactionnelle). Écart entre les deux → le signaler dans le rapport, ne pas trancher seul (D10).

## Variantes du prompt

- **Sujet imposé** (`routine quotidienne — sujet : …, thème TECH`) : respecter sujet/angle/thème ; produire la paire.
- **Brouillons seulement** : `--no-publish-final` sur tous les runs.
- **`type application` / `type texte fondateur`** : article **seul** (C ou D), pas de B.
- **`type question — sur <ID>`** : article **B seul**, en rattrapage, sur la question finale de l'article `<ID>` déjà publié (étapes 6B à 9 seulement, `--previous <ID>`). Sans `<ID>` : prendre la première entrée P1 de `00_Systeme/Articles_a_creer.md` §2.

Autonomie totale : pas de validation du sujet, pas de confirmation intermédiaire, exécution jusqu'au rapport final.

## 1. Lire la mémoire éditoriale

`00_Systeme/Memoire_editoriale.md` : §1 (15 dernières lignes), §2 fils actifs, §3 dernier Fil du Phare, §4 cap du mois. Identifier sujets récents, Questions du Phare ouvertes, dossiers actifs, penseurs récents, étapes du Sentier sollicitées, prolongements envisagés. Ne pas répéter un sujet sans raison.

Puis `00_Systeme/Articles_a_creer.md` §1–§2 (liste priorisée tenue par l'hebdomadaire et la mensuelle) : repérer les entrées P1 dont l'échéance est atteinte.

Les deux IDs (A puis B) sont attribués à l'étape 8 par `tools/new_article.py` (ne pas les calculer à la main).

## 2. Analyser l'actualité (24–72 h)

Veille web (presse sérieuse, sources institutionnelles). Retenir 5 à 10 sujets ayant des conséquences réelles, compréhensibles au-delà de l'événement, ou prolongeant une question / un dossier existant, ou faisant émerger une question durable. Écarter buzz, polémique sans conséquence, fait divers isolé, sensationnel.

## 3. Choisir UN sujet

Critères : importance, durabilité, intérêt intellectuel, originalité, connexion avec les publications précédentes. **Le potentiel de Question du Phare est décisif** : un sujet qui n'ouvre aucune question réutilisable ailleurs ne fait pas une paire. Tenir compte des catégories sous-représentées (§4 de la mémoire) sans forcer. Une entrée P1 de `00_Systeme/Articles_a_creer.md` arrivée à échéance passe en tête des candidats si l'actualité du jour la confirme ; sinon la laisser.

## 4. Déterminer la forme

Par défaut : **la paire A + B**. Article seul uniquement sur demande explicite (variantes).

| Article | Question principale | `--type` | Code index | Dossier canonique | Categorie_WP |
|---------|---------------------|----------|------------|-------------------|--------------|
| **A. Actualité** | Que s'est-il passé et pourquoi est-ce important ? | `actualite` | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **B. Question du Phare** | Qu'est-ce que cet événement révèle au-delà de lui-même ? | `question` | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| C. Application (seul) | Une question déjà étudiée, vue sur un autre terrain | `application` | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| D. Texte fondateur (seul) | Seulement si un concept devient nécessaire — jamais artificiel | `texte-fondateur` | `TF` | `04_Textes_fondateurs/Auteurs/` | `textes-fondateurs` |

Tags de type posés par le script : `type-actualite` | `type-question` | `type-application` | `type-texte-fondateur`, + `question-du-phare`.

## 5. Fiche de préparation (interne, non publiée)

Sujet / titre provisoire · Pourquoi aujourd'hui (2–4 phrases) · Faits essentiels (5–10) · Certain / incertain · **Question du Phare (une seule)**, testée contre les critères du §6B · **Au moins 2 autres domaines ou situations réels** où la question se pose (articles du Phare de préférence) · Penseur/concept comme grille de lecture (si pertinent) · Connexion précédente (quel article y mène) · Dossier existant éventuel · Sentier (étape ou fondamental, via `00_Systeme/Manifests/sentier_fondamentaux.csv`, jamais `wiki-du-phare`) · Prolongement possible.

Si la question est trop faible : la **reformuler**, ne pas sauter B.

## 6. Rédiger

Commun à A et B : qualité cible `00_Systeme/Instructions_editoriales_officielles.md` (slow journalism, §3.0 titres adaptés au sujet, §3.8 si institutionnel, gras parcimonieux). Rédiger soi-même (pas d'API / Ollama). Chaque article doit pouvoir être lu seul. Micro-édition + calibrage automatiques. Aucun fait inventé.

### 6A. Article A — Actualité (~700–1100 mots)

Factuel, sourcé, accessible, contextualisé, non sensationnaliste. Répond notamment à : que s'est-il passé ? que savons-nous avec certitude, que reste-t-il incertain ? quelles causes, quelles conséquences ? quels acteurs ? quelles interprétations s'opposent ?

Intertitres adaptés au sujet (pas de plan fixe). **Pas de section penseur** (elle passe dans B). Ne se termine pas sur une simple synthèse : la dernière section fait **émerger** la Question du Phare des faits.

### 6B. Article B — Question du Phare (~800–1200 mots)

Critères de la question : claire ; ouverte ; durable ; compréhensible ; directement issue des faits ; réutilisable dans d'autres domaines ; profonde sans devenir artificiellement philosophique.

Structure indicative (intertitres à adapter) :

1. **Le point de départ** — l'actualité en **un** paragraphe, lien vers A. Pas de redite des faits au-delà.
2. **Pourquoi cette question** — ce que l'événement révèle au-delà de lui-même.
3. **Ailleurs, la même question** — au moins deux autres domaines ou situations réels (URLs de l'index).
4. **Une pensée pour regarder autrement** — si pertinent : *tester une intuition* d'un penseur, puis la confronter aux faits. Jamais d'argument d'autorité (pas « X avait raison »). Repères : `plan.md` §5.8. Lien vers un TF seulement s'il est dans l'index ; sinon nommer sans lien.
5. **Ce qui résiste** — objections, limites, ce que la question ne permet pas de trancher.
6. **Ce que nous pouvons en retenir** — outils pour penser par soi-même.
7. **La question laissée ouverte** — prolongement ; n'appelle pas automatiquement un nouvel article.

Titre : la question elle-même ou une formulation courte qui la porte.

## 7. Navigation finale (avant `# SEO`)

```markdown
---

**Repères de sources**

- Source : [libellé](url)

**La question suivante**

[A : la Question du Phare — devient un lien vers B une fois B publié (§8, étape 3)]
[B : la question laissée ouverte, une phrase]

**Pour aller plus loin**

- [B : premier lien = article A](url)
- [Titre article précédent ou dossier](url)

**Sur le Sentier du Savoir**

- [Titre du fondamental](url_canonique)
```

Liens Markdown obligatoires (pas d'URL nue). Liens internes : uniquement des URLs réelles lues dans `index_editorial.csv` / `sentier_fondamentaux.csv`. Pas de section `Dans ce triptyque`.

## 8. Fichiers, index, WordPress

Créer **A puis B avant** de rédiger les corps (ID, dossier, nom de fichier, catégorie, tags et ligne d'index sont calculés par le script) :
```bash
python tools/new_article.py create --type actualite --theme <THEME> --title "…" --slug <kebab-case> --pillar <pilier> --question "…" --previous <ID> --linked "<ID>;…" --prolongement "…" --keywords "…;…" --summary "…" --objective "…" --tags "<concept>;<concept>" [--dossier "<…>"]
python tools/new_article.py create --type question --theme <THEME> --title "…" --slug <kebab-case> --pillar <pilier> --question "<question de A>" --previous <ID A> --linked "<ID A>;<IDs de la section 3>" --prolongement "…" --keywords "…;…" --summary "…" --objective "…" --tags "<concept>;<concept>"
```
(Article seul C/D : un seul `create` ; `--routine quotidienne` obligatoire pour un texte fondateur.) Le script renvoie `id` et `path` : écrire le corps à la place de `[Corps de l'article à rédiger]`, compléter la navigation finale, `Sources principales` et le bloc `# SEO` (mot-clé, meta description, `Slug propose`). En-tête de B : `Type article : Question`, `Question du Phare` = la question traitée, `Article precedent (ID)` = ID de A.

`python tools/new_article.py stage <ID>` copie dans `07_A_Publier/<date>_<slug>/` et lance le contrôle v3 : s'il est KO, corriger et relancer — jamais `--force` en routine. Ne jamais écrire l'index à la main ni via `csv.writer`.

Publication de la paire (mécanique transitoire, `plan.md` §5.9 — `post_linking.py` refuse un dossier de 2 articles) :

1. Rédiger A ; `stage` A ;
   `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier A>" --keep-publish-folder [--no-publish-final]`
2. Rédiger B avec l'URL de A **lue dans l'index** (`python tools/index_lookup.py <ID A>`) ; `stage` B ;
   `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier B>" --keep-publish-folder --force [--no-publish-final]`
   (`--force` : le run du jour est déjà marqué réussi par A.)
3. Dans A (copie canonique **et** copie de transit), remplacer la question nue de « La question suivante » par `[question](URL de B lue dans l'index)`, puis :
   `python tools/wp_refresh_body.py "<chemin canonique A>"`
   (le script trouve seul la config WP locale : ne jamais écrire son chemin dans une commande, la règle deny la bloque ; ne pas lire ce fichier.)

Extraire seulement `status`, `error`, `wordpress_id`, `link` des sorties JSON. Si B échoue : A reste publié, l'échec est **signalé** dans le rapport (jamais livrer A seul en silence).

Fournir dans le rapport : idée d'image, légende, texte alternatif pour A et B (pas de génération d'image).

## 9. Mettre à jour la mémoire éditoriale

Ajouter **deux lignes** (A puis B) à la fin du tableau §1 de `00_Systeme/Memoire_editoriale.md` : date, ID, `[titre](url WP)`, type, catégorie/thème, Question du Phare, dossier, penseur, Sentier, article précédent, prolongement envisagé. Pour B, article précédent = A. Ne pas toucher §2–§5.

Si la paire réalise une entrée de `00_Systeme/Articles_a_creer.md`, **retirer** cette entrée (pas d'ajout : réservé à l'hebdomadaire et à la mensuelle).

**La routine s'arrête ici.**

## Rapport final

```
Routine quotidienne — [date]
A : [titre] (ID YYYY-NNN, Actualité) — URL
B : [titre] (ID YYYY-NNN, Question) — URL
Question du Phare : …
Liens croisés : A → B ok / B → A ok
Prolongement envisagé : …
Images : A idée / légende / alt · B idée / légende / alt
Écarts socle / Instructions : … (ou aucun)
À vérifier : WordPress
```

## Économie de tokens

Ne pas relire un fichier après une édition réussie. Résumer les sorties JSON. Lire la mémoire par sections, pas l'index entier (`python tools/index_lookup.py <IDs>` pour les URLs).

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `cd … &&`, `;`, `|`, ni `python -c` multiligne (chaque segment est vérifié séparément et déclenche une demande). Lire / chercher / éditer avec Read, Grep, Edit plutôt qu'avec `cat`, `grep`, `sed`. Ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande.

## Ne pas faire

- Livrer A seul sans B (hors variante explicite) sans le signaler.
- Répéter dans B les faits de A au-delà d'un paragraphe ; mettre un penseur dans A.
- Produire un triptyque ou un atelier Sentier (→ `/routine-triptyque` ou `/routine-mensuelle`).
- Modifier `02_Fonds/`, `03_Dossiers/`, les §2–§5 de la mémoire.
- Inventer une URL interne ou un fait.
- `editorial_pipeline.py` sans demande explicite `api`.
