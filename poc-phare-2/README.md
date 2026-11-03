# POC Le Phare 2.0

Front public statique en Astro, qui lit le contenu du Phare **en lecture seule**. Ce prototype ne publie rien, ne modifie rien en ligne et ne touche à aucun fichier du dépôt hors de `poc-phare-2/`.

| Document | Contenu |
|---|---|
| [AUDIT_EXISTANT.md](AUDIT_EXISTANT.md) | Audit en lecture seule du dépôt et du site actuel |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Contrat de contenu, design system, choix et limites |
| [PLAN_INTEGRATION.md](PLAN_INTEGRATION.md) | Étapes après validation, impact sur l'orchestrateur, décisions ouvertes |
| [TESTS.md](TESTS.md) | Tests exécutés, avec leurs sorties réelles et les captures |
| [DEPLOIEMENT_OVH.md](DEPLOIEMENT_OVH.md) | Publication sur `test.le-phare.info` (OVH Perso, SFTP WinSCP) |
| [SECURITE_DEPLOIEMENT.md](SECURITE_DEPLOIEMENT.md) | Garde-fous du script de déploiement, risques résiduels |
| [RETOUR_ARRIERE.md](RETOUR_ARRIERE.md) | Restauration, coupure d'accès, retrait du POC |

## Prérequis

- Node ≥ 22.12 (testé avec 22.23.2). Aucune dépendance globale.
- `npm install` dans `poc-phare-2/` : les versions sont figées dans `package.json` (Astro 7.3.8, marked 18.1.1, @astrojs/check 0.9.10, TypeScript 6.0.3).

## Commandes

Toutes se lancent depuis `poc-phare-2/`.

| Commande | Rôle |
|---|---|
| `npm run mock` | Régénère `src/data/mock/corpus.json` à partir du dépôt, en lecture seule |
| `npm run dev` | Serveur de développement sur http://localhost:4321 |
| `npm run check` | Vérification TypeScript et Astro |
| `npm run build` | Construit le site statique dans `dist/` |
| `npm run preview` | Sert le contenu de `dist/` |
| `npm run verify` | Contrôle hors ligne de `dist/` : liens, métadonnées, structure, poids. Ajouter `-- dist-wp` pour un autre dossier |

## Variables d'environnement

| Variable | Valeurs | Défaut |
|---|---|---|
| `PHARE_SOURCE` | `mock`, ou `wordpress` (GET publics sur l'API REST, sans authentification) | `mock` |
| `PHARE_WP_URL` | Base WordPress | `https://le-phare.info` |
| `PHARE_SITE` | Origine du site construit (canonical, og:url) | `https://test.le-phare.info` |
| `ASTRO_TELEMETRY_DISABLED` | `1` désactive la télémétrie d'Astro pour la commande | — |

Astro envoie par défaut une télémétrie anonyme. Pour l'éviter sans toucher à la configuration globale, préfixez chaque commande : `ASTRO_TELEMETRY_DISABLED=1 npm run build`. Le premier `astro check` de la session a tourné télémétrie active (voir [TESTS.md](TESTS.md)). La commande `astro telemetry disable` existe, mais elle modifie un fichier utilisateur global : elle n'a pas été lancée.

Build sur le contenu en ligne, dans un dossier séparé :

```bash
PHARE_SOURCE=wordpress ASTRO_TELEMETRY_DISABLED=1 npx astro build --outDir dist-wp
node scripts/verify-dist.mjs dist-wp
```

## Déploiement

```powershell
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1                  # simulation, sans réseau
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -VerifierDistant # SFTP en lecture seule
```

Le transfert réel (`-Executer`) et ses prérequis (WinSCP, `.env.deploy`, clé d'hôte, identifiants) sont décrits dans [DEPLOIEMENT_OVH.md](DEPLOIEMENT_OVH.md). Premier transfert fait le 2026-11-03 vers test.le-phare.info (version `20261103-100047-6ccee18-mock`). La nouvelle orientation (accueil, Explorer, Sentier, Le Phare, article) est en ligne depuis la version `20261103-120254-6ccee18-mock` ; le CSS orphelin de la version précédente (`_astro/Base.CL8Kpbk1.css`) a été supprimé à la main, sur autorisation explicite.

## Ce que le POC n'est pas

- Il ne remplace pas le site. Toutes les pages portent `noindex`, et les canonicals pointent vers `PHARE_SITE` (le site de test).
- Il n'a ni images, ni commentaires, ni newsletter, ni analytics.
- Il ne modifie pas `tools/phare.py` ni les routines (voir [PLAN_INTEGRATION.md](PLAN_INTEGRATION.md)).
