---
name: routine-triptyque
description: ANCIENNE routine quotidienne (archivée, conservée en secours) — triptyque ACTU+TF+SENTIER complet. Déclenché uniquement par « routine triptyque », « triptyque », ou /routine-triptyque.
---

# Routine triptyque Le Phare (ancienne routine quotidienne, archivée)

> Remplacée le 2026-10-05 par les routines quotidienne / hebdomadaire / mensuelle. Conservée en secours.

## Quand utiliser

L'utilisateur dit `routine triptyque`, `triptyque`, ou invoque ce skill.

Variantes à détecter dans le prompt :
- **Sujet imposé** : extraire titre/angle et thème (TECH, CLIMAT, ECON, SCIENCE, POL, CULTURE).
- **Brouillons seulement** : ajouter `--no-publish-final` à `daily_run.py`.
- **`api` dans le prompt** : basculer sur `editorial_pipeline.py --use-api-llm` (exception).

## Checklist d'exécution

Copier mentalement cette liste et cocher chaque étape avant de conclure.

### Phase A — Préparation

- [ ] Lire `CLAUDE.md` et `.claude/skills/routine-triptyque/workflow.md` si pas déjà en contexte.
- [ ] Dernier ID dans `index_editorial.csv` → réserver 3 IDs consécutifs pour ACTU, TF, SENTIER.
- [ ] Scanner les 3 derniers fichiers SENTIER (`05_Sentier/`, tri ID desc) pour rotation étape + format de titre.
- [ ] Veille web si sujet non imposé (priorité TECH/CULTURE).

### Phase B — Rédaction

- [ ] ACTU rédigée (posture Observer ; §3.8 si sujet institutionnel).
- [ ] TF rédigé (posture Comprendre ; lien ACTU).
- [ ] SENTIER rédigé (grille outil ; 3 règles densité §3.7).
- [ ] Micro-édition sur les 3 textes.
- [ ] Calibrage longueur/densité par type (automatique, sans demander).

### Phase C — Ancrage Sentier

- [ ] Fondamental parent choisi dans `00_Systeme/Manifests/sentier_fondamentaux.csv` (pas wiki-du-phare).
- [ ] Métadonnées SENTIER : `Type Sentier : atelier`, fondamental lié.
- [ ] Ligne ajoutée dans `## Ateliers` du fondamental parent canonique, puis `python tools/wp_refresh_body.py "<chemin 02_Fonds/…>" --allow-fonds` sur ce fichier `02_Fonds/…` (PATCH du corps WP existant — autorisé, voir « Ne pas faire »).

### Phase D — Fichiers

- [ ] En-têtes complets + bloc `# SEO` + `Slug propose` sur chaque fichier.
- [ ] `Repères de sources` avec `[libellé](url)`.
- [ ] `Dans ce triptyque` (libellés hors liens).
- [ ] Sauvegarde chemins canoniques (`01_…`, `04_…`, `05_…`).
- [ ] Copie dans `07_A_Publier/<YYYY-MM-DD_slug>/`.
- [ ] `index_editorial.csv` mis à jour via `index_editorial_utils.append_rows_to_index`.

### Phase E — Publication

- [ ] `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder` (+ options si demandées). `--keep-publish-folder` est systématique (pas de `rm` autorisé) ; ménage manuel occasionnel du dossier `07_A_Publier/`.
- [ ] Refresh SENTIER atelier WP si corps post-maillage modifié (`python tools/wp_refresh_body.py "<chemin>"`).
- [ ] Rapport final à l'utilisateur : URLs WP, doublons wiki si slugs -2/-3.

## Rapport final (format)

```
Routine triptyque — [date]
Sujet : …
IDs : ACTU YYYY-NNN | TF YYYY-NNN | SENTIER YYYY-NNN
URLs WP : …
Étape Sentier : … | Fondamental parent : fondamental-YYYY-NNN
À faire manuellement : vérifier WP ; doublons wiki si slugs -2/-3
Log : 00_Systeme/Logs/daily_run_YYYY-MM-DD.json
```

## Économie de tokens

- Rediriger les sorties JSON verbeuses (`daily_run.py`, `wp_push_draft.py`) et n'extraire/résumer que les champs utiles (`status`, `error`, `wordpress_id`, `link`) plutôt que d'afficher le JSON complet.
- Ne pas relire un fichier juste après une édition réussie (l'outil confirme déjà l'écriture).
- Ne pas redemander confirmation sur les choix déjà actés (sujet, mode de publication) : exécuter toute la chaîne d'un trait jusqu'au rapport final.

## Ne pas faire

- Demander validation du sujet avant de rédiger.
- Lancer `editorial_pipeline.py` sans demande `api`.
- Push WP sur `02_Fonds/…` pour créer un nouveau post (le `--refresh-body` du fondamental parent en Phase C est une exception : PATCH du corps existant, pas une création).
- Oublier le calibrage ou l'ancrage atelier.
