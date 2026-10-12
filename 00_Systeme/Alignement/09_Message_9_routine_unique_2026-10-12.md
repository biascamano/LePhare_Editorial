# LE PHARE INFO — ÉVOLUTION VERS UNE ROUTINE UNIQUE

Claude,

Nous souhaitons simplifier radicalement le pilotage quotidien du Phare.

**Le fondateur veut disposer d'une seule commande : `routine phare`.**

Lorsqu'elle est lancée, elle examine automatiquement ce qui a été effectué et choisit la prochaine routine pertinente.

Nous ne voulons plus sélectionner manuellement entre :
- Actualité générale.
- Actualité de curiosité.
- Question du Phare.
- Rattrapage.
- Fil du Phare.
- Rétrospective hebdomadaire.
- Consolidation et rétrospective mensuelle.

## 1. Principe

Une seule porte d'entrée, mais conservation des routines spécialisées en interne.

Ne construis pas un système monolithique.

Privilégie un orchestrateur léger qui réutilise les skills et scripts existants.

## 2. Examiner l'état réel avant toute décision

À chaque lancement, déterminer :

- La date locale et la période éditoriale.
- Les articles déjà publiés aujourd'hui.
- Leur regard : général ou curiosité.
- Les Questions du Phare déjà publiées.
- Les rattrapages déjà effectués.
- Les articles bloqués ou laissés en brouillon.
- La date du dernier Fil du Phare.
- La date de la dernière rétro hebdomadaire.
- La période couverte par la dernière rétro mensuelle.
- Les décisions et actions encore en attente.
- Les éventuels contrôles ou problèmes prioritaires.

Ne pas déduire une exécution réussie de la seule existence d'un fichier.

Vérifier les statuts et résultats pertinents.

## 3. Sélectionner une seule prochaine action

À chaque lancement, sélectionner l'action prioritaire restant à effectuer.

Objectifs quotidiens :
1. Une actualité générale.
2. Une actualité de curiosité.
3. Une Question du Phare.
4. Une action de rattrapage ou d'approfondissement.

Objectifs hebdomadaires :
5. Le Fil du Phare, lorsque les conditions éditoriales sont réunies.
6. Une rétrospective éditoriale interne.

Objectifs mensuels :
7. La consolidation du patrimoine.
8. Une rétrospective stratégique interne.

Une rétro due peut devenir prioritaire sur la production quotidienne lorsqu'elle doit examiner une période terminée.

Ne pas confondre un objectif de publication avec une obligation de publier un contenu non conforme.

## 4. Éviter les doublons et les boucles

Une action effectuée avec succès ne doit pas être sélectionnée de nouveau pour la même période.

Une action bloquée ne doit pas relancer automatiquement la même production.

Un article en brouillon doit être enregistré comme travail effectué mais non publié, avec un statut approprié.

La routine doit pouvoir répondre :

**« Aucune action obligatoire en attente pour cette période. »**

Elle peut alors suggérer une action facultative, sans la lancer automatiquement.

## 5. Contrôle prépublication

Tous les articles, quelle que soit leur origine, passent le contrôle de qualité déjà décidé :

- Respect des droits humains et des personnes.
- Absence de propos discriminatoires non contextualisés.
- Vérification factuelle.
- Contrôle des citations.
- Liens internes et externes.
- Propriété intellectuelle.
- Conformité éditoriale.

Issues : PUBLIER, CORRIGER puis revérifier, ou BROUILLON et signalement.

Le contrôle porte sur le texte final. Les modifications effectuées ensuite par le maillage automatique doivent être couvertes par les vérifications techniques existantes.

## 6. Pilotage des rétrospectives

Les rétrospectives doivent être des activités prioritaires de l'orchestrateur.

### Rétro hebdomadaire

Déclenchée lorsque la période hebdomadaire précédente est terminée et que le bilan correspondant n'existe pas encore.

Elle examine :
- Les actualités générales.
- Les actualités de curiosité.
- Les Questions du Phare.
- Les rattrapages.
- Les contrôles qualité.
- Les apprentissages.
- Les erreurs et angles morts.
- Les décisions précédentes.
- Les nouvelles actions prioritaires.

Elle est distincte du Fil du Phare.

### Rétro mensuelle

Déclenchée lorsque le mois précédent est terminé et que sa rétrospective n'a pas été réalisée.

Elle examine :
- La cohérence du média.
- Les progrès du patrimoine.
- La qualité éditoriale.
- La diversité des analyses.
- L'évolution des intérêts intellectuels du fondateur.
- Les dossiers et le Sentier.
- Le fonctionnement technique.
- Les décisions du mois précédent et leurs effets.
- Les orientations du mois suivant.

La rétro mensuelle doit utiliser les bilans hebdomadaires existants sans ignorer les journées qui ne seraient couvertes par aucun bilan.

## 7. Sobriété technique

La détermination de la prochaine action devrait être aussi déterministe que possible.

Éviter les appels IA pour vérifier simplement une date, un statut ou une activité déjà réalisée.

Réutiliser les structures existantes.

Prévoir la reprise après interruption, la prévention des doubles publications, les erreurs réseau et les exécutions successives.

Le registre de suivi doit rester compact.

## 8. Ce que nous attendons avant implémentation

Présente une proposition technique minimale précisant :

1. La commande unique proposée.
2. Les fichiers existants réutilisés.
3. Les éventuelles données manquantes pour déterminer l'état.
4. Les règles de priorité entre quotidienne, hebdomadaire et mensuelle.
5. Les statuts nécessaires : à faire, en cours, publié, terminé sans publication, brouillon, bloqué, reporté.
6. Les conditions de déclenchement et de clôture.
7. Le fonctionnement en cas de panne ou d'interruption.
8. La façon de tester le système sans publier sur WordPress.
9. L'impact en tokens et en maintenance.
10. Les simplifications possibles.

Ne modifie aucun fichier à ce stade.

**Objectif : une seule commande, une seule décision de prochaine action, un système capable de savoir ce qui a été réalisé et ce qu'il reste à faire.**

L'orchestrateur doit servir la philosophie du Phare, et non transformer la publication en simple remplissage de cases.
