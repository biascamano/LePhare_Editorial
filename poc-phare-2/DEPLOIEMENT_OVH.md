# Déploiement sur OVH Perso (test.le-phare.info)

Publication du POC statique dans un dossier dédié de l'hébergement OVH Perso, servi par le sous-domaine `test.le-phare.info`. WordPress (`www/`), sa base et le domaine principal ne sont pas touchés.

**État au 2026-11-03** : la simulation locale est validée (voir [TESTS.md](TESTS.md) §10). **Aucune connexion SFTP et aucun transfert n'ont eu lieu.** Le premier transfert attend l'accord explicite du fondateur sur la destination et les accès.

Voir aussi [SECURITE_DEPLOIEMENT.md](SECURITE_DEPLOIEMENT.md) et [RETOUR_ARRIERE.md](RETOUR_ARRIERE.md).

## 1. Principe

```
npm run build ─► dist/ ─► .deploy/lot/ (+ .htaccess, .htpasswd, marqueur, phare-version.txt)
                                 │  SFTP (WinSCP, clé d'hôte vérifiée)
                                 ▼
             <racine du compte OVH>/poc-phare-2/   ◄── multisite test.le-phare.info
             <racine du compte OVH>/www/           ◄── WordPress, jamais visé
```

| Mode | Commande | Réseau | Écrit à distance |
|---|---|---|---|
| Simulation (défaut) | `scripts\deploy-ovh.ps1` | aucun | non |
| Vérification distante | `-VerifierDistant` | SFTP, lecture seule | non |
| Premier déploiement | `-Executer -Initialiser -Confirmer poc-phare-2` | SFTP | oui, dossier POC seul |
| Mise à jour | `-Executer -Confirmer poc-phare-2` | SFTP | oui, après sauvegarde |
| Contrôle HTTPS | `-VerifierHttps` | HTTPS, GET | non |
| Restauration | `-Restaurer <dossier> [-Executer -Confirmer poc-phare-2]` | SFTP | oui avec `-Executer` |

Toutes les commandes se lancent depuis `poc-phare-2/`, dans Windows PowerShell 5.1 :
`powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 [options]`.
`-ExecutionPolicy Bypass` ne vaut que pour ce processus : la politique de la machine n'est pas modifiée.

## 2. Prérequis locaux

| Outil | État constaté | Action |
|---|---|---|
| Node 22.23.2, npm 11.3.0 | présents | — |
| Git 2.49 (fournit `openssl` et `ssh-keyscan`) | présent | — |
| Windows PowerShell 5.1 | présent (pas de PowerShell 7, inutile) | — |
| **WinSCP** (≥ 6.x, avec `WinSCPnet.dll`) | **absent** | à installer par le fondateur |

Installation de WinSCP (non lancée : elle modifie la machine) :

```powershell
winget install --id WinSCP.WinSCP --exact
```

L'installeur standard place `WinSCP.exe` et `WinSCPnet.dll` dans `C:\Program Files (x86)\WinSCP\`, où le script les cherche. Pour une version portable, renseigner `WINSCP_DIR`.

## 3. Côté OVH Manager (actions du fondateur)

Aucune n'est faite par le script.

**A. Multisite** : *Web Cloud > Hébergements > (hébergement de le-phare.info) > Multisite > Ajouter un domaine ou sous-domaine.*
- Domaine : `test.le-phare.info`.
- Dossier racine : `poc-phare-2`. OVH le crée s'il n'existe pas, au même niveau que `www`.
- SSL : cocher le certificat Let's Encrypt. Firewall et logs séparés au choix.
- L'ajout du sous-domaine crée un enregistrement DNS `test` dans la zone OVH. **C'est une modification DNS : décision du fondateur.** Ne toucher ni aux enregistrements du domaine principal ni aux MX.
- Attendre que le multisite soit « Activé » et que le SSL soit généré (quelques minutes à quelques heures).

**B. FTP - SSH** : *onglet FTP - SSH.*
- Vérifier que SFTP est activé.
- Relever le serveur (`ftp.clusterXXX.hosting.ovh.net`), le port (22) et le login.
- Recommandé : créer un **utilisateur FTP secondaire** dont le dossier racine est `/poc-phare-2`. Le script ne verrait alors rien d'autre (voir [SECURITE_DEPLOIEMENT.md](SECURITE_DEPLOIEMENT.md) §2). Dans ce cas, `OVH_REMOTE_DIR` doit tout de même désigner le dossier vu par ce compte : voir §8.

**C. Accès HTTP et noindex** : rien à faire dans le Manager. Le `.htaccess` déployé gère l'authentification Basic, l'en-tête `X-Robots-Tag` et la redirection HTTPS.

## 4. Clé d'hôte SSH (à faire avant toute connexion)

WinSCP refuse de se connecter si l'empreinte du serveur ne correspond pas à `OVH_SFTP_HOSTKEY`. Le script n'accepte ni `*` ni une clé inconnue.

1. Lire l'empreinte depuis Git Bash :
   ```bash
   ssh-keyscan -t ed25519 -p 22 ftp.clusterXXX.hosting.ovh.net 2>/dev/null | ssh-keygen -lf -
   # 256 SHA256:AbCd...xyz ftp.clusterXXX.hosting.ovh.net (ED25519)
   ```
2. **La recouper par un second chemin**, sans quoi le premier relevé peut lui-même être falsifié :
   - depuis un autre réseau (partage 4G par exemple) ;
   - ou en comparant avec l'empreinte affichée à la première connexion de l'interface WinSCP ;
   - ou avec celle de la documentation ou du support OVH du cluster.
3. La transcrire au format WinSCP, sans le préfixe `SHA256:` :
   `OVH_SFTP_HOSTKEY=ssh-ed25519 255 AbCd...xyz`
   Le format `ssh-ed25519 255 AbCd...xyz=` (avec `=` final) est aussi accepté par WinSCP.

Si OVH change la clé d'un cluster (migration), la connexion échoue : refaire les étapes 1 à 3. Ne jamais contourner l'échec.

## 5. Configuration locale

```powershell
Copy-Item .env.example .env.deploy   # puis compléter : hôte, utilisateur, clé d'hôte
```

`.env.deploy` est ignoré par git et ne doit **contenir aucun mot de passe** : le script s'arrête s'il y trouve une clé `PASSWORD`, `SECRET` ou `TOKEN`. Les variables d'environnement priment sur le fichier.

Secrets, stockés hors dépôt dans `%APPDATA%\LePhare-POC\`, chiffrés par DPAPI (lisibles par ce seul compte Windows sur cette machine) :

```powershell
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -EnregistrerIdentifiants   # login + mot de passe SFTP
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -CreerAccesHttp            # accès Basic au site de test
```

`-CreerAccesHttp` demande un identifiant et un mot de passe (12 caractères minimum, distinct du SFTP). Il en tire `htpasswd`, haché en apr1 par `openssl` sur l'entrée standard, donc jamais en argument. Il garde aussi une copie chiffrée qui sert aux contrôles HTTPS authentifiés.

Faute de fichier chiffré, le mot de passe SFTP est demandé au clavier, ou lu dans `OVH_SFTP_PASSWORD` pour la seule session.

## 6. Séquence du premier déploiement

À dérouler **seulement après accord explicite** du fondateur :

```powershell
# 1. Simulation (aucun réseau) : build, verify, lot, exclusions
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1

# 2. Lecture seule : connexion, clé d'hôte, inventaire de la racine, état du dossier cible
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -VerifierDistant

# 3. Premier transfert (dossier absent ou vide, sans marqueur)
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -Executer -Initialiser -Confirmer poc-phare-2
```

L'étape 3 refait les contrôles de l'étape 2, puis :
1. crée le dossier s'il est absent ;
2. envoie le marqueur, `.htpasswd` puis `.htaccess`, pour que l'accès soit protégé avant l'arrivée du contenu ;
3. synchronise le reste, sans aucune suppression ;
4. enchaîne `-VerifierHttps`.

Sans `-Confirmer`, le script demande de taper le nom du dossier.

Contrôles `-VerifierHttps` :
- `https://test.le-phare.info/` répond 401 sans identifiants, avec un certificat valide et l'en-tête `X-Robots-Tag: noindex` ;
- `http://` redirige vers `https://` sans demander d'identifiants ;
- avec identifiants : `/`, `/explorer/` et `/sentier/` répondent 200 et la version servie est celle du build ; `.htaccess`, `.htpasswd` et le marqueur répondent 403 ; une page inconnue répond 404 ;
- `https://le-phare.info/` répond toujours 200 et ne sert pas `phare-version.txt`.

## 7. Mises à jour

```powershell
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -VerifierDistant              # aperçu des fichiers à envoyer
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -Executer -Confirmer poc-phare-2
```

Avant chaque mise à jour, la version en ligne est copiée dans `.deploy\sauvegardes\<horodatage>\`. Les fichiers distants absents du nouveau build sont **conservés** et listés dans le journal (`ORPHELIN …`). Leur nettoyage est un chantier ultérieur, manuel et explicitement autorisé.

Options :
- `-Source wordpress` : build sur l'API publique ;
- `-SansBuild` : republier `dist/` tel quel ;
- `-JournalWinSCP` : journal de session WinSCP, où les mots de passe sont masqués ;
- `-SansAuthentification` : seulement si OVH refusait l'authentification Basic. Le site reste alors en `noindex`, mais public.

Chaque transfert ajoute une ligne à `.deploy\historique.csv` : horodatage, type, build, cible, sauvegarde.

## 8. Points à valider au premier déploiement

- **Chemin vu par SFTP.** OVH Perso présente en général la racine du compte comme `/homez.NNN/<login>`. Le script y ajoute `OVH_REMOTE_DIR`. Si le serveur montre `/` (compte chrooté, utilisateur secondaire par exemple), renseigner `OVH_HOME_ABS` avec le chemin absolu réel. Il figure dans le Manager (*FTP - SSH > Répertoire*) ou se lit avec la commande `pwd` en SSH. Sinon le script refuse le transfert, car `AuthUserFile` serait faux.
- **Utilisateur secondaire restreint à `/poc-phare-2`.** Sa racine *est* le dossier du POC, alors que le script attend un sous-dossier. Deux possibilités, à trancher au premier `-VerifierDistant` :
  - restreindre l'utilisateur à la racine du compte et garder `OVH_REMOTE_DIR=poc-phare-2` ;
  - ou adapter le script : chantier non fait, à demander.
- **`.htaccess`.** Le gabarit `deploy/htaccess.template` suppose Apache 2.4 avec `mod_rewrite`, `mod_headers`, `mod_auth_basic` et les blocs `<If>`. C'est la configuration documentée des hébergements Perso, mais elle n'a pas été vérifiée sur ce compte. Si le site renvoie une erreur 500 après le transfert : voir [RETOUR_ARRIERE.md](RETOUR_ARRIERE.md) §3.
- **Page 404.** `ErrorDocument 404 /404.html` suppose que `test.le-phare.info` a bien `poc-phare-2/` pour racine.
- **SSL.** Si `-VerifierHttps` signale un certificat invalide, le certificat Let's Encrypt du multisite n'est pas encore généré. Attendre ; ne rien contourner.

## 9. Ce qui est envoyé

Uniquement le contenu de `dist/`, plus `.htaccess`, `.htpasswd`, `.phare-poc-marker` et `phare-version.txt`. Le lot est contrôlé avant tout transfert :
- **extensions autorisées** : `.html .css .js .svg .png .jpg .jpeg .webp .avif .gif .ico .txt .woff2 .xml .webmanifest` ;
- **motifs refusés** : `.env*`, `*.local.json`, `.cred`, `*.ps1`, `*.mjs`, `*.ts`, `*.md`, `*.astro`, `package*.json`, `node_modules`, `.git`, `*.map`, `wp-config` ;
- **taille** : 10 Mo au maximum par fichier.

Un seul fichier refusé arrête tout. État actuel : 57 fichiers, 1,2 Mo.

## 10. Informations OVH encore nécessaires

| Information | Où la trouver | Variable |
|---|---|---|
| Serveur SFTP | Manager > FTP - SSH | `OVH_SFTP_HOST` |
| Port (22 attendu) | idem | `OVH_SFTP_PORT` |
| Login (principal ou secondaire) | idem | `OVH_SFTP_USER` |
| Empreinte ed25519 du serveur, recoupée | §4 | `OVH_SFTP_HOSTKEY` |
| Confirmation du multisite `test.le-phare.info` → `poc-phare-2`, SSL actif | Manager > Multisite | `OVH_REMOTE_DIR` |
| Chemin absolu du compte, si SFTP chrooté | Manager > FTP - SSH | `OVH_HOME_ABS` |

Le mot de passe ne figure dans aucune de ces variables. Il se saisit uniquement via `-EnregistrerIdentifiants` ou au clavier.
