# Retour arrière

Le POC vit dans `<racine du compte>/poc-phare-2/`. Aucun retour arrière ne concerne WordPress : `www/` et la base ne sont jamais modifiés. Le pire cas reste un sous-domaine de test cassé.

## 1. Revenir à la version précédente

Chaque mise à jour sauvegarde d'abord la version en ligne dans `.deploy\sauvegardes\<horodatage>\`. La correspondance entre horodatage et build se lit dans `.deploy\historique.csv`.

```powershell
Get-Content .deploy\historique.csv -Tail 5
# 20261110-091500;deploiement;20261110-091458-abc1234-mock;/homez.NNN/login/poc-phare-2;D:\...\.deploy\sauvegardes\20261110-091500

# Simulation : contrôle du lot et aperçu, sans écriture
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -Restaurer .deploy\sauvegardes\20261110-091500 -VerifierDistant

# Restauration réelle (le dossier distant doit porter le marqueur du POC)
powershell -ExecutionPolicy Bypass -File scripts\deploy-ovh.ps1 -Restaurer .deploy\sauvegardes\20261110-091500 -Executer -Confirmer poc-phare-2
```

La restauration :
- réenvoie les fichiers de la sauvegarde, `.htaccess` et `.htpasswd` compris, et remet `phare-version.txt` à sa valeur d'alors ;
- sauvegarde d'abord l'état présent, ce qui la rend elle-même réversible ;
- ne supprime rien : les fichiers ajoutés depuis restent en place (protégés), à retirer à la main si besoin.

Autre voie, plus simple quand le dépôt n'a pas bougé : reconstruire un commit antérieur, puis `-Executer -Confirmer poc-phare-2`.

## 2. Couper l'accès immédiatement

Par ordre de préférence, depuis l'interface WinSCP ou le gestionnaire FTP d'OVH :

1. **Manager OVH > Multisite** : désactiver ou supprimer l'entrée `test.le-phare.info`. Le dossier reste intact ; le sous-domaine ne sert plus rien.
2. Remplacer `poc-phare-2/.htaccess` par une seule ligne `Require all denied` : tout répond 403.
3. Renommer `poc-phare-2/index.html` : il reste l'authentification et le 404.

Ces actions sont manuelles : le script ne les automatise pas, par choix.

## 3. Erreur 500 après le premier déploiement

C'est presque toujours une directive `.htaccess` refusée par Apache (DEPLOIEMENT_OVH.md §8). Elle ne touche que `test.le-phare.info`.

1. Lire le journal d'erreurs Apache du multisite : Manager > Statistiques et logs.
2. Corriger `deploy/htaccess.template` en local. Pistes :
   - retirer le bloc `<If>` et garder les directives `Auth*` seules ;
   - vérifier le chemin `AuthUserFile` (`OVH_HOME_ABS`).
3. Relancer `-Executer -Confirmer poc-phare-2`. Le `.htaccess` est régénéré et renvoyé à chaque fois.

En urgence, la seule ligne `Require all denied` (§2) remet le sous-domaine dans un état sain.

## 4. Retirer complètement le POC

Hors périmètre du script, qui ne supprime jamais rien. À faire à la main, après décision du fondateur :

1. Manager OVH > Multisite : supprimer `test.le-phare.info`. Supprimer aussi l'enregistrement DNS `test` s'il a été créé, ce qui est une modification DNS.
2. Supprimer le dossier `poc-phare-2/` par SFTP, après avoir vérifié qu'il contient bien `.phare-poc-marker`.
3. Locales : `.deploy\` (journaux, sauvegardes) et `%APPDATA%\LePhare-POC\` (secrets chiffrés).
4. Changer le mot de passe SFTP s'il a été saisi sur un poste partagé, et supprimer l'utilisateur FTP secondaire s'il a été créé.
