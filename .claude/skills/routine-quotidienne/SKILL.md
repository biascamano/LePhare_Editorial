---
name: routine-quotidienne
description: Routine quotidienne Le Phare (V5, pilotage éditorial adaptatif) — part de l'état éditorial (derniers articles, fils, Radar) puis de l'actualité, choisit LE meilleur prochain article et son type (Actualité, Question, Application, exceptionnellement Texte fondateur), le rédige, le publie sur WordPress, le relie et le mémorise. Déclenché par « routine quotidienne » ou /routine-quotidienne. Variante « paire » = Actualité + Question le même jour. (L'ancien triptyque = /routine-triptyque.)
---

# Routine quotidienne — Le Phare Info

**Question du jour : « Quel est le meilleur prochain article du Phare ? »**

Regarder derrière (ce qu'on vient de publier), devant (le Radar), autour (l'actualité) ; choisir ; publier ; relier ; mémoriser (`plan.md` D12–D14).

Le quotidien produit **un** article par jour, dont le type se décide **après** le sujet. Il ne fait PAS : restructuration des dossiers, synthèse de la semaine, architecture du Sentier, analyse du mois, atelier Sentier, tri du Radar → routines hebdomadaire / mensuelle.

Référence éditoriale : `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` (ligne éditoriale) et `00_Systeme/Instructions_editoriales_officielles.md` (qualité rédactionnelle). Écart entre les deux → le signaler dans le rapport, ne pas trancher seul (D10).

**Sobriété** : avant de lire un fichier, se demander s'il est nécessaire. Lectures par défaut : **trois** (État courant, Radar, veille web). Pas de `Catalogue_editorial.md`, pas de mémoire complète, pas d'index entier.

## Variantes du prompt

- **Sujet imposé** (`routine quotidienne — sujet : …, thème TECH`) : respecter sujet/angle/thème ; le type reste à choisir (étape 5) sauf s'il est précisé.
- **Brouillons seulement** : `--no-publish-final`.
- **`type application` / `type texte fondateur` / `type actualite`** : type imposé, sujet choisi par la routine.
- **`type question — sur <ID>`** : article Question sur la question finale de `<ID>` (`--previous <ID>`). Sans `<ID>` : première question P1 du Radar (bloc 2).
- **`paire`** : Actualité + Question le même jour (mécanique en fin de skill). Ancienne règle D9, désormais sur demande.

Autonomie totale : pas de validation du sujet, pas de confirmation intermédiaire, exécution jusqu'au rapport final.

## 1. Regarder derrière : l'état immédiat

Lire `00_Systeme/Etat_editorial_courant.md` (généré, ≤ 50 lignes) : 10 derniers articles, 5 fils actifs, questions prioritaires, prochains candidats, cap du mois, dernier Fil du Phare.

S'il manque ou date de plus de 7 jours : `python tools/build_etat_courant.py` puis le lire. Ne lire `00_Systeme/Memoire_editoriale.md` qu'en cas de besoin précis (une ligne, un fil), par section.

## 2. Regarder devant : le Radar

Lire `00_Systeme/Radar_editorial.md` (≤ 30 entrées actives). Repérer : entrées `à échéance` dont la date est atteinte, suites naturelles des derniers articles, questions en attente, connexions, structurants.

## 3. Regarder autour : l'actualité (24–72 h)

Veille web (presse sérieuse, sources institutionnelles). **Si le Radar a déjà un candidat fort** (échéance atteinte, suite naturelle) : la veille se limite à vérifier qu'aucun événement majeur ne doit passer devant. Sinon : 5 à 10 sujets à conséquences réelles, compréhensibles au-delà de l'événement. Écarter buzz, polémique sans conséquence, fait divers isolé, sensationnel.

Une entrée `à échéance` ne s'écrit que si les faits du jour la confirment, sur sources vérifiées ce jour-là.

## 4. Candidats et arbitrage

Constituer **5 candidats au plus**, dont **1 à 3 issus de la veille** :

| Sorte | Exemple |
|---|---|
| A. Actualité nouvelle | un événement majeur des dernières 72 h |
| B. Suite d'un article récent | échéance atteinte, question finale d'une actualité récente |
| C. Connexion | relier deux articles ou un fil à un nouveau terrain |
| D. Contenu structurant | texte fondateur ou application qui éclaire plusieurs articles |

Noter chaque candidat **Faible / Moyen / Fort** sur cinq critères : **importance actuelle**, **continuité** (avec ce qui vient d'être publié, les fils), **durabilité**, **valeur de compréhension**, **nouveauté** (ne pas répéter un sujet sans raison).

Ordre de priorité à notes proches : actualité majeure → suite naturelle → connexion → article structurant. Tenir compte des catégories sous-représentées (cap du mois) sans forcer.

Critère final : **« Cet article est-il le meilleur prochain article du Phare ? »**

## 5. Choisir le type (après le sujet)

| Type | Quand | `--type` | Code index | Dossier canonique | Categorie_WP |
|------|-------|----------|------------|-------------------|--------------|
| **Actualité** | Un fait nouveau à établir et contextualiser | `actualite` | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **Question** | La question finale d'un article récent mérite d'être développée | `question` | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **Application** | Une question déjà étudiée, vue sur un autre terrain (connexion) | `application` | `ACTU` | `01_Actualites/<Theme>/` | `actualites` |
| **Texte fondateur** (exceptionnel) | Un concept devient nécessaire à plusieurs articles — jamais artificiel | `texte-fondateur` | `TF` | `04_Textes_fondateurs/Auteurs/` | `textes-fondateurs` |

Le type découle du sujet, **jamais** d'un équilibrage artificiel. Pas de série rigide (pas « Actualité un jour, Question le lendemain » par principe).

## 6. Fiche de préparation (interne, non publiée)

Sujet / titre provisoire · Type et pourquoi · Pourquoi aujourd'hui (2–4 phrases) · Faits essentiels (5–10) · Certain / incertain · **Question du Phare (une seule)** · Penseur/concept (Question, Application, TF) · Article d'origine (`--previous`) · Dossier existant éventuel · Sentier (fondamental via `00_Systeme/Manifests/sentier_fondamentaux.csv`, jamais `wiki-du-phare`) · Prolongement possible.

**Liens internes : 5 articles au plus vérifiés** avant rédaction, via `python tools/index_lookup.py <IDs>` ou `python tools/index_lookup.py --search "<mot>" [--type question] [--theme SCIENCE] [--dossier 2026-559]`.

## 7. Rédiger

Commun : qualité cible `00_Systeme/Instructions_editoriales_officielles.md` (slow journalism, §3.0 titres adaptés au sujet, §3.8 si institutionnel, gras parcimonieux). Rédiger soi-même (pas d'API / Ollama). L'article doit pouvoir être lu seul. Aucun fait inventé.

**Actualité (~700–1100 mots)** — Factuel, sourcé, accessible, contextualisé, non sensationnaliste. Que s'est-il passé ? que savons-nous avec certitude, que reste-t-il incertain ? causes, conséquences, acteurs, interprétations opposées. Intertitres adaptés au sujet. **Pas de section penseur.** La dernière section fait **émerger** la Question du Phare des faits.

**Question (~800–1200 mots)** — Question claire, ouverte, durable, compréhensible, issue des faits, réutilisable ailleurs, profonde sans devenir artificiellement philosophique. Structure indicative :
1. **Le point de départ** — l'actualité d'origine en **un** paragraphe, lien vers elle.
2. **Pourquoi cette question** — ce que l'événement révèle au-delà de lui-même.
3. **Ailleurs, la même question** — au moins deux autres situations réelles (URLs de l'index).
4. **Une pensée pour regarder autrement** — si pertinent : *tester* une intuition d'un penseur, la confronter aux faits ; jamais d'argument d'autorité. Repères : `plan.md` §5.8. Lien vers un TF seulement s'il est dans l'index.
5. **Ce qui résiste** — objections, limites.
6. **Ce que nous pouvons en retenir** — outils pour penser par soi-même.
7. **La question laissée ouverte**.

**Application (~800–1100 mots)** — Une question déjà posée par Le Phare (lien vers l'article Question ou le TF), appliquée à un terrain nouveau et réel : ce que la grille éclaire, ce qu'elle ne voit pas.

**Texte fondateur (~900–1600 mots)** — Posture Comprendre ; règles de `00_Systeme/Instructions_editoriales_officielles.md` ; liens vers les articles récents qu'il éclaire. `--routine quotidienne` obligatoire.

## 8. Navigation finale (avant `# SEO`)

```markdown
---

**Repères de sources**

- Source : [libellé](url)

**La question suivante**

[Actualité : la Question du Phare · Question/Application/TF : la question laissée ouverte, une phrase]

**Pour aller plus loin**

- [Article d'origine](url)
- [Titre article lié ou dossier](url)

**Sur le Sentier du Savoir**

- [Titre du fondamental](url_canonique)
```

Liens Markdown obligatoires (pas d'URL nue). Liens internes : uniquement des URLs réelles lues dans l'index / le manifeste. Pas de section `Dans ce triptyque`.

## 9. Publier

```bash
python tools/new_article.py create --type <type> --theme <THEME> --title "…" --slug <kebab-case> --pillar <pilier> --question "…" --previous <ID> --linked "<ID>;…" --prolongement "…" --keywords "…;…" --summary "…" --objective "…" --tags "<concept>;<concept>" [--dossier "<ID dossier>"]
```

Le script renvoie `id` et `path` (ID, dossier, nom de fichier, catégorie, tags, ligne d'index calculés ; ne jamais écrire l'index à la main ni via `csv.writer`). Écrire le corps à la place de `[Corps de l'article à rédiger]`, compléter la navigation, `Sources principales` et le bloc `# SEO` (mot-clé, meta description, `Slug propose`). Pour une Question : `Question du Phare` = la question traitée, `Article precedent (ID)` = l'article d'origine.

```bash
python tools/new_article.py stage <ID>
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder [--force] [--no-publish-final]
```

`stage` lance le contrôle v3 : s'il est KO, corriger et relancer — jamais `--force` sur `stage` en routine. `--force` sur `daily_run` seulement si un run a déjà réussi le même jour. Extraire seulement `status`, `error`, `wordpress_id`, `link` des sorties JSON.

**Relier en retour** : si l'article est une Question ou une Application issue d'un article récent, dans l'article d'origine (copie canonique), remplacer la question nue de « La question suivante » par `[question](URL lue dans l'index)`, puis `python tools/wp_refresh_body.py "<chemin canonique de l'origine>"` (le script trouve seul la config WP locale : ne jamais écrire son chemin dans une commande, ne pas lire ce fichier).

## 10. Mémoriser

```bash
python tools/memoire_append.py <ID> --penseur "<penseur ou concept>" --sentier <ID fondamental>
```
(ajoute la ligne au §1 de la mémoire depuis l'en-tête et l'index ; `--dry-run` pour voir la ligne.)

Puis, dans `00_Systeme/Radar_editorial.md` :
- **retirer** l'entrée réalisée (s'il y en a une) ;
- si l'article est une Actualité : **ajouter** sa Question du Phare au bloc 2 (`| P? | Question | <question> (<THEME>) | <ID> | approfondir |`) et, si un fait est attendu, une suite au bloc 1 (`à échéance (…)`).
Ne pas fusionner, re-prioriser ni archiver : c'est le rôle de l'hebdomadaire.

En dernier : `python tools/build_etat_courant.py`.

**La routine s'arrête ici.**

## Rapport final

```
Routine quotidienne — [date]
Candidats : 1. … (sorte, notes) · 2. … · … (5 au plus)
Choix : [titre] (ID YYYY-NNN, <type>) — URL
Pourquoi celui-là : 2–3 phrases (critères décisifs)
Pourquoi ce type : 1 phrase
Question du Phare : …
Liens : origine → article ok / article → origine ok (ou sans objet)
Radar : retiré … / ajouté …
Image : idée / légende / alt
Écarts socle / Instructions : … (ou aucun)
À vérifier : WordPress
```

## Variante `paire` (Actualité + Question le même jour)

`post_linking.py` refuse un dossier de 2 articles (`plan.md` §5.9) : deux dossiers de transit, deux runs.
1. `create` + rédiger l'Actualité ; `stage` ; `daily_run --publish-existing "<dossier A>" --keep-publish-folder [--no-publish-final]`.
2. `create --type question --previous <ID A>` ; rédiger avec l'URL de A **lue dans l'index** ; `stage` ; `daily_run … --keep-publish-folder --force [--no-publish-final]`.
3. Relier en retour A → B (étape 9) ; `memoire_append` pour A puis B ; la question de A n'entre pas au Radar (elle est traitée).
Si B échoue : A reste publié, l'échec est **signalé** dans le rapport.

## Économie de tokens

Ne pas relire un fichier après une édition réussie. Résumer les sorties JSON. URLs : `index_lookup.py`, jamais l'index entier.

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `cd … &&`, `;`, `|`, ni `python -c` multiligne (chaque segment est vérifié séparément et déclenche une demande). Lire / chercher / éditer avec Read, Grep, Edit plutôt qu'avec `cat`, `grep`, `sed`. Ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande.

## Ne pas faire

- Choisir le type avant le sujet, ou pour « équilibrer ».
- Lire `Catalogue_editorial.md` ou la mémoire entière en routine quotidienne.
- Éditer `Etat_editorial_courant.md` à la main (il est régénéré).
- Mettre un penseur dans une Actualité ; répéter dans une Question les faits de l'origine au-delà d'un paragraphe.
- Produire un triptyque ou un atelier Sentier (→ `/routine-triptyque` ou `/routine-mensuelle`).
- Modifier `02_Fonds/`, `03_Dossiers/`, les §2–§5 de la mémoire.
- Inventer une URL interne ou un fait.
- `editorial_pipeline.py` sans demande explicite `api`.
