# Sécurité du déploiement

Menaces retenues, protections en place dans `scripts/deploy-ovh.ps1` et risques qui demeurent.

## 1. Garde-fous du script

| Risque | Protection |
|---|---|
| Écraser WordPress | Dossier distant = un seul segment `^[A-Za-z0-9][A-Za-z0-9._-]*$`, sans `/` ni `..`. Liste refusée : `www`, `public_html`, `htdocs`, `wordpress`, `wp`, `cgi-bin`, `private`, `logs`, `ovhconfig`. Refus si la cible contient `wp-config.php`, `wp-content`, `wp-admin`, `wp-includes`, `wp-login.php` ou `xmlrpc.php`. Refus si la cible est un lien symbolique |
| Écrire dans un dossier étranger | Mise à jour seulement si le marqueur `.phare-poc-marker` (`le-phare-2.0-poc`, `site=test.le-phare.info`) est présent et conforme. Premier déploiement seulement sur un dossier absent ou vide, avec `-Initialiser`. Dossier non vide sans marqueur : refus |
| Déploiement accidentel | Simulation par défaut. Le transfert exige `-Executer` **et** la confirmation du nom du dossier (`-Confirmer` ou saisie au clavier) |
| Suppression distante | Aucune : `SynchronizeDirectories(..., removeFiles = $false)`. Aucun appel `RemoveFiles`. Les orphelins sont seulement listés |
| Perte de la version en ligne | Sauvegarde intégrale du dossier distant avant chaque mise à jour ; transfert annulé si elle est incomplète (marqueur absent) |
| Usurpation du serveur (MITM) | `SshHostKeyFingerprint` obligatoire, format contrôlé, `*` refusé. `GiveUpSecurityAndAcceptAnySshHostKey` n'est jamais utilisé |
| Viser la production | `PHARE_SITE` doit être une origine HTTPS ; `le-phare.info` et `www.le-phare.info` sont refusés |
| Publier un secret ou une source | Liste blanche d'extensions et liste noire de motifs sur le lot ; un seul écart arrête tout (§9 de DEPLOIEMENT_OVH.md) |
| Mot de passe dans le dépôt | `.env.deploy` est ignoré par git et rejeté s'il contient une clé `PASSWORD`, `SECRET` ou `TOKEN`. Les secrets vivent dans `%APPDATA%\LePhare-POC\` (DPAPI) |
| Mot de passe dans les journaux | Le journal du script n'écrit ni mot de passe, ni hash, ni identifiant complet : l'utilisateur est masqué (`te***`). Le journal WinSCP est facultatif (`-JournalWinSCP`), et WinSCP y masque les mots de passe. Test : aucune occurrence d'un mot de passe factice dans `.deploy/` |
| Mot de passe HTTP intercepté | Authentification seulement en HTTPS (`<If "%{SERVER_PORT} == '443'">`) ; le HTTP redirige avant toute demande d'identifiants. Hash apr1 calculé localement, mot de passe transmis à `openssl` par l'entrée standard |
| Lecture des fichiers techniques | `RewriteRule (^|/)\.(ht|phare) - [F]` : `.htaccess`, `.htpasswd` et le marqueur répondent 403 (contrôlé par `-VerifierHttps`) |
| Indexation du site de test | `<meta name="robots" content="noindex, nofollow, noarchive">` sur chaque page (contrôlé par `verify`), en-tête `X-Robots-Tag` hors `IfModule`, pour qu'une absence de `mod_headers` se voie au lieu de passer en silence. Accès protégé par mot de passe |
| Contenu dupliqué avec le-phare.info | Canonical auto-référent sur `test.le-phare.info`, page en `noindex`. Pas de `robots.txt Disallow` : il empêcherait les robots de voir le `noindex` |

## 2. Limites et risques résiduels

1. **Le chemin n'est pas une frontière.** Avec le login principal OVH, le compte SFTP voit tout l'hébergement, y compris `www/` : un bug ou une mauvaise manipulation hors script pourrait l'atteindre. Le script réduit ce risque, il ne l'annule pas. **Recommandation** : un utilisateur FTP secondaire limité à `/poc-phare-2` (DEPLOIEMENT_OVH.md §3 B et §8).
2. **Confiance au premier relevé (TOFU).** L'empreinte de la clé d'hôte n'est sûre que si elle a été recoupée par un second chemin (DEPLOIEMENT_OVH.md §4).
3. **Mot de passe partagé.** Le login SFTP principal est aussi celui de l'hébergement WordPress. Sa compromission locale (poste Windows) exposerait le site de production. DPAPI protège contre la lecture du fichier par un autre compte ou sur une autre machine, pas contre un logiciel malveillant exécuté sous la session de l'utilisateur.
4. **Basic Auth.** Elle protège un prototype ; elle ne protège pas des données sensibles. Le contenu du POC est de toute façon public sur le-phare.info.
5. **`.htaccess` non éprouvé.** Le gabarit n'a pas encore tourné sur ce compte OVH. Une directive refusée provoque une erreur 500, sur `test.le-phare.info` seulement, jamais sur `www`.
6. **Fichiers orphelins.** Sans suppression, une page retirée du build reste en ligne (protégée par l'authentification) jusqu'à un nettoyage manuel.
7. **Ordre du premier transfert.** Le marqueur, `.htpasswd` et `.htaccess` partent avant le contenu. Une coupure entre ces envois et la synchronisation laisse un site partiel, mais protégé. Relancer suffit.
8. **Intégrité du lot.** Le lot est reconstruit à chaque exécution depuis `dist/` ; un `node_modules` compromis pourrait injecter du contenu dans le build. Atténuation : versions figées, `npm audit` (0 vulnérabilité), contrôle `verify` qui refuse tout script ou image externe.
9. **WinSCP lui-même.** Il faudra le tenir à jour, car c'est un composant exécuté avec le mot de passe en mémoire.

## 3. Ce que le script ne fait jamais

- Toucher `www/`, la base de données, les DNS, le Manager OVH ou `.ovhconfig`.
- Supprimer un fichier distant.
- Accepter une clé d'hôte inconnue.
- Lire `tools/wp_config.local.json`, `tools/editorial_config.local.json` ou tout autre fichier du dépôt hors de `poc-phare-2/`.
- Envoyer autre chose que des requêtes GET au contrôle HTTPS.
