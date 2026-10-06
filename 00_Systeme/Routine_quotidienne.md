> **ARCHIVÉ (2026-10-05)** — décrit l'ancienne routine triptyque (`routine triptyque`). Routines actuelles : `.claude/skills/routine-quotidienne|hebdomadaire|mensuelle/`.

# Routine quotidienne Le Phare

## Objectif

Executer de bout en bout une routine editoriale assistee qui :

1. choisit un sujet du jour si aucun sujet manuel n'est fourni
2. redige manuellement un triptyque `ACTU + TF + SENTIER` selon les instructions editoriales
3. applique une micro-edition finale sur les 3 textes
4. applique une phase de **calibrage qualite par type** (longueur, densite, promesse ACTU/TF/SENTIER ; cf. Instructions_editoriales_officielles sections **3.7** et, pour l'ACTU « cadre institutionnel », **3.8**)
4 bis. **ancre le SENTIER** comme **atelier** d'un fondamental existant et met a jour la rubrique **« Ateliers »** en fin du fondamental parent (cf. Instructions **3.9**, `00_Systeme/Manifests/sentier_fondamentaux.csv`, `00_Systeme/Sentier_fondamentaux_referentiel.md`)
5. ajoute des `Reperes de sources` en liens Markdown `[libelle](url)` et le bloc `Dans ce triptyque` avec libelles hors lien (voir Instructions **3.10**)
6. cree les fichiers locaux
7. met a jour `index_editorial.csv`
8. copie dans `07_A_Publier`
9. pousse les brouillons dans WordPress
10. applique le maillage interne automatique du triptyque
10 bis. **Rafraichissement WP du SENTIER atelier** : `wp_push_draft --refresh-body` sur le **fichier SENTIER atelier** canonique uniquement (`--config tools/wp_config.local.json`) — **pas** le fondamental parent (`Sentier_fondamentaux_referentiel.md` §5). Doublons Echo KB : desactivation **manuelle** par l'editeur sur WP (`Sentier_dedoublonnage_wiki.md`).
11. *(optionnel, API payante)* amélioration ciblée **Rank Math / SEO** et diversité rédactionnelle : `tools/post_seo_enrich.py` (après maillage), puis rafraîchissement du corps WP — le prompt système du script encode les critères de la [KB Rank Math « Score 100/100 »](https://rankmath.com/kb/score-100-in-tests/) **sans** sacrifier les longueurs cibles Le Phare (Instructions 3.7) — voir `tools/editorial_config.example.json` (`seo_enrich_api_enabled`, `seo_enrich_model` défaut **gpt-5.5**) et l’option **`--seo-enrich-after-link`** sur `daily_run.py --publish-existing`.

## Fichiers

- `tools/daily_run.py`
- `tools/daily_run.cmd`
- `tools/editorial_pipeline.py`
- `tools/wp_push_draft.py`
- `tools/wp_featured_media.local.json` : remplir surtout **`by_tag_slug`** (themes / Sentier / etc.) pour une **image a la une partagee** (ID ou nom de fichier, ex. `economie.png`) ; categories optionnelles dans `by_category_slug` (voir `wp_featured_media.local.example.json` pour un squelette vide)
- `tools/post_linking.py`
- `tools/post_seo_enrich.py` : passe API post-maillage (contenu + bloc `# SEO` + push Rank Math via `wp_push_draft --refresh-body` ; critères d’analyse Rank Math documentés dans le script + [KB officielle](https://rankmath.com/kb/score-100-in-tests/))

## Choix du sujet

Par defaut, la routine choisit directement un sujet pertinent via veille web ou flux d'actualite.

Le sujet n'est pas soumis a validation utilisateur avant redaction : la routine va jusqu'au brouillon WordPress, puis l'utilisateur verifie le resultat dans WordPress.

**Objectif long terme (graphe de savoir + Sentier + moteur editorial)** : le sujet du jour doit aussi **construire petit a petit l'architecture editoriale** du Phare : nouveaux concepts, liens entre themes, rotation des etapes du Sentier, categories et tags WordPress coherents. Strategie detaillee :

- `00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md`

Source possible de veille :

- `https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr`

Puis elle :
- score les sujets selon les themes du Phare
- ignore les sujets peu pertinents
- evite de reutiliser les sujets recents quand c'est possible
- privilegie les sujets offrant un potentiel d'analyse durable
- applique la grille de choix (noeuds, Sentier, taxonomie) decrite dans la strategie ci-dessus lorsque l'assistant selectionne le sujet

## Lancement manuel

```bash
python tools/daily_run.py
```

## Lancement manuel avec sujet impose

```bash
python tools/daily_run.py --topic "Guerre usa israel iran" --theme POL
```

## Lancement sans push WordPress

```bash
python tools/daily_run.py --no-publish-drafts
```

## Workflow editorial reel

1. Choisir le sujet sans demander une validation intermediaire.
2. Rediger les 3 articles directement avec l'assistant.
3. Faire une micro-edition finale :
   resserrer les phrases, lisser le ton, verifier SEO, titres, transitions et fins d'articles.
4. **Phase de calibrage qualité par type** : executee **systematiquement** pour chaque fichier **sans demander** si elle doit avoir lieu ; verifier le **Type** (`ACTU`, `TF`, `SENTIER`) et ajuster **longueur** et **densite** pour tenir la promesse du format (voir `00_Systeme/Instructions_editoriales_officielles.md`, section 3.7). Priorite : qualite percue par un lecteur engage, pas un quota SEO. **Modele recommandé dans Cursor** pour cette passe : **Claude Sonnet 4.6** ou **GPT-5.5** (ou successeur) pour une revision long-form prudente. Passe HTTP optionnelle uniquement si `calibration_api_enabled` est `true` dans `tools/editorial_config.local.json` et que les scripts y font appel ; validation finale toujours humaine / assistant principal du depot.
4 bis. **Ancrage Sentier — atelier et fondamental** : lire `00_Systeme/Manifests/sentier_fondamentaux.csv` ; choisir etape + fondamental parent ; marquer le SENTIER `Type Sentier : atelier` ; ajouter la ligne dans `## Ateliers (applications sur l'actualite)` en fin du `.md` du fondamental parent (Instructions 3.9).
5. Completer `Repères de sources` et `Dans ce triptyque` selon Instructions **3.10** (URLs en `[texte](url)` ; libelles « Approfondir… » / « Prolonger… » hors du lien).
6. Integrer les fichiers dans les bons dossiers.
7. Dupliquer dans `07_A_Publier`.
8. Pousser les brouillons WordPress (`daily_run --publish-existing` ou equivalent).
9. Ajouter les liens internes du triptyque.
9 bis. **SENTIER atelier** : si le corps local a evolue apres maillage, `wp_push_draft --refresh-body` sur le `.md` **SENTIER** uniquement (`--config tools/wp_config.local.json`) — pas le fondamental (`Sentier_fondamentaux_referentiel.md` §5).
10. Laisser l'utilisateur controler le resultat final dans WordPress (y compris mise en brouillon des doublons `wiki-du-phare` et, si besoin, republication du **fondamental parent** pour afficher la rubrique Ateliers — voir `Sentier_fondamentaux_referentiel.md` §5).

## Logs

Chaque execution cree :

- `00_Systeme/Logs/daily_run_YYYY-MM-DD.log`
- `00_Systeme/Logs/daily_run_YYYY-MM-DD.json`

Le fichier JSON stocke :
- le sujet retenu
- le theme
- le statut
- stdout/stderr du pipeline

## Amelioration continue et agilite

Principes et boucle de retrospective : voir la section du meme nom dans `00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md`.

Gabarit a dupliquer chaque semaine (copier le fichier et renommer avec la periode) :

- `00_Systeme/Retro_routine_hebdo_TEMPLATE.md`

## Tache planifiee Windows

Nom de la tache :

- `LePhareRoutineQuotidienne`

Horaire :

- tous les jours a `04:00`

Commande executee :

- `LePhare_Editorial/tools/daily_run.cmd` (depuis la racine du dépôt Nexus des mondes)

## Garde-fous

- une execution reussie par jour maximum, sauf avec `--force`
- publication WordPress en brouillons uniquement
- logs persistants

## Limites actuelles

- le choix du sujet reste perfectible
- les liens vers d'anciens articles pertinents ne sont pas encore automatiques
- la verification finale editoriale se fait dans WordPress par l'utilisateur
