# Sentier — dédoublonnage wiki-du-phare / Echo Knowledge Base

## Contexte

L’import **Echo Knowledge Base (EPKB)** a créé des articles dupliqués sous l’URL :

`https://le-phare.info/wiki-du-phare/...`

Les **fondamentaux canoniques** du Sentier sont les versions déjà publiées à la **racine du site** :

`https://le-phare.info/{slug}/`

Exemple : [Argumenter en situation complexe](https://le-phare.info/argumenter-en-situation-complexe/) (**2026-182**), pas la copie [wiki-du-phare/argumenter-en-situation-complexe](https://le-phare.info/wiki-du-phare/argumenter-en-situation-complexe/) (**2026-384**).

Environ **77 doublons** (même slug, deux IDs) sont recensés dans `index_editorial.csv`.

## Règle projet (obligatoire)

| À utiliser | À ne pas utiliser |
|------------|-------------------|
| `fondamental_id` et `url_canonique` du CSV `Manifests/sentier_fondamentaux.csv` | Lignes index dont `URL_WordPress` contient `wiki-du-phare` |
| Fichier `nom_fichier` indiqué dans le CSV (souvent `02_Fonds/…` ou ancien import) | Fichiers `05_Sentier/Etape_XX/` **uniquement** s’ils ne sont que des copies KB sans URL racine |
| Rubrique `## Ateliers` en fin du **fichier canonique** | Rubrique Ateliers sur la copie wiki |

Colonne `exclure_wiki` du CSV : `non` = canonique OK ; `manquant` = pas d’URL racine trouvée (à traiter à la main).

## Regénérer le CSV après mise à jour de l’index

```bash
python tools/rebuild_sentier_fondamentaux_canonical.py
```

## Désactivation d’Echo KB sur WordPress

**Responsabilité** : la **desactivation** (mise en brouillon) des articles doublons `/wiki-du-phare/*` sur WordPress est faite **manuellement par l’éditeur** lors de la fermeture d’Echo KB. L’assistant / les scripts du dépôt **ne poussent pas** ces copies et **ne les désactivent pas** à sa place.

Recommandations (hors dépôt) :

1. **Ne pas supprimer** les articles racine (`/argumenter-en-situation-complexe/`, etc.).
2. Mettre en **brouillon** (ou **rediriger 301**) les URLs `/wiki-du-phare/*` vers l’URL racine équivalente (plugin Redirection ou Yoast) — **action éditoriale WP**, pas automatisée ici.
3. Retirer la page [Base de connaissance](https://le-phare.info/wiki-du-phare) du menu si elle ne sert plus.
4. Sidebar Sentier : pointer vers les **10 fondamentaux racine**, pas la KB.

## Fichiers dépôt

- Les copies dans `05_Sentier/Etape_XX/` (IDs 3xx) peuvent rester comme archive import ; ajouter un commentaire HTML en tête si doublon confirmé (voir `2026-384`).
- Pour les **ateliers**, toujours mettre à jour le parent **canonique** (`02_Fonds/…` ou chemin du CSV).

## Liste des ateliers récents (parents canoniques)

| Atelier ID | Fondamental canonique |
|------------|------------------------|
| 2026-468 | 2026-182 — argumenter-en-situation-complexe |
| 2026-465 | 2026-198 — lire-une-source-avec-discernement |
| 2026-462, 456, 459, 450 | voir CSV étape 2 |
