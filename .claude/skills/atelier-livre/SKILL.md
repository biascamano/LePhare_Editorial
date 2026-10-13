---
name: atelier-livre
description: Routine d'amélioration continue d'un livre — plan, rédaction, critique, arbitrage, puis plan suivant. Une étape par séance, déduite du journal de l'atelier.
---

# Atelier livre — amélioration continue

**Question de chaque séance : « Quelle est la prochaine étape qui rend ce livre meilleur ? »**

Le cycle :

```
PLAN vN ──► RÉDACTION (par chantiers) ──► CRITIQUE vN ──► ARBITRAGE ──► PLAN vN+1 …
   ▲  auteur valide                          lecteurs à l'aveugle   auteur décide
```

Le livre par défaut est `09_Livres/Vivons-nous tous dans le même réel/` (seul livre ayant un `atelier/`). Si plusieurs livres ont un atelier et que le prompt n'en nomme aucun : demander lequel.

Chemins ci-dessous relatifs au dossier du livre (`atelier/…`) ; dans les commandes, `<livre>` = `09_Livres/<titre>`. Commandes lancées depuis la racine du dépôt.

L'étape ARTICLE (§6) est **hors cycle** : elle se fait à la demande (`— article`) et ne change pas l'étape suivante du journal.

## Variantes du prompt

- `atelier livre` : étape suivante, lue dans la dernière ligne de `atelier/journal.md`.
- `atelier livre — état` : afficher où en est le cycle (journal, plan, chantiers restants, dernières mesures), sans rien écrire.
- `atelier livre — plan` / `— rédaction [partie N | chapitres a-b]` / `— critique` / `— arbitrage` : étape imposée (la signaler si elle saute une étape du cycle).
- `atelier livre — à blanc` : proposer l'étape suivante et son contenu, sans écrire.
- `atelier livre — article [chapitre NNN]` : un article « Savoir du livre » pour le Phare (§6). Sans chapitre : le premier chapitre rédigé de la version en cours qui n'a pas d'article dans `atelier/articles.md`.

## 0. Lire le contexte (toujours, et seulement ça)

1. `atelier/journal.md` : où en est le cycle.
2. `atelier/bible.md` : la promesse, la voix, les règles.
3. `atelier/decisions.md` : ce qui est tranché (ne pas le rouvrir sans motif nouveau).
4. Selon l'étape : le dernier `plans/plan_vN.md`, la dernière `critiques/critique_vN.md`, les dernières `mesures/vN.md`.

Ne pas relire tout le manuscrit hors des étapes RÉDACTION (chapitres du chantier) et CRITIQUE (confiée à l'agent).

## 1. PLAN vN

Entrées : bible, décisions, dernière critique arbitrée, matière existante (`manuscrit/`, `versions/`, `reserve.md`).

Écrire `atelier/plans/plan_vN.md` :

```markdown
# Plan vN — <date>

## Intention de la version
3–5 lignes : ce que cette version doit faire mieux que la précédente (renvoyer aux décisions D…).

## Architecture
| Partie | Titre | Question qu'elle fait avancer | Chapitres | Mots cibles |

## Chapitres
### NNN — <titre>
- Fonction : ce que le chapitre apporte au lecteur (une phrase)
- Scène (jardin) : …
- Notion : … · Niveau : établi / exploré / hypothèse
- Savant ou expérience : … · Source : …
- Origine : repris v3 NNN / fusion v3 NNN+NNN / nouveau
- Longueur cible : … mots
- Statut : à écrire / à reprendre / verrouillé

## Sorties vers la réserve
Ce qui quitte le livre et pour quel livre suivant.

## Questions à l'auteur
```

Règles :
- Chaque chapitre fait avancer **la** question du livre ; un chapitre sans fonction propre est fusionné ou sorti.
- Pas plus de 1 chapitre sur 4 sans savant, expérience ou fait vérifiable.
- Somme des mots cibles dans la fourchette de la bible.

Validation : présenter l'architecture (tableau des parties + nombre de chapitres + mots) et les points de rupture avec la version précédente, puis AskUserQuestion (valider / ajuster / refaire). Sur « ajuster » : modifier puis redemander. Journal : `PLAN vN | validé`.

## 2. RÉDACTION vN (par chantiers)

Un chantier = une partie, ou 4 à 8 chapitres. Le plan dit l'ordre ; le journal dit le chantier suivant.

Pour chaque chapitre du chantier :
1. Lire sa fiche dans le plan et les chapitres d'origine (`manuscrit/` ou `versions/`).
2. Réécrire **soi-même** en respectant la bible (voix, règles mesurables) : garder ce qui marche, ne pas réécrire pour réécrire. Chapitre `verrouillé` : ne pas toucher.
3. Nom de fichier : `NNN_slug.md`, numérotation du plan ; titre de partie en `# Partie …` en tête du premier chapitre de la partie, chapitre en `# Chapitre N` + `## Titre`.
4. Sources : ajouter les références du chapitre dans `atelier/sources.md`.
5. Matière retirée : l'ajouter à `atelier/reserve.md` (d'où, quoi, pour quel livre).

Les anciens fichiers qui ne correspondent plus au plan sont déplacés, pas supprimés : `manuscrit/_retires/` (le snapshot de la version précédente les garde de toute façon).

Fin de chantier :
```bash
python tools/livre.py stats "<livre>/atelier/manuscrit"
```
Contrôler les règles mesurables de la bible sur les chapitres du chantier ; corriger les écarts nets avant de clore. Journal : `RÉDACTION vN — <chantier> | fait`, et nommer le chantier suivant dans la note (ou `CRITIQUE vN` si tout est écrit).

## 3. CRITIQUE vN (version complète)

1. Figer et mesurer :
   ```bash
   python tools/livre.py snapshot "<livre>/atelier/manuscrit" "<livre>/atelier/versions/vN"
   python tools/livre.py stats "<livre>/atelier/versions/vN" --out "<livre>/atelier/mesures/vN.md"
   python tools/livre.py export "<livre>/atelier/versions/vN" "<livre>/VN/<titre> — VN complet.docx" --title "<titre>" --toc
   ```
2. Lecture à l'aveugle : agent `lecteur-critique`, **trois appels en parallèle**, un par regard (`curieux`, `scientifique`, `editeur`). Le prompt contient seulement : le regard, le chemin de `atelier/versions/vN`, et la section « Promesse » de la bible recopiée. **Jamais** le plan, les décisions, la critique précédente ni le raisonnement de l'auteur.
3. Écart au plan (par soi-même) : chapitres qui ne remplissent pas leur fonction, longueurs hors cible, sorties non faites.
4. Comparaison des mesures avec la version précédente (tableau : indicateur, v précédente, vN, cible bible).
5. Écrire `atelier/critiques/critique_vN.md` :

```markdown
# Critique vN — <date>

## Verdict en 5 lignes
## Mesures (vN-1 → vN, cible)
## Ce qui marche (à protéger)
## Propositions
### P1 — <titre> · gravité : majeure / moyenne / mineure · source : curieux / scientifique / éditeur / plan / mesures
- Constat : … (chapitres, citations courtes)
- Proposition : …
- Coût : léger / chantier / refonte
## Erreurs factuelles (liste, à corriger quoi qu'il arrive)
## Convergence
```

Une proposition = un constat appuyé sur le texte. Fusionner les remarques convergentes des trois lecteurs ; noter les désaccords entre eux. Les erreurs factuelles ne sont pas soumises à arbitrage : elles seront corrigées.

**Convergence** : aucune proposition majeure ET mesures dans les cibles de la bible ET deux critiques successives sans proposition majeure → déclarer la vN **version candidate** et préparer `atelier/beta_lecture.md` (questions pour 3 à 5 lecteurs humains). Journal : `CRITIQUE vN | faite`.

## 4. ARBITRAGE

Présenter les propositions par gravité. AskUserQuestion, au plus 4 questions par appel (regrouper les mineures) : retenir / rejeter / à modifier. Les erreurs factuelles ne se demandent pas.

Écrire ensuite :
- `atelier/decisions.md` : une décision `Dn` par proposition tranchée (retenue ou rejetée, avec le motif donné ou « sans motif »).
- `atelier/bible.md` : seulement si une décision change la promesse, la voix ou une règle (le noter dans la décision).

Journal : `ARBITRAGE vN | fait` ; l'étape suivante est `PLAN vN+1`.

## 5. Journal

Une ligne par étape, ajoutée en fin de tableau de `atelier/journal.md` :
`| <date> | vN | <ÉTAPE> | <statut> | <note : fait, puis étape suivante> |`

Une ligne ARTICLE recopie dans sa note l'étape suivante de la ligne précédente : le cycle reprend là où il en était.

## 6. ARTICLE — le savoir d'un chapitre sur le Phare (`plan.md` D23)

Un article du Phare sur **ce que le chapitre sait** (le savant, l'expérience, la notion), écrit pour être lu seul. **Jamais d'extrait ni de paraphrase du manuscrit** : pas de jardin, pas de vieil homme, pas de Yuki. Le livre est cité en fin d'article, sans promotion.

1. Lire la fiche du chapitre dans le dernier plan (Notion, Niveau, Savant ou expérience, Source), ses lignes de `atelier/sources.md` et le chapitre lui-même si besoin.
2. **Vérifier les sources** (veille web, sources primaires ou de référence). Une source `[à vérifier]` confirmée : retirer la marque dans `sources.md` et, si le chapitre est écrit, dans le chapitre. Infirmée ou douteuse : l'écrire dans `sources.md` (`[contredit : …]`) et le signaler dans le rapport ; le chapitre sera corrigé à la prochaine RÉDACTION (erreur factuelle, non soumise à arbitrage).
3. Créer et rédiger (~800–1200 mots), qualité `00_Systeme/Instructions_editoriales_officielles.md`, posture Transmettre : ce que l'on sait (établi), comment on le sait (l'expérience, le protocole), ce qui reste discuté, ce que cela change dans notre manière de voir.
   ```bash
   python tools/new_article.py create --type livre --theme <SCIENCE|CULTURE|…> --title "…" --slug <kebab-case> --pillar <pilier> --question "…" --keywords "…;…" --summary "…" --objective "…" --tags "livre-meme-reel;<savant ou notion>" [--linked "<ID>;…"]
   ```
   Navigation v3 (comme la routine quotidienne, étape 8) ; « Pour aller plus loin » : articles du Phare liés (URLs de `tools/index_lookup.py`) ; dernière ligne du corps avant la navigation : « Ce savoir nourrit le chapitre <N> du livre *<titre>*, en cours d'écriture. »
4. Publier comme tout article (`CLAUDE.md` racine, règles communes) : `stage`, contrôle prépublication (auto-contrôle puis agent `relecteur-prepublication`), `daily_run --publish-existing … --keep-publish-folder`, `verify_publication`. Mode brouillons : brouillon WP seulement. Pas de `memoire_append` ni de Radar (hors routines du Phare).
5. `atelier/articles.md` : une ligne `| <chapitre> | <ID> | <titre> | <statut> | <date> |`. Journal : `ARTICLE <chapitre> | <ID>`.

Une séance = une étape (une rédaction = un chantier). Ne pas enchaîner deux étapes dans la même conversation, sauf demande.

## Rapport

```
Atelier livre — <livre> — <date>
Étape : <ÉTAPE vN> → <statut>
Fichiers : …
Mesures : mots …, % courts …, formules récurrentes … (si mesuré)
À décider par l'auteur : … (ou rien)
Prochaine étape : …
```

## Commandes

Une commande Bash simple par appel (pas de `&&`, `;`, `|`). Read / Grep / Glob / Edit plutôt que `cat` / `grep` / `sed`. Ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande, ni lire ces fichiers.

## Ne pas faire

- Modifier ou supprimer un `.docx` existant ; réécrire un `versions/vN` existant.
- Écrire dans `bible.md` ou `decisions.md` sans arbitrage de l'auteur.
- Réécrire un chapitre `verrouillé`.
- Donner à l'agent critique le plan, les décisions ou la critique précédente.
- Supprimer de la matière : elle va en `reserve.md` ou `manuscrit/_retires/`.
- Inventer une expérience, une citation ou une référence : en cas de doute, la marquer `[à vérifier]` dans le texte et dans `sources.md`.
- Utiliser une API externe pour rédiger.
- Publier un extrait du manuscrit ; publier ou modifier en ligne en mode brouillons (`00_Systeme/Mode_brouillons.md`).
