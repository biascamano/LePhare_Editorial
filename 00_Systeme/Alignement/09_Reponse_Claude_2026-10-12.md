# Proposition : routine unique `routine phare`

Le Phare garde ses routines spécialisées. On y ajoute **un script qui décide sans appel IA**, **un registre compact** et **une skill d'aiguillage courte**. Aucun fichier n'a été modifié.

## 1. La commande

- `routine phare` (et `/routine-phare`) lance l'action prioritaire, une seule, puis s'arrête et donne un rapport.
- `routine phare — état` affiche la décision sans rien lancer.
- `routine phare — reporter <activité>` permet au fondateur de reporter une activité.
- `routine phare — à blanc` est le mode test (voir §8).

À chaque lancement :
1. La skill appelle `python tools/phare.py next`. Ce script détermine l'état et la prochaine action, sans IA.
2. La skill exécute la skill spécialisée correspondante : quotidienne, rénovation, hebdomadaire ou mensuelle. Celles-ci restent inchangées pour l'essentiel.
3. En fin de séance, la skill appelle `phare.py close …`.

Je recommande **une conversation par lancement**, pour éviter la saturation du contexte.

## 2. Fichiers réutilisés

| Besoin | Source existante | Fiable ? |
|---|---|---|
| Articles du jour, état réel | `index_editorial.csv` : `Statut` passe de `brouillon` (local) à `wp_draft` puis `publie`, plus `Date_publication_WP` | Oui : ce statut est écrit par `wp_push_draft` et `post_linking` |
| Questions publiées | index (`Tags_WP` contient `type-question`) et mémoire §1 (colonne Type) | Oui |
| Regard curiosité | mémoire §1 (`Actualité — curiosité`, lot 1) | Oui, mais seulement pour les articles publiés |
| Rattrapages | index, `Remarques` = `Rénové … YYYY-MM-DD` | Partiel : pas de trace pour les « Contextualiser » ou les échecs |
| Dernier Fil | index : `SYNTHESE` dans `06_Syntheses/Fil_du_Phare`, statut `publie` | Oui |
| Consolidation mensuelle | `06_Syntheses/Rapports_mensuels/YYYY-MM.md` et mémoire §4 (« Mois ») | Partiel |
| Problèmes en cours | `Signalements_renovation.md` (ouverts), compteur du Radar, brouillons `wp_draft` | Oui, à titre d'information |
| Anti-doublon WP | `wp_push_draft.resolve_existing_post_id` (recherche par slug, puis mise à jour du post existant), garde-fou de `daily_run` | Oui |

## 3. Données manquantes

- **Séances sans article publié** (brouillon, bloqué, curiosité sans ancrage) : aucune source structurée aujourd'hui. Les blocs de trace sont en prose.
- **Séance en cours ou interrompue** : rien ne l'indique. Le log `daily_run_YYYY-MM-DD.json` est **écrasé** à chaque run du jour, donc inutilisable dès la deuxième séance.
- **Rétros hebdomadaires et mensuelles terminées** : il n'en existe aucune.
- **Actions décidées par une rétro et encore ouvertes** : nulle part.

D'où un seul ajout : **`00_Systeme/Journal_phare.csv`**, une ligne par séance (6 au plus par jour, environ 2 000 lignes par an).

```
date;periode;activite;statut;ids;debut;fin;note
2026-10-13;2026-10-13;generale;publie;2026-567;09:02;09:41;
2026-10-13;2026-10-13;curiosite;termine_sans_publication;;10:05;10:20;aucun ancrage du jour (C3, C7)
2026-10-19;2026-S42;retro_hebdo;termine;;08:30;08:55;
```

- `activite` prend l'une de ces valeurs : `generale` · `curiosite` · `question` · `rattrapage` · `fil` · `retro_hebdo` · `consolidation_mensuelle` · `retro_mensuelle`.
- Le journal sert au script. La prose reste dans les traces de `Retros/`.
- Les actions ouvertes d'une rétro vont dans un tableau `| Action | Échéance | Statut |` en fin de rétro. Le script compte les lignes non closes et les affiche.

## 4. Priorités : une action par lancement, la première due

0. **Reprise** : une séance `en_cours` interrompue (voir §7).
1. **Rétro hebdomadaire** de la semaine ISO précédente, si elle est terminée et que sa rétro n'est pas `terminé`.
2. **Rétro mensuelle** du mois précédent, s'il est terminé, **après** la rétro hebdomadaire de la semaine qui le chevauche.
3. **Consolidation mensuelle** : routine mensuelle actuelle, due du 1er au 7 du mois.
4. **Fil du Phare** : du vendredi au dimanche, s'il n'y a pas encore de Fil cette semaine et s'il y a au moins 4 articles publiés depuis le dernier Fil. La routine peut clore en `reporte` si aucune vraie connexion n'apparaît.
5. Puis les objectifs quotidiens, dans l'ordre :
   1. actualité générale ;
   2. actualité de curiosité ;
   3. Question du Phare ;
   4. rattrapage.

Un objectif est **traité** pour la période dès qu'une ligne existe avec l'un de ces statuts : publié, brouillon, bloqué, terminé sans publication ou reporté. Il n'est alors jamais relancé. Si tout est traité, le script répond : **« Aucune action obligatoire en attente pour cette période. »** Il suggère au plus une action facultative (P1 à échéance, signalement ouvert…) sans la lancer.

## 5. Statuts

| Statut | Sens | Écrit quand |
|---|---|---|
| à faire | calculé, jamais écrit | — |
| `en_cours` | séance démarrée, sert aussi de verrou | `phare.py start` |
| `publie` | publié **et vérifié** | `close`, accepté seulement si l'index dit `publie` pour tous les IDs |
| `brouillon` | contrôle = BROUILLON, l'article existe en brouillon WP | `close`, si l'index dit `wp_draft` |
| `termine_sans_publication` | séance menée à bien sans article (pas d'ancrage, pas de sujet au niveau) ; rétros et consolidation | `close` |
| `bloque` | échec technique ou besoin d'un humain, deux tentatives au plus | `close` ou reprise |
| `reporte` | report délibéré (conditions non réunies, décision du fondateur) | `close` ou `reporter` |

## 6. Déclenchement et clôture

- **Rétro hebdomadaire**
  - Déclenchement : la semaine ISO est terminée (lundi 00:00) et il n'y a pas de ligne `retro_hebdo` `termine` pour cette semaine.
  - Clôture : `## Rétro` du fichier `YYYY-Snn.md` est rempli, puis `close termine`.
  - Le script vérifie que la section n'est pas vide. Le fichier seul ne suffit pas.
  - Elle absorbe le **comité du Radar et l'audit des fils**, qui sont dus chaque semaine. L'hebdomadaire actuelle se réduit alors au **Fil**, qui est conditionnel.
- **Rétro mensuelle**
  - Déclenchement : le mois est terminé et sa rétro n'est pas `terminé`.
  - Le script lui fournit les rétros hebdomadaires qui chevauchent le mois, plus les **dates sans rétro couverte**, tirées du journal et de l'index.
  - Clôture : `YYYY-MM_retro_mensuelle.md` rempli.
- **Quotidiennes** : clôture avec le statut issu du contrôle prépublication et de `verify_publication`.
- **Date et fuseau** : date locale de la machine, semaines ISO (lundi à dimanche), mois civil.

## 7. Panne et interruption

- **Verrou** : `start` écrit `en_cours`. Si un deuxième lancement trouve une ligne `en_cours` de moins de 2 h, il annonce « séance en cours » et passe à l'action suivante. Cela évite qu'une même production soit lancée deux fois en parallèle.
- **Reprise d'une ligne `en_cours` ancienne**, selon l'état réel de l'ID :
  - pas d'ID : rien n'a été créé, on relance la même activité **une fois** ;
  - ID `brouillon` (local) : reprise à `stage` et au contrôle, **jamais de nouveau `create`** ;
  - ID `wp_draft` sans décision BROUILLON : on relance `daily_run --force` sur le même dossier de transit (`--keep-publish-folder`). Le post est retrouvé par son slug, donc pas de doublon ;
  - ID `publie` : on termine les étapes 10 et 11 (mémoire, Radar, vérification), puis `close publie`.
- **Erreur réseau** : la ligne reste `en_cours` avec une note. Au deuxième échec, elle passe en `bloque` : le script passe à la suite et la rétro la reprend.

## 8. Tests sans WordPress

1. **Tests de décision, hors ligne** : `phare.py next --date 2026-10-18 --journal <fixture>`, sur une dizaine de scénarios (lundi avec rétro due, 1er du mois, journée complète, interruption avec ID `wp_draft`, verrou, Fil sans assez d'articles…). Ils sont déterministes et ne coûtent aucun appel IA.
2. **`routine phare — à blanc`** : décision, rédaction, `stage` et contrôle avec relecteur, **sans `daily_run`**, dans un worktree git que l'on jette ensuite. En effet, `new_article create` écrit déjà une ligne dans l'index.
3. Ensuite seulement, une vraie journée en `brouillons seulement`.

## 9. Coût

- **Tokens** : `phare.py next` renvoie environ 15 lignes. L'aiguillage coûte environ 1 à 2 k tokens par lancement. La séance elle-même coûte ce qu'elle coûte aujourd'hui. Rien ne demande à l'IA de relire l'état pour décider.
- **Maintenance** :
  - un script d'environ 200 lignes ;
  - une skill d'environ 50 lignes ;
  - un CSV ;
  - les fixtures de test ;
  - une ligne `start`/`close` ajoutée à chaque skill spécialisée.

## 10. Simplifications possibles

- Fondre le **comité Radar et l'audit des fils** dans la rétro hebdomadaire, et le **rapport mensuel et le cap** dans la rétro mensuelle. On évite deux bilans de la même période.
- La **trace de séance** en prose devient facultative pour les rubriques déjà dans le journal (activité, statut, IDs). Elle ne garde que les raisons, les contrôles et les questions ouvertes.
- Les **objectifs quotidiens sont des plafonds, pas des quotas** : une liste réglable dans `phare.py` (par exemple pas de curiosité le dimanche, rattrapage seulement 3 jours sur 7). On évite le remplissage de cases.

## Décisions à prendre

1. **Point de départ des rétros.** Nous sommes lundi 12 octobre (S42). Le script exigerait aussitôt la rétro de S41 et la rétro mensuelle de septembre, sans traces pour les nourrir. Je propose de démarrer les rétros avec le pilote : première rétro hebdomadaire S42 le 19 octobre, première rétro mensuelle (octobre) début novembre.
2. Garder les **quatre objectifs quotidiens chaque jour**, ou adopter un rythme réglable.
3. Valider les deux fusions (rétro hebdomadaire avec comité Radar et fils ; rétro mensuelle avec rapport mensuel).
4. Valider la **fenêtre du Fil** : du vendredi au dimanche, avec au moins 4 articles.

À l'implémentation, je peux enregistrer ce message et cette réponse dans `00_Systeme/Alignement/` (09).
