# Workflow — après publication WordPress

Enchaînement recommandé une fois un article publié par une routine (`routine phare`, `routine quotidienne`…).

## 0. Condition

- L’article est **publié** : statut `publie` dans `index_editorial.csv` et `python tools/verify_publication.py <ID>` sans erreur.
- Tant que `00_Systeme/Mode_brouillons.md` existe, les articles restent en brouillon jusqu’à publication par le fondateur : **aucun post** sur un brouillon.
- Pas de post systématique : un article par jour, deux à quatre posts par semaine au total (voir `00_Strategie/calendrier-type.md`). Choisir les articles qui portent le mieux une question.

## 1. Récupérer les URLs

```bash
python tools/index_lookup.py <ID>
```

- URL de l’article, question du Phare, article suivant éventuel (Question / Application qui l’a reprise), fondamental du Sentier lié (navigation de l’article).

## 2. Créer le pack social

```text
08_Social/02_Contenus/a-publier/YYYY-MM-DD_<slug>/
  pack.md      ← copier depuis gabarit-post-article.md
  visuel.png   ← optionnel
```

Rédiger les posts **à la main** en phase 1 (qualité > automatisation), ou demander `pack social [<ID>]` à Claude Code (skill `.claude/skills/pack-social/`) : brouillon de pack, rien n'est posté.

## 3. Relecture (2 min)

- [ ] Le post ne contredit pas l’article
- [ ] Pas de clickbait
- [ ] Lien fonctionne (URL de l’index, pas de `?p=`)
- [ ] Hashtags ≤ 4

## 4. Planifier ou publier

- Phase manuelle : copier-coller dans LinkedIn / Bluesky.
- Plus tard : Buffer, Later, ou script interne.

## 5. Archiver

Dans `pack.md` : statut **publié**, dates, plateformes.

Déplacer le dossier vers `02_Contenus/archives/YYYY-MM/` une fois terminé (créer le dossier au besoin).

## Lien avec la routine éditoriale

| Étape Editorial | Étape Social |
|-----------------|--------------|
| Article publié, `verify_publication` OK | Décider s’il est relayé ; créer le dossier `a-publier/` |
| Index à `publie` | Copier URL et question du Phare dans `pack.md` |
| — | J+1 LinkedIn ; J+3 à J+7 prolongement (question suivante ou Sentier) |

## Évolution technique (non implémentée)

Un script pourrait lire un article et proposer un brouillon LinkedIn à valider :

```bash
# futur
python tools/social_pack_from_article.py --article-id 2026-568
```

À brancher seulement si la rédaction manuelle devient un goulot.
