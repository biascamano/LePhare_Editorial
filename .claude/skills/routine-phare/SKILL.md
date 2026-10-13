---
name: routine-phare
description: L'Orchestrateur du Phare — porte d'entrée unique. Demande à tools/phare.py la prochaine action (rétro, consolidation, Fil, objectif quotidien, reprise), l'ouvre dans le journal, l'exécute avec la routine spécialisée et la clôt avec son statut réel. Une seule activité par lancement. Déclenché par « routine phare » ou /routine-phare.
---

# Routine phare — l'orchestrateur

**Une commande, plusieurs routines spécialisées, une décision déterministe** (`plan.md` D22). La décision appartient à `tools/phare.py`, pas au jugement de la séance. Le jugement éditorial reste dans les routines spécialisées.

## Variantes du prompt

- `routine phare` : la prochaine action, exécutée jusqu'au bout.
- `routine phare — état` : `next` seulement, sans rien lancer.
- `routine phare — reprendre` : `next --reprendre` (une séance « active » est en réalité interrompue).
- `routine phare — reporter <activité> : <motif>` : décision du fondateur, `python tools/phare.py reporter <activité> --note "<motif>"`, puis `next`.
- `routine phare — brouillons seulement` : voir « Mode brouillons » ci-dessous. **Automatique tant que `00_Systeme/Mode_brouillons.md` existe** (`next` l'annonce), même si le prompt ne le dit pas.
- `routine phare — bilan pilote [<jour>]` : bilan de la journée de pilote (section dédiée), sans `start` ni `close`.
- `routine phare — à blanc` : `next` puis la routine désignée **sans écriture** (ni `create`, ni WP, ni journal) : proposition seulement, dans le rapport.

## Mode brouillons (pilote, `plan.md` D22)

Tant que `00_Systeme/Mode_brouillons.md` existe, rien n'est rendu public ni modifié en ligne. Les scripts le garantissent (`post_linking --publish-final`, `wp_refresh_body` et `daily_run --refresh-body` refusés ; `daily_run` force `--no-publish-final`) ; la séance ne cherche pas à les contourner (`--hors-pilote` est réservé au fondateur).
- **Contrôle complet obligatoire pour chaque article** : auto-contrôle puis agent `relecteur-prepublication` (prompt = chemin du fichier canonique, rien d'autre ; au cycle 2, chemin + passages modifiés). Défauts classés bloquant / mineur : des mineurs seuls ne font ni nouveau cycle ni BROUILLON ; 2 relectures au plus, puis on publie après correction à la source (`Controle_prepublication.md`). Une validation de forme ne suffit pas : faits, chiffres et dates, sources ouvertes, citations exactes, liens, droits humains et risques discriminatoires (grille A–D). La trace sépare **Autocontrôle** (codes trouvés par le rédacteur) et **Relecteur** (codes trouvés par l'agent, verdict), puis divergences et cycles.
- **Mémoire et Radar** : décision PUBLIER (retenu seulement par le mode) → `memoire_append` et Radar comme pour un article publié, pour que les activités suivantes s'appuient dessus ; décision BROUILLON → pas de ligne §1.
- **Relier en retour** : ne pas modifier l'article d'origine. Noter dans la trace « relier en retour à faire après publication : <origine> → <ID> ».
- **Rattrapage** : version révisée dans `07_A_Publier/<YYYY-MM-DD>_rattrapage_<ID>/` (copie du canonique modifiée), canonique et WP intacts ; clôture `termine_sans_publication --note "pilote : refresh en attente du fondateur"`.
- **Clôture** d'un article : `close … --statut brouillon --ids <ID> --note "pilote ; contrôle : PUBLIER"` (ou `"pilote ; contrôle : BROUILLON — <motif>"`).
- **Le fondateur publie** : `verify_publication.py --publish-drafts <ID>` (index mis à `publie`) ; depuis l'admin WP → `verify_publication.py <ID> --fix` pour resynchroniser l'index. La séance le lance elle-même, sans demande, pour chaque ID que `verify_publication` signale « publié sur WP mais `wp_draft` dans l'index » (le fondateur a déjà publié : `--fix` ne fait que mettre l'index à `publie` et ajouter `a-la-une` si absent). Le journal garde `brouillon` (décision de la séance) ; `contexte` et le bilan affichent « publié ensuite par le fondateur ». Publication d'une Question ou d'une Application → demander `relier en retour <ID>` : la séance relie l'origine puis `wp_refresh_body.py "<origine>" --hors-pilote` sur cette demande explicite.

## Bilan de pilote (`routine phare — bilan pilote`)

Juste après les quatre activités du jour (`next` le propose tant que le fichier manque), **distinct de la rétro hebdomadaire**, qui le lira.
```bash
python tools/phare.py contexte bilan_pilote [--periode <jour>]
```
Lire aussi les blocs de trace du jour (`06_Syntheses/Retros/<semaine>.md`) et les articles produits. Écrire `06_Syntheses/Retros/<jour>_bilan_pilote.md` :

```markdown
# Bilan de pilote — <jour>

## Activités
| Activité | ID | Statut journal | Tentatives | Durée | Décision de contrôle | Publié ensuite |

## 1. Sujets et complémentarité
## 2. Sources (nombre, nature, ouvertes ou non, sources faibles)
## 3. Contrôle : rédacteur et relecteur
| ID | Autocontrôle (codes) | Relecteur (codes B/m, verdict) | Trouvé par le relecteur seul | Cycles | Décision |
## 4. Corrections et maintiens en brouillon (motifs)
## 5. Rattrapage
## 6. Journal (erreurs, incohérences avec l'index)
## 7. Ressources (durée, lectures, recherches, appels à l'agent)
## 8. Difficultés techniques
## 9. Adaptations proposées
## Recommandation
Poursuivre le pilote / passer en production / corriger d'abord — argumentée par les sections 1–8. **Aucun passage en production sans validation du fondateur** (suppression de `00_Systeme/Mode_brouillons.md` par lui seul).
```
Rien d'autre n'est écrit (ni journal, ni WP, ni mémoire). Rapport : chemin du bilan et recommandation en trois lignes.

## 1. Décider

```bash
python tools/phare.py next
```
- `→ ARRÊT` (code 3) : séance active, intervention humaine requise ou production suspendue par une décision bloquante. **Afficher le message et s'arrêter.** Ne rien lancer d'autre.
- `→ Aucune action obligatoire` : le dire, avec la suggestion facultative ; ne rien lancer. Exception : suggestion « Bilan de pilote dû » → le bilan est la tâche de cette conversation (section dédiée).
- `→ PROCHAINE ACTION` ou `→ REPRISE` : passer à l'étape 2.

Les lignes « Décision … ouverte » sont du contexte : la routine les lit et en tient compte.

## 2. Ouvrir la séance

Lancer **exactement** la commande `start` affichée par `next` (activité et période). Refus → l'afficher et s'arrêter.

## 3. Exécuter avec la routine spécialisée

| Activité | Skill | Partie |
|---|---|---|
| `generale`, `curiosite`, `question` | `routine-quotidienne` | activité correspondante |
| `rattrapage` | `routine-renovation` | variante rattrapage |
| `fil` | `routine-hebdomadaire` | A. Fil du Phare |
| `retro_hebdo` | `routine-hebdomadaire` | B. Rétro hebdomadaire |
| `retro_mensuelle` | `routine-mensuelle` | A. Rétro mensuelle |
| `consolidation` | `routine-mensuelle` | B. Consolidation |

Lire la skill et suivre la partie désignée. En **reprise**, appliquer la consigne de `next` : même ID, même dossier de transit, jamais de nouveau `create` ; le push WP retrouve le post existant par slug.

Signaux de vie (même `--periode` que `start`), pour une reprise sans double création ni double publication :
```bash
python tools/phare.py etape <activité> --periode <P> --etape redaction --ids <ID>     # juste après create
python tools/phare.py etape <activité> --periode <P> --etape controle_ok             # décision PUBLIER
python tools/phare.py etape <activité> --periode <P> --etape wp                      # juste avant daily_run / wp_refresh_body
```

## 4. Clore avec le statut réel

```bash
python tools/phare.py close <activité> --periode <P> --statut <statut> [--ids …] [--note "<motif>"]
```

| Statut | Quand |
|---|---|
| `publie` | publié, `verify_publication` passé (l'index doit dire `publie`) |
| `brouillon` | contrôle éditorial non satisfait : brouillon WP (`wp_draft`), motif en note. **Pas de sujet de remplacement.** |
| `termine` | rétro (fichier complet, décisions) ou consolidation achevée |
| `termine_sans_publication` | activité menée sans article : rien ne mérite publication (Fil sans connexion sérieuse, rattrapage sans cible), motif en note |
| `reporte` | report volontaire (fondateur), motif en note |
| `incident` | échec technique (WP, script, réseau) : motif en note. Jamais considéré comme résolu : `next` le reproposera, puis demandera une intervention humaine après 2 tentatives. |

`close` refuse un statut que l'index ou le fichier de rétro ne confirment pas : corriger la situation ou choisir le statut réel, jamais forcer.

## 5. S'arrêter

Une activité par lancement : pas de deuxième `next` dans la même conversation. Rapport de la routine spécialisée, précédé d'une ligne :
```
Orchestrateur : <activité> (<période>) → <statut>
```
Pas de commit sans demande.

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `cd … &&`, `;`, `|`, ni `python -c` multiligne. Ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande, ni lire ces fichiers.

La séance tourne **sans interaction** : le fondateur vérifie le résultat dans WordPress à la fin. Toujours `python tools/…` nu, **sans préfixe de variable d'environnement** (`PYTHONIOENCODING=…` fait sortir la commande des règles autorisées ; l'UTF-8 est fixé par `env` dans `.claude/settings.json`). Pas de question ni de confirmation en cours de séance.

## Ne pas faire

- Choisir soi-même l'activité, ou en lancer une deuxième dans la même conversation.
- Lancer quoi que ce soit quand `next` dit ARRÊT.
- Éditer `00_Systeme/Journal_phare.csv` à la main (sauf correction humaine demandée).
- Clore `publie` ou `brouillon` sans que l'index le confirme ; clore un incident comme s'il était résolu.
- Chercher un autre sujet après un brouillon.
- En mode brouillons : publier, modifier un article en ligne, utiliser `--hors-pilote` sans demande explicite du fondateur, supprimer `00_Systeme/Mode_brouillons.md`.
