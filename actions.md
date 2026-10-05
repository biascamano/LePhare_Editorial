# Actions disponibles — Le Phare Editorial

Répertoire de tout ce qui peut être déclenché dans le dépôt. Décisions et état des routines : `plan.md`.

Légende : 🟢 lecture seule / sans effet · 🟡 écrit en local · 🔴 écrit sur WordPress · 💰 API payante

---

## 1. Routines (prompts à taper dans Claude Code)

Toutes s'exécutent en autonomie totale jusqu'au rapport final. Déclenchement manuel uniquement.

| Prompt | Slash command | Ce que ça fait |
|--------|---------------|----------------|
| `routine quotidienne` | `/routine-quotidienne` | Veille 24–72 h, choix d'**un** sujet, rédaction d'un article (Actualité, Question, Application, ou Texte fondateur occasionnel) avec sa Question du Phare, index, publication WP, une ligne en mémoire §1. 🔴 |
| `routine quotidienne — sujet : …, thème TECH` | idem | Même chose avec sujet, angle et thème imposés. 🔴 |
| `routine quotidienne — type question` / `application` / `texte fondateur` | idem | Même chose avec le type d'article imposé. 🔴 |
| `routine quotidienne — brouillons seulement` | idem | Même chose mais les posts restent en brouillon WP (`--no-publish-final`). 🔴 |
| `routine hebdomadaire` / `fil du phare` | `/routine-hebdomadaire` | Relit la semaine, trouve les connexions, formule une grande question, rédige **Le Fil du Phare** (`SYNTHESE`, catégorie `syntheses`), audite les fils éditoriaux, prépare la semaine suivante, met à jour mémoire §2–§3. 🔴 |
| `routine mensuelle` | `/routine-mensuelle` | Bilan du mois : phénomènes, mise à jour/création de dossiers, 0–2 textes fondateurs, 0–2 ateliers Sentier, synthèse mensuelle si justifiée, audit navigation et équilibre, rapport `06_Syntheses/Rapports_mensuels/YYYY-MM.md`, cap du mois suivant (mémoire §4–§5). 🔴 |
| `routine triptyque` / `triptyque` | `/routine-triptyque` | **Ancienne** routine (archivée, secours) : ACTU + TF + SENTIER atelier le même jour. Accepte aussi sujet imposé et `brouillons seulement`. 🔴 |
| `… api` (ex. `routine triptyque api`) | — | Exception : génération par LLM externe via `editorial_pipeline.py --use-api-llm`. 🔴💰 |

Ce qui reste **manuel (éditeur)** : republier sur WP un fondamental parent `02_Fonds/…` après ajout d'un atelier, désactiver les doublons `wiki-du-phare`, ménage de `07_A_Publier/`.

---

## 2. Publication : `tools/daily_run.py`

Point d'entrée technique des routines. À lancer depuis la racine du dépôt.

| Commande | Ce que ça fait |
|----------|----------------|
| `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder` | **Chaîne standard** : push des brouillons WP → maillage interne (`post_linking`) → publication. Garde le dossier de transit (pas de `rm` autorisé). 🔴 |
| `… --no-publish-final` | S'arrête après le maillage : les posts restent en brouillon. 🔴 |
| `… --force` | Passe outre la garde « déjà exécuté aujourd'hui » (2e routine du jour : hebdo, mensuelle). 🔴 |
| `… --skip-wp-push` | Seconde passe après retouche locale : maillage + publication seulement (posts déjà créés). 🔴 |
| `… --wp-push-only` | Push WP seulement, sans maillage. 🔴 |
| `… --refresh-body` | Réécrit le contenu HTML des posts existants depuis les `.md` (+ Rank Math). 🔴 |
| `… --sync-featured-media` | Met à jour uniquement l'image à la une des posts existants. 🔴 |
| `… --seo-enrich-after-link` | Après maillage, passe SEO/Rank Math par API puis refresh WP. Exige `seo_enrich_api_enabled` + `api_key`. Triptyque uniquement (3 IDs). 🔴💰 |
| `python tools/daily_run.py --use-api-llm --topic "…"` | Génère manifeste + articles par LLM externe (mode historique). Options `--mode`, `--output-profile`, `--theme`, `--angle`, `--no-publish-drafts`. 🔴💰 |

---

## 3. WordPress : scripts unitaires

| Commande | Ce que ça fait |
|----------|----------------|
| `python tools/wp_push_draft.py --dry-run --config tools/wp_config.example.json --index index_editorial.csv <fichier.md>` | Aperçu JSON (titre, slug, catégorie, tags, HTML) sans rien envoyer. 🟢 |
| `python tools/wp_push_draft.py --config tools/wp_config.local.json --index index_editorial.csv <fichier\|dossier>` | Crée les brouillons WP et met à jour l'index (URL, slug). Ignore les articles déjà poussés sauf `--force`. 🔴 |
| `… --refresh-body` | Réécrit le corps d'un post existant. Autorisé sur `05_Sentier/…`, **jamais** sur `02_Fonds/…`. 🔴 |
| `… --sync-featured-media` | Met à jour l'image à la une seulement. Options : `--featured-media-map`, `--no-featured-media`. 🔴 |
| `… --no-rank-math-meta` | Ne pousse pas les métadonnées Rank Math du bloc `# SEO`. 🔴 |
| `python tools/post_linking.py --dry-run --index index_editorial.csv --config tools/wp_config.local.json <dossier>` | Aperçu du maillage interne d'un dossier (1 ou 3 articles). 🟢 |
| `python tools/post_linking.py --index … --config … <dossier> [--publish-final]` | Insère les liens internes réels, met à jour les posts WP, et les publie avec `--publish-final`. 🔴 |
| `python tools/post_seo_enrich.py --article-ids A,B,C [--dry-run] [--no-wp-refresh]` | Enrichissement SEO par LLM sur 3 articles. Bloqué si `seo_enrich_api_enabled` est faux (sauf `--ignore-config-gate`). 🔴💰 |

---

## 4. Synchronisation depuis WordPress

| Commande | Ce que ça fait |
|----------|----------------|
| `python tools/fetch_wp_categories.py --csv-out 00_Systeme/Manifests/wp_categories_snapshot.csv` | Snapshot des catégories WP (API publique, sans auth). `--json-out`, `--site-url` en option. 🟡 |
| `python tools/fetch_wp_tags.py --csv-out 00_Systeme/Manifests/wp_tags_snapshot.csv` | Snapshot des tags WP. 🟡 |
| `python tools/import_wp_posts.py --dry-run` | Plan d'import des posts WP vers le dépôt, sans écrire. 🟢 |
| `python tools/import_wp_posts.py --apply [--limit N] [--refresh-existing] [--statuses publish,draft] [--include-skipped-categories]` | Importe les posts WP en `.md` classés + lignes d'index (backup `.csv.bak_import_*`). `--refresh-existing` réécrit les `.md` déjà indexés. 🟡 |

---

## 5. Index éditorial

| Commande | Ce que ça fait |
|----------|----------------|
| `python tools/validate_index_editorial.py [--index …]` | Détecte les décalages de colonnes (cause de doublons WP au re-push). 🟢 |
| `python tools/validate_index_editorial.py --ids <ID> [<ID>…]` | Contrôle v3 d'articles : type/chemin/catégorie, ≤ 8 tags dont le tag de thème, champs v3 de l'en-tête, corps rédigé, navigation finale, `Slug propose` = index, meta description, pas d'URL nue dans les Repères, liens internes connus. Les articles d'avant la v3 échouent sur les champs v3 (normal). 🟢 |
| `python tools/build_hubs.py [--dry-run]` | Régénère `## Liens internes du dossier` des pages principales de `03_Dossiers` depuis l'index (volets du sous-dossier + en-têtes `Dossier :`). Local uniquement ; affiche les `--refresh-body` à lancer. 🟡 |
| `index_editorial_utils.build_index_row(...)` + `append_rows_to_index(...)` (Python) | **Seule** façon autorisée d'ajouter une ligne à l'index. 🟡 |
| `python tools/new_article.py create --type <type> --theme <THEME> --title "…" [--slug …] [--pillar …] [--fondamental-id …] [--dossier-dir …] [--dry-run]` | Crée un article déjà rangé : réserve l'ID, choisit dossier, nom de fichier, catégorie et tags (≤ 8), écrit le squelette v3 et ajoute la ligne d'index (`en_redaction`). Types : `actualite`, `question`, `application`, `texte-fondateur`, `fil-du-phare`, `synthese-mensuelle`, `dossier`, `atelier`. 🟡 |
| `python tools/new_article.py stage <ID> [--date YYYY-MM-DD]` | Copie le fichier canonique rédigé dans `07_A_Publier/<date>_<slug>/`, prêt pour `daily_run.py --publish-existing`. Refuse si le contrôle v3 est KO (`--force` pour passer outre, hors routine). 🟡 |
| `python tools/merge_index_fragment.py [--out PATH]` | Fusionne un fragment CSV dans l'index (en place, ou vers `PATH` si l'index est verrouillé). Usage ponctuel historique. 🟡 |
| `python tools/_merge_index_to_merged_file.py` | ⚠️ **S'exécute sans argument** : écrit `index_editorial.merged.csv` (index + fragment). 🟡 |

---

## 6. Sentier du Savoir

| Commande | Ce que ça fait |
|----------|----------------|
| `python tools/rebuild_sentier_fondamentaux_canonical.py` | ⚠️ **S'exécute sans argument** et réécrit `00_Systeme/Manifests/sentier_fondamentaux.csv` (URLs canoniques hors `wiki-du-phare`). Helper ponctuel ; relancé sur un manifeste déjà traité, il **duplique** les colonnes `url_canonique`, `nom_fichier`, `exclure_wiki`. À ne pas relancer sans correction. 🟡 |

---

## 7. Génération par API (exception)

| Commande | Ce que ça fait |
|----------|----------------|
| `python tools/editorial_pipeline.py "<sujet>" --manifest-only` | Génère seulement le manifeste éditorial. 🟡💰 |
| `python tools/editorial_pipeline.py "<sujet>" --use-api-llm [--mode triptyque\|architecture_editoriale\|mini_encyclopedie] [--output-profile …] [--theme …] [--angle …] [--publish-folder-name …]` | Génère les articles par LLM externe dans `07_A_Publier/`. 🟡💰 |
| `… --publish-drafts --wp-config tools/wp_config.local.json` | Pousse en plus les brouillons WP. 🔴💰 |

---

## 8. Maintenance du système

| Action | Comment |
|--------|---------|
| Faire évoluer une routine | Modifier le skill `.claude/skills/routine-*/SKILL.md`, puis `plan.md` (§12 état, §13 journal) — procédure `plan.md` §17. |
| Changer catégories / tags | `00_Systeme/Taxonomie_WordPress_le-phare_info.md` puis `plan.md` §9.5. |
| Changer l'en-tête d'article | `00_Systeme/Modele_Entete_Article.md` + skills concernés. |
| Ajuster la mémoire partagée | `00_Systeme/Memoire_editoriale.md` (chaque routine n'écrit que dans ses sections). |
| Rétro hebdomadaire | Copier `00_Systeme/Retro_routine_hebdo_TEMPLATE.md`. |
| Contrôle avant publication | `00_Systeme/Checklist_publication.md`. |
