---
name: routine-quotidienne
description: Routine quotidienne Le Phare (V5, pilotage éditorial adaptatif) — part de l'état éditorial (derniers articles, fils, Radar) puis de l'actualité, choisit LE meilleur prochain article et son type (Actualité, Question, Application, exceptionnellement Texte fondateur), le rédige, le publie sur WordPress, le relie et le mémorise. Déclenché par « routine quotidienne » ou /routine-quotidienne. Variante « paire » = Actualité + Question le même jour. (L'ancien triptyque = /routine-triptyque.)
---

# Routine quotidienne — Le Phare Info

**Question du jour : « Quel est le meilleur prochain article du Phare ? »**

Regarder derrière (ce qu'on vient de publier), devant (le Radar), autour (l'actualité) ; choisir ; publier ; relier ; mémoriser (`plan.md` D12–D14).

Le quotidien produit **un** article par séance, dont le type se décide **après** le sujet. Il ne fait PAS : restructuration des dossiers, synthèse de la semaine, architecture du Sentier, analyse du mois, atelier Sentier, tri du Radar → routines hebdomadaire / mensuelle.

Référence éditoriale : `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` (ligne éditoriale) et `00_Systeme/Instructions_editoriales_officielles.md` (qualité rédactionnelle). Écart entre les deux → le signaler dans le rapport, ne pas trancher seul (D10).

**Sobriété** : avant de lire un fichier, se demander s'il est nécessaire. Lectures par défaut : **trois** (État courant, Radar, veille web). Pas de `Catalogue_editorial.md`, pas de mémoire complète, pas d'index entier.

## Variantes du prompt

- **Sujet imposé** (`routine quotidienne — sujet : …, thème TECH`) : respecter sujet/angle/thème ; le type reste à choisir (étape 5) sauf s'il est précisé.
- **Brouillons seulement** : `--no-publish-final`.
- **`type application` / `type texte fondateur` / `type actualite`** : type imposé, sujet choisi par la routine.
- **`type question — sur <ID>`** : article Question sur la question finale de `<ID>` (`--previous <ID>`). Sans `<ID>` : première question P1 du Radar (bloc 2).
- **`paire`** : Actualité + Question le même jour (mécanique en fin de skill). Ancienne règle D9, désormais sur demande.

**Activités** (`plan.md` D18) — une par séance, plusieurs séances possibles le même jour (conversations distinctes) :
- **`generale`** : regard général. Veille **toujours complète** (étape 3, 5 à 10 sujets) ; le Radar ne fournit que des candidats parmi d'autres.
- **`curiosite`** : regard curiosité. Partir du bloc 6 du Radar (questions `ouverte`), puis veille ciblée sur ces champs. Un **ancrage vérifiable** du jour (fait, publication, décision, découverte sourcée) est obligatoire : sans ancrage, une autre question du bloc ; si aucune n'en a, la séance s'arrête sans article et le trace. Type Actualité par défaut (Question/Application si le sujet l'appelle). `memoire_append --type-label "Actualité — curiosité"` (ou « Question — curiosité »…). Ligne du bloc 6 → `explorée (<ID>)`.
- **`question`** : Question autonome, d'origine libre (question finale d'un article ancien, bloc 2 du Radar, dossier). Sans doublon avec l'index (`index_lookup.py --search`) ni avec les articles du jour.
- Sans activité précisée : comportement d'origine (meilleur prochain article).

Toute séance relit l'état courant **régénéré** (il liste les articles déjà publiés le jour même) pour éviter un doublon.

Autonomie totale : pas de validation du sujet, pas de confirmation intermédiaire, exécution jusqu'au rapport final.

**Sous l'orchestrateur** (`routine phare`, `plan.md` D22) : l'activité est imposée par `tools/phare.py`. Signaux `phare.py etape` après `create` (`--etape redaction --ids <ID>`), à la décision PUBLIER (`controle_ok`) et avant `daily_run` (`wp`), puis `close` : `publie`, `brouillon` (contrôle non satisfait), `termine_sans_publication` (curiosité sans ancrage, aucun sujet qui mérite publication) ou `incident` (échec technique). En reprise : même ID et même dossier de transit, jamais de nouveau `create`.

## 1. Regarder derrière : l'état immédiat

Lancer `python tools/build_etat_courant.py`, puis lire `00_Systeme/Etat_editorial_courant.md` (≤ 50 lignes) : compteur du Radar, 10 derniers articles, 5 fils actifs, questions prioritaires, prochains candidats, cap du mois, dernier Fil du Phare. Ne lire `00_Systeme/Memoire_editoriale.md` qu'en cas de besoin précis (une ligne, un fil), par section.

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

`--title` sans préfixe : le script ajoute « Question du Phare - », « Application du Phare - » ou « Texte fondateur - » (aucun préfixe pour une Actualité, `plan.md` D16). Le script renvoie `id`, `path` et `title` (ID, dossier, nom de fichier, catégorie, tags, ligne d'index calculés ; ne jamais écrire l'index à la main ni via `csv.writer`). Écrire le corps à la place de `[Corps de l'article à rédiger]`, compléter la navigation, `Sources principales` et le bloc `# SEO` (mot-clé, meta description, `Slug propose`). Pour une Question : `Question du Phare` = la question traitée, `Article precedent (ID)` = l'article d'origine.

```bash
python tools/new_article.py stage <ID>
```

`stage` lance le contrôle v3 : s'il est KO, corriger et relancer — jamais `--force` sur `stage` en routine.

**Contrôle prépublication** (`plan.md` D20, grille `00_Systeme/Controle_prepublication.md`, lue à ce moment-là) :
1. **Auto-contrôle** : chaque point A–D avec sa preuve ; ouvrir chaque lien externe.
2. **Relecture indépendante** (pilote : tous les articles) : lancer l'agent `relecteur-prepublication` avec pour seul prompt le chemin du fichier canonique (ni fiche, ni candidats, ni raisonnement).
3. **Décision** : PUBLIER → `daily_run` ; CORRIGER → corriger, `stage`, refaire 1 puis 2 (2 cycles au plus) ; BROUILLON → `daily_run … --no-publish-final`, puis étapes 10–11, trace, et **la séance s'arrête** (pas d'autre sujet).

```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder [--force] [--no-publish-final]
```

`--force` sur `daily_run` dès qu'un run a déjà réussi le même jour (deuxième séance du jour et suivantes). Extraire seulement `status`, `error`, `wordpress_id`, `link` des sorties JSON.

**Relier en retour** : si l'article est une Question ou une Application issue d'un article récent, dans l'article d'origine (copie canonique), remplacer la question nue de « La question suivante » par `[question](URL lue dans l'index)`, puis `python tools/wp_refresh_body.py "<chemin canonique de l'origine>"` (le script trouve seul la config WP locale : ne jamais écrire son chemin dans une commande, ne pas lire ce fichier). **Mode brouillons** (`00_Systeme/Mode_brouillons.md` présent) : ne pas toucher l'origine, noter « relier en retour à faire après publication » dans la trace.

**Signaler sans rénover** (`plan.md` §19.4) : un article lié (Pour aller plus loin, Sentier) qui est sous le standard (import brut, sans navigation v3, texte en bloc) OU dont le lien est jugé faible ne se modifie pas pendant la quotidienne. L'inscrire en une ligne dans la table « Ouverts » de `00_Systeme/Signalements_renovation.md` (date, ID, titre lié, `quotidienne <ID>`, constat, suite proposée ; compléter la ligne s'il y est déjà), et le mentionner au rapport. Fondamental `02_Fonds/` : proposition seulement, l'éditeur humain valide et pousse.

## 10. Mémoriser

```bash
python tools/memoire_append.py <ID> --penseur "<penseur ou concept>" --sentier <ID fondamental>
```
(ajoute la ligne au §1 de la mémoire depuis l'en-tête et l'index ; `--dry-run` pour voir la ligne. Activité curiosité : `--type-label "Actualité — curiosité"`. Brouillon : pas de ligne §1, la trace suffit.)

Puis, dans `00_Systeme/Radar_editorial.md` (`plan.md` D19) :
- **retirer** l'entrée réalisée (s'il y en a une) ; curiosité : statut du bloc 6 → `explorée (<ID>)` ;
- si l'article est une Actualité : **ajouter** sa Question du Phare au bloc 2 **seulement si elle est P1 ou P2** (`| P1 | Question | <question> (<THEME>) | <ID> | approfondir |`) et, si un fait est attendu, une suite au bloc 1 (`à échéance (…)`) ; une piste P3 durable → bloc 6 si elle touche un centre d'intérêt, sinon Archives (« P3, réserve ») ;
- compteur au-dessus de 30 (état courant) : ne rien archiver soi-même, le noter dans la trace.
Ne pas fusionner, re-prioriser ni archiver les entrées existantes : c'est le rôle de l'hebdomadaire.

**Trace de séance** (`plan.md` D21) : ajouter un bloc à `06_Syntheses/Retros/YYYY-Snn.md` (semaine ISO ; créer le fichier depuis le gabarit de `06_Syntheses/Retros/README.md` s'il manque). Aussi en cas de BROUILLON ou de séance sans article.

## 11. Vérifier (`plan.md` D15)

```bash
python tools/verify_publication.py
```
Contrôle les articles des 7 derniers jours : liens internes, maillage aller-retour, navigation, URL nues, statut WP, tag `a-la-une` (**sans ce tag, l'article est invisible sur le site**).
- Erreur de tag `a-la-une` ou lien `?p=` vers un article publié → `python tools/verify_publication.py --fix`, puis relancer sans option.
- Autre erreur → corriger le fichier canonique, puis `python tools/wp_refresh_body.py "<chemin>"`.
- Avertissement « lien vers un brouillon » : normal en mode `brouillons seulement`, à signaler.
- Ne jamais lancer `--publish-drafts` sans demande.

En dernier : `python tools/build_etat_courant.py`.

**La routine s'arrête ici.**

## Rapport final

```
Routine quotidienne — [date] — activité : générale | curiosité | question | (défaut)
Candidats : 1. … (sorte, notes) · 2. … · … (5 au plus)
Choix : [titre] (ID YYYY-NNN, <type>) — URL
Pourquoi celui-là : 2–3 phrases (critères décisifs)
Pourquoi ce type : 1 phrase
Question du Phare : …
Contrôle : auto (codes relevés) · relecteur (codes, verdict) · divergences · cycles · décision
Liens : origine → article ok / article → origine ok (ou sans objet)
Radar : retiré … / ajouté …
Signalés : <ID> — constat en une ligne (ou aucun)
Image : idée / légende / alt
Écarts socle / Instructions : … (ou aucun)
Vérification : N articles, X erreurs (corrigées : …), Y avertissements (…)
Trace : 06_Syntheses/Retros/YYYY-Snn.md
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
- Publier sans contrôle prépublication, ou transmettre au relecteur autre chose que le chemin du fichier.
- Chercher un autre sujet après un BROUILLON dans la même séance.
- Ajouter une entrée P3 au Radar actif.
- `editorial_pipeline.py` sans demande explicite `api`.
