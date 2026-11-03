# Tests

Tests exécutés le 2026-11-03 sur Windows 10, avec Node 22.23.2 et Chrome headless. Les sorties ci-dessous sont copiées des exécutions réelles, éventuellement abrégées. Chaque commande est préfixée par `ASTRO_TELEMETRY_DISABLED=1`, sauf la toute première exécution d'`astro check` de la session.

## 1. Types et build (mode mock)

```
$ npx astro check
- 0 errors
- 0 warnings
- 0 hints

$ npx astro build
[build] 52 page(s) built in 478ms
[build] Complete!
```

## 2. Contrôle du site produit (`npm run verify`)

`scripts/verify-dist.mjs` contrôle, hors ligne, chaque page de `dist/` :
- `lang="fr"`, `title` et une description d'au moins 50 caractères ;
- un canonical sur `PHARE_SITE` (`https://test.le-phare.info/…/`), une meta `robots` noindex, un seul h1 et `main#contenu` ;
- des ressources locales (`src`, `link href`) présentes dans `dist/`, aucune image ni aucun script externe ;
- aucune astérisque Markdown visible, aucune `img` sans `alt`, aucun id dupliqué ;
- des ancres internes résolues et des liens internes existants, terminés par un slash.

```
52 pages, 748 liens internes, 504 liens externes (non testés : hors ligne)
Pages les plus lourdes (HTML, Ko brut / gzip) :
  134.5 / 28.9  /explorer/index.html
  43.7 / 9.5  /sentier/index.html
  29.2 / 8.7  /fil-du-phare-qui-a-les-moyens-de-verifier-ce-qu-on-nous-affirme/index.html
Médiane HTML : 20.6 Ko
Assets JS/CSS (Ko brut / gzip) :
  4.6 / 1.7  _astro\Base.CL8Kpbk1.css
Pages avec un script exécutable : /explorer/index.html

OK : aucune erreur.
```

Les premières exécutions ont relevé des erreurs, toutes corrigées depuis :

| Erreur | Correction |
|---|---|
| Faux positif sur `lang` | Expression régulière corrigée |
| Faux positif sur le canonical racine | Expression régulière corrigée |
| Description de la 404 trop courte | Description réécrite |
| Id `questions-ouvertes` dupliqué dans Explorer | Titre renommé `t-questions-ouvertes` |

## 3. Mode wordpress (API publique, GET uniquement)

```
$ PHARE_SOURCE=wordpress npx astro build --outDir dist-wp     → 290 pages, ~10,6 s
$ node scripts/verify-dist.mjs dist-wp
290 pages, 2549 liens internes, 1179 liens externes (non testés : hors ligne)
  410.0 / 74.2  /explorer/index.html
Médiane HTML : 22.9 Ko
132 erreur(s)
```

Les 132 erreurs se répartissent ainsi : 92 pages avec des astérisques visibles, 25 pages avec plusieurs h1 et 15 ancres `href="#"`. Toutes viennent du **contenu publié** : elles sont présentes telles quelles dans `content.rendered`. Le détail est dans AUDIT_EXISTANT.md §6.

Le premier build a échoué sur `NoMatchingStaticPathFound`, à cause d'un slug encodé en pourcents (`…iv%e1%b5%89-republique…`). La correction est un `decodeURIComponent` dans le provider. Aucune requête autre que GET n'a été émise, et aucune authentification n'a été utilisée.

## 4. Navigation et lecture sans JavaScript

- **Explorer avec JS** (version initiale) : `?famille=dossiers` affiche « 1 article affiché ». La recherche, les sélecteurs et l'URL (`replaceState`) restent synchronisés. Depuis la nouvelle orientation, les paramètres sont `q`, `theme`, `format`, `tri`, `porte` et `page` (12 par page) ; à recontrôler dans un navigateur.
- **Nouvelle orientation (2026-11-03, mock)** : `check` 0 erreur, build de 53 pages, `verify` sans erreur. Sur 48 articles : « L'essentiel en deux minutes », Transparence et Poursuivre sur 48, double circulation sur 37, Toutes les références sur 47. Pas encore contrôlé visuellement (desktop ou mobile).
- **Explorer sans JS** : capture faite avec un profil Chrome qui bloque JS (`Preferences` → `javascript: 2`).
  - Les 97 éléments sont listés, aucun masqué, aucune section masquée.
  - Le compteur reste vide.
  - Le formulaire reste un GET classique.
- **Article** :
  - aucun script exécutable, hors JSON-LD ;
  - le corps, les Repères de sources (dans un `<details>`), Pour aller plus loin et Sur le Sentier du Savoir sont présents dans le HTML.
- **Liens** : les 748 liens internes résolvent vers une page du build (§2).

## 5. Affichage desktop et mobile

| Capture | Contenu |
|---|---|
| [accueil-1366.png](tests/captures/accueil-1366.png) | Accueil, deux portes |
| [article-1366.png](tests/captures/article-1366.png) | Article : chapeau, L'essentiel, Les questions, sommaire |
| [explorer-filtre-1366.png](tests/captures/explorer-filtre-1366.png) | Explorer filtré, avec JS |
| [explorer-sans-js-1366.png](tests/captures/explorer-sans-js-1366.png) | Explorer sans JS |
| [mobile-360-390.png](tests/captures/mobile-360-390.png) | Accueil à 360 px, article et Sentier à 390 px |

Chrome headless sous Windows impose une largeur minimale d'environ 500 px : une capture directe à 390 px est donc tronquée à tort. Les largeurs mobiles ont été rendues dans des iframes de 360 et 390 px, au sein d'une page harnais. Aucun débordement horizontal n'est apparu.

## 6. Accessibilité

Contrastes calculés par script (formule WCAG 2.x) sur tous les couples de jetons utilisés ; le tableau est dans ARCHITECTURE.md §3. Deux défauts ont été trouvés et corrigés :

| Défaut | Ratio | Correction |
|---|---|---|
| Anneau de focus ambre sur papier | 2,07 | Contour encre doublé d'un halo ambre |
| Pastille d'étape du Sentier ouverte, blanc sur teal | 4,10 | Papier sur teal-ink |

Contrôlés par lecture du HTML produit :
- lien d'évitement, landmarks et un seul h1 (aussi vérifié par `verify`) ;
- labels associés aux champs, `aria-live` sur le compteur, `alt` sur les images (il n'y en a aucune) ;
- cibles d'au moins 44 px.

## 7. Aucun fichier existant modifié

```
$ find <dépôt> -path .git -prune -o -path poc-phare-2 -prune -o -type f -newermt "2026-11-01 00:00" -print | wc -l
0
```

`git status` montre bien des fichiers modifiés ou non suivis hors du POC. Tous datent d'avant cette session :
- logs `daily_run` du 26 et du 29/10 ;
- articles 577–579 et 07_A_Publier ;
- rétros S44 ;
- 09_Livres V7.

Il n'y a eu aucun commit (le dernier date du 2026-10-26) ni aucun push.

## 8. Dépendances

```
$ npm audit
found 0 vulnerabilities
```

Les versions ont été vérifiées avant l'installation : Astro 7.4.5 exige Node ≥ 22.23.4, d'où le choix de 7.3.8. Rien n'a été installé globalement. `node_modules` pèse 209 Mo, `dist` 1,4 Mo et `dist-wp` 8,1 Mo, tous hors git.

## 9. Non testé

- Liens externes : 504 en mock, 1179 en wordpress, aucun requêté.
- Lecteur d'écran réel (NVDA, VoiceOver) et parcours complet au clavier : seul le focus visible a été vérifié, par CSS et par contraste.
- Lighthouse et Core Web Vitals mesurés.
- Navigateurs autres que Chrome, et appareils mobiles physiques.
- Charge et hébergement : rien n'a été déployé.
- Connexion SFTP, `-VerifierDistant`, `-Executer`, `-Restaurer` avec `-Executer`, `-VerifierHttps`, `-EnregistrerIdentifiants` et `-CreerAccesHttp` : WinSCP est absent, aucun paramètre OVH n'est connu et aucun transfert n'est autorisé.

## 10. Script de déploiement (simulation, 2026-11-03)

Windows PowerShell 5.1.19041. Le script est enregistré en UTF-8 avec BOM, sans quoi PowerShell 5.1 lit les accents en ANSI.

```
$ Parser::ParseFile(scripts\deploy-ovh.ps1)            → PARSE OK
$ powershell -File scripts\deploy-ovh.ps1               (simulation, aucune config OVH)
[ATTENTION] Paramètres SFTP encore inconnus (Hote, Utilisateur, CleHote) : sans effet en simulation.
[build] 52 page(s) built in 517ms
52 pages, 748 liens internes, 504 liens externes (non testés : hors ligne), 104 références de ressources locales
[OK]   verify-dist : aucune erreur.
[ATTENTION] Fichier htpasswd absent (...\AppData\Roaming\LePhare-POC\htpasswd) : lancer -CreerAccesHttp avant tout transfert réel.
[OK]   57 fichiers, 1,2 Mo ; liste d'exclusion respectée.   (52 .html, 1 .css, 1 .svg, 1 .txt, marqueur, .htaccess)
[OK] SIMULATION terminée : aucune connexion, aucun transfert.   → code 0
```

Cas de refus, tous en code 1 et sans connexion :

| # | Entrée | Résultat |
|---|---|---|
| 1 | `-VerifierDistant` sans configuration | « Paramètres SFTP manquants : Hote, Utilisateur, CleHote » |
| 2 | `OVH_REMOTE_DIR=www` | « Dossier distant interdit » |
| 3 | `OVH_REMOTE_DIR=../www` | « doit être un seul nom de dossier… sans / ni .. » |
| 4 | `OVH_SFTP_HOSTKEY=*` | « Aucune acceptation automatique de clé n'est permise » |
| 5 | `PHARE_SITE=https://le-phare.info` | « vise le site de production : interdit » |
| 6 | `-Executer -Initialiser -Confirmer poc-phare-2`, hôte fictif | utilisateur affiché masqué (`te***`), arrêt « WinSCP introuvable » avant toute connexion |
| 7 | `-Restaurer D:\workspaces` | « attend un dossier de .deploy\sauvegardes contenant le marqueur » |
| 8 | `.env.deploy` contenant `OVH_SFTP_PASSWORD=…` | « contient une clé de secret » ; la valeur n'apparaît dans aucun fichier de `.deploy/` |
| 9 | `config.local.json` et `notes.md` ajoutés dans `dist/` | « 2 fichier(s) ne doivent pas être publiés » |
| 10 | `-SansAuthentification` | `.htaccess` sans aucune directive `Auth*` |

Le `.htaccess` produit dans `.deploy/lot/` est conforme au gabarit. `AuthUserFile` vaut `<HOME_OVH>/poc-phare-2/.htpasswd` en simulation ; le chemin réel est résolu à la connexion, ou exigé via `OVH_HOME_ABS` si la racine SFTP est chrootée. Les fichiers de test temporaires (`.env.deploy`, fichiers ajoutés à `dist/`) ont été supprimés. Aucun fichier du dépôt hors de `poc-phare-2/` n'est plus récent que le début du POC (`find -newer package.json` : 0).
