# Mode brouillons (pilote de l'orchestrateur)

**Tant que ce fichier existe, rien n'est rendu public automatiquement sur WordPress** (`plan.md` D22, message 11).

- `post_linking.py --publish-final` est refusé : `daily_run.py` laisse les articles en brouillon WP (`wp_draft`), même si `--no-publish-final` a été oublié.
- `wp_refresh_body.py` est refusé : aucun article en ligne n'est modifié (ni « relier en retour », ni rattrapage). Le rattrapage dépose sa version révisée dans `07_A_Publier/` pour validation.
- `routine phare` passe d'elle-même en variante `brouillons seulement`.

Le fondateur garde la main :
- publier un brouillon : `python tools/verify_publication.py --publish-drafts <ID>` (met aussi l'index à `publie`) ; publié depuis l'admin WP : `python tools/verify_publication.py <ID> --fix` pour resynchroniser l'index ;
- appliquer un refresh validé (rattrapage déposé dans `07_A_Publier/`) : `python tools/wp_refresh_body.py "<chemin>" --hors-pilote` ;
- après publication d'une Question ou d'une Application : demander `relier en retour <ID>` (la séance relie l'article d'origine, puis refresh `--hors-pilote` sur cette demande).

Le journal garde le statut `brouillon` décidé par la séance ; `phare.py contexte` signale « publié ensuite par le fondateur » d'après l'index.

Chaque journée de pilote se clôt par un bilan (`routine phare — bilan pilote` → `06_Syntheses/Retros/<jour>_bilan_pilote.md`), distinct de la rétro hebdomadaire.

**Passage en publication réelle : décision du fondateur seul, en supprimant ce fichier** (commit dédié). Aucune routine ne le supprime.
