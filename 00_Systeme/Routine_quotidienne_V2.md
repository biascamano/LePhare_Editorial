> **ARCHIVÉ (2026-10-05)** — décrit l'ancienne routine triptyque (`routine triptyque`). Routines actuelles : `.claude/skills/routine-quotidienne|hebdomadaire|mensuelle/`.

# Routine quotidienne Le Phare — V2

> **La V1 (`Routine_quotidienne.md`) reste valide et inchangée.** Ce fichier documente les
> améliorations apportées par la V2 aux scripts techniques et au workflow éditorial.

---

## Ce qui change en V2

### Corrections dans les scripts (rétro-compatibles)

| Fichier | Problème V1 | Fix V2 |
|---------|-------------|--------|
| `wp_push_draft.py` | `'NoneType' object has no attribute 'strip'` sur frontmatter malformé → crash de tous les articles | Défensif : `(metadata.get(key) or "").strip()` — valeur None traitée comme `""` |
| `wp_push_draft.py` | `Missing required field: Slug propose` → crash + re-run manuel | Dérivation automatique du slug depuis le nom de fichier si absent (`_slug_from_filename`) |
| `post_linking.py` | `Unable to extract WordPress post ID from URL 'slug/'` quand l'article est déjà publié (permalink propre) | Fallback WP API par slug via `find_wp_post_id_by_slug` ; config chargé tôt dans `main()` |
| `daily_run.py` | Message de garde-fou peu explicite ; pas de rappel fondamental parent | Message `--force` explicite dans le log ; champ `parent_refresh_reminder` dans le JSON de run |

### Nouveau champ JSON dans les logs de run

Après chaque run avec maillage réussi, `daily_run_YYYY-MM-DD.json` contient :

```json
"parent_refresh_reminder": {
  "needed": true,
  "sentier_article_id": "2026-483",
  "sentier_canonical_path": "05_Sentier/Science/2026-483_..._V1.md",
  "sentier_wp_url": "https://le-phare.info/?p=4547",
  "parent_fundamental": "fondamental-2026-154",
  "action": "1. wp_push_draft --refresh-body sur le fichier SENTIER canonique … 2. Rafraîchir manuellement le fondamental parent (fondamental-2026-154) sur WP …"
}
```

Ce champ remplace le rappel mental post-run : il est directement lisible dans le log JSON.

---

## Workflow éditorial V2 (identique à V1, avec les améliorations actives)

```
1. Choisir le sujet (rotation thématique et Sentier — voir § ci-dessous)
2. Rédiger le triptyque ACTU + TF + SENTIER
3. Micro-édition finale
4. Calibrage qualité par type (ACTU/TF/SENTIER — automatique)
4 bis. Ancrage SENTIER atelier (fondamental parent + ## Ateliers)
5. Repères de sources + Dans ce triptyque
6. Sauvegarder dans dossiers canoniques + 07_A_Publier
7. Mettre à jour index_editorial.csv
8. Lancer daily_run.py --publish-existing
9. Vérifier sur WordPress
10 bis. Refresh SENTIER atelier sur WP (wp_push_draft --refresh-body sur 05_Sentier/…)
        → le champ parent_refresh_reminder du JSON indique le fichier à rafraîchir
10 ter. Rafraîchir manuellement le fondamental parent sur WP (afficher ## Ateliers)
```

---

## Rotation thématique et Sentier — guide V2

Ces deux points étaient des lacunes identifiées dans les logs mai 2026.

### Rotation des étapes du Sentier

Avant de choisir une étape pour le SENTIER, consulter les 5 derniers runs dans les logs :
au moins deux étapes différentes devraient être couvertes sur 5 jours consécutifs.

Étapes les plus fréquentes en mai 2026 (à équilibrer) :

| Étape | Fréquence mai-26 | Sous-utilisées |
|-------|-----------------|----------------|
| `Etape_02_Pensee_critique` | Très fréquente | ← à limiter |
| `Etape_08_Relier_savoirs_et_experience` | Fréquente | ← à limiter |
| `Etape_01_Culture_generale` | Rare | ← à prioriser |
| `Etape_03_Argumentation` | Rare | ← à prioriser |
| `Etape_04_Expertise` | Rare | ← à prioriser |
| `Etape_05 à 07` | Absentes | ← à prioriser |

### Rotation thématique

Ordre de priorité si pas de sujet imposé :

1. **TECH** et **CULTURE** : systématiquement sous-représentés — prioriser dès qu'une actu le permet
2. **SCIENCE** et **ECON** : bien couverts, ne pas sur-représenter
3. **CLIMAT** et **POL** : équilibrés, à maintenir

---

## Doublons WordPress (slugs `-2`, `-3`, `-4`)

Les suffixes numériques sur les slugs WP (`-2`, `-4`) indiquent qu'un post avec le même
slug existe déjà (doublon `wiki-du-phare` non désactivé à temps).

**Action systématique** avant ou juste après chaque run :
- Dans WP Admin → Articles → filtrer par état « Publié » et rechercher le slug de base
- Mettre en brouillon les doublons `wiki-du-phare`
- Voir `00_Systeme/Sentier_dedoublonnage_wiki.md`

---

## Commandes V2

La commande principale reste identique à V1 :

```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>"
```

Les options inchangées :
- `--no-publish-final` — garder les brouillons après maillage
- `--wp-push-only` — seulement push WP, pas de maillage
- `--skip-wp-push` — seulement maillage (second passage après retouches)
- `--force` — forcer un second run le même jour
- `--keep-publish-folder` — conserver le dossier staging après succès

Nouveau comportement V2 :
- Si le run du jour était en **erreur**, la relance est automatiquement autorisée (pas de `--force` requis)
- Si le run du jour était en **succès**, le log affiche maintenant le conseil `--force` explicitement

---

## Amélioration continue

Toujours utiliser le gabarit hebdo :

```
00_Systeme/Retro_routine_hebdo_TEMPLATE.md
```

Fréquence recommandée : **une fois par semaine**, 2 minutes.

Sources de backlog à consulter :
- `00_Systeme/Logs/daily_run_YYYY-MM-DD.json` → champ `parent_refresh_reminder`
- `index_editorial.csv` → déséquilibres de thèmes ou étapes Sentier
- Slugs WP `-2` / `-3` → doublons wiki à désactiver

---

## Fichiers modifiés en V2

| Fichier | Nature |
|---------|--------|
| `tools/wp_push_draft.py` | Bug fix : None-safe metadata + slug auto-dérivé (V1.3) |
| `tools/post_linking.py` | Bug fix : fallback WP API pour URL permalink propre |
| `tools/daily_run.py` | Amélioration : garde-fou explicite + `parent_refresh_reminder` |
| `00_Systeme/Routine_quotidienne_V2.md` | Ce fichier — documentation V2 |

Les scripts V1 sont **rétro-compatibles** : aucun argument existant n'est supprimé,
aucun comportement par défaut n'est modifié.
