# Le Phare Social — diffusion & visibilité

Projet **Nexus des Mondes** / **Le Phare Info** : présence sur les réseaux sociaux pour **orienter vers les articles** (le-phare.info), sans reproduire le clickbait ni la course au clic.

**Infos communes** (bios, URLs, mission, hashtags) : [`../../referentiel-commun.md`](../../referentiel-commun.md).

**Complément de la production** du dépôt [`LePhare_Editorial`](../) — pas un second média parallèle.

## Rôle

| Production (dépôt racine) | Diffusion (`08_Social/`) |
|---------------------------|--------------------------|
| Rédaction (un article par jour, routines v3), WordPress | Teasers, fils, visuels, planning de publication |
| Source de vérité : articles `.md` + index | Source de vérité : posts planifiés + métriques légères |

## Navigation

| Dossier | Contenu |
|---------|---------|
| [`00_Strategie/`](00_Strategie/) | Plateformes, priorités, ligne éditoriale RS, calendrier type |
| [`01_Identite/`](01_Identite/) | Bios, handles, charte visuelle à définir |
| [`02_Contenus/`](02_Contenus/) | Gabarits de posts, dossier `a-publier/` |
| [`03_Operation/`](03_Operation/) | Création de comptes, workflow après publication WP |
| [`04_Mesure/`](04_Mesure/) | Indicateurs simples, relecture mensuelle |

## Démarrage rapide (phase 0)

1. Lire `00_Strategie/plateformes-et-priorites.md` et trancher **2 plateformes max** au lancement.
2. Créer les comptes (`03_Operation/checklist-nouveau-compte.md`).
3. Remplir `01_Identite/bios-gabarits.md` et préparer 1 visuel type (`01_Identite/visuels-a-preparer.md`).
4. Pour un article **publié** (pas un brouillon) jugé digne d'être relayé : remplir un pack dans `02_Contenus/a-publier/` avec `gabarit-post-article.md`.
5. Suivre `03_Operation/workflow-apres-publication.md`.

## Évolutions possibles (plus tard)

- Script `tools/social_pack_from_article.py` (titre, URL, question du Phare → brouillon de posts par plateforme).
- Option dans `tools/daily_run.py` (`--social-pack` après publication).
- Planification via Buffer / n8n / API Meta — seulement après validation manuelle des premiers posts.

## Principes non négociables

Alignés sur [`00_Systeme/Instructions_editoriales_officielles.md`](../00_Systeme/Instructions_editoriales_officielles.md) :

- Le post **renvoie** vers l’article ; il ne remplace pas la lecture.
- Pas de titre sensationnaliste « pour l’algo ».
- Citer la source / le cadre quand on résume un fait.
- Transparence : compte officiel Le Phare Info, lien vers le site.
