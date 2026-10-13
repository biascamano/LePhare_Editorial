---
name: routine-hebdomadaire
description: Routine hebdomadaire Le Phare, en deux parties lancées séparément par l'orchestrateur — A. « Le Fil du Phare » (catégorie cycle, publié si au moins 4 articles et une connexion sérieuse) ; B. rétro hebdomadaire interne (décisions, audit des fils, comité du Radar). Déclenché par « routine phare » (via tools/phare.py), ou en secours par « routine hebdomadaire », « fil du phare » ou /routine-hebdomadaire.
---

# Routine hebdomadaire — le Fil et la rétro

**A. Fil du Phare** : « Qu'est-ce que nos articles racontent ensemble ? » (public).
**B. Rétro hebdomadaire** : « Qu'avons-nous décidé, fait, appris, et que changeons-nous ? » (interne, jamais publiée).

Deux activités distinctes de l'orchestrateur (`plan.md` D22) : `fil` (vendredi–dimanche, semaine en cours) et `retro_hebdo` (lundi, semaine précédente). Une seule par séance. En secours, sans orchestrateur : `routine hebdomadaire` = B puis A, `fil du phare` = A.

L'hebdomadaire crée les connexions. Elle ne cherche pas de sujet d'actualité et ne restructure ni dossiers ni Sentier (→ mensuelle). Autonomie totale. `brouillons seulement` → `--no-publish-final`.

---

## A. Le Fil du Phare

### A1. Relire les publications depuis le dernier Fil

L'orchestrateur a vérifié la condition minimale (≥ 4 articles publiés depuis le dernier Fil). Mémoire §1 : lignes depuis le dernier Fil (+ §2, §4). Pour chaque article (fichier canonique via `index_lookup.py`) : sujet, type, Question du Phare, concepts, dossier, Sentier, penseurs.

### A2. Chercher les connexions

Questions récurrentes, tensions communes, événements différents qui parlent du même phénomène, contradictions, thèmes émergents.

**Le seuil n'est pas une justification.** Si aucune connexion intellectuelle sérieuse n'apparaît (seulement des thèmes voisins ou un mot commun), **ne pas forcer** : pas de Fil cette semaine. Clore `termine_sans_publication` avec le motif (et l'ajouter à la trace de semaine) ; la rétro en jugera.

### A3. Formuler UNE grande question

Une seule question qui résume la période (ex. « Sommes-nous devenus plus libres ou simplement plus dépendants ? »).

### A4. Rédiger

Titre : `Le Fil du Phare - [question]` (passer `--title "[question]"` : `new_article.py` ajoute le préfixe, `plan.md` D16). ~900–1400 mots. Sections :

- **Cette semaine** — présentation très courte des événements (liens vers chaque article).
- **Le lien invisible** — ce qu'ils ont en commun.
- **La grande question** — développement.
- **Un penseur pour regarder autrement** — uniquement si pertinent, pas un cours de philosophie.
- **Ce que ces événements nous apprennent** — relier les domaines.
- **Ce que nous ne savons pas encore** — limites, questions ouvertes.
- **Où poursuivre ?** — dossier, textes fondateurs, Sentier (URLs réelles de l'index / `sentier_fondamentaux.csv`).

```bash
python tools/new_article.py create --type fil-du-phare --theme <THEME dominant> --title "…" --slug <kebab-case> --question "…" --linked "<IDs de la période>" --keywords "…" --summary "…" --objective "…" --tags "<concept>;…"
```
Le script calcule ID, fichier `06_Syntheses/Fil_du_Phare/`, type `SYNTHESE`, catégorie `cycle`, tags, slug `fil-du-phare-<slug>` et la ligne d'index. Rédiger le corps dans le `path` renvoyé, compléter navigation et `# SEO`. Sources en `[libellé](url)`.

### A5. Contrôler et publier

`python tools/new_article.py stage <ID>` (KO → corriger et relancer, jamais `--force` sur `stage`).

**Contrôle prépublication** (`00_Systeme/Controle_prepublication.md`) : auto-contrôle puis agent `relecteur-prepublication`. Pour un Fil, B porte surtout sur la fidélité aux articles reliés (aucun fait nouveau non sourcé, aucune affirmation qu'ils ne contiennent pas). PUBLIER → `daily_run` ; CORRIGER (au moins un défaut bloquant) → 2 cycles au plus, cycle 2 ciblé sur les passages modifiés ; défauts mineurs seuls : corrigés et tracés, sans nouveau cycle ; BROUILLON → `--no-publish-final`, clore `brouillon`.

```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder --force [--no-publish-final]
```

### A6. Mémoire, vérification

- §1 : `python tools/memoire_append.py <ID> --penseur "…"`.
- §3 : nouvelle ligne **en haut** — semaine, grande question, ID du Fil, concepts apparus, dossiers renforcés, pistes.
- `python tools/verify_publication.py` (erreur de tag ou lien `?p=` → `--fix`, puis relancer sans option), puis `python tools/build_etat_courant.py`.
- Trace : bloc `fil` dans `06_Syntheses/Retros/YYYY-Snn.md` (gabarit `06_Syntheses/Retros/README.md`).

---

## B. Rétro hebdomadaire

Fichier : `06_Syntheses/Retros/<YYYY-Snn>.md` de la semaine examinée (le créer depuis le gabarit s'il manque). La rétro remplit `## Rétro` ; elle **ne recopie pas** les traces, elle les juge.

### B1. Rassembler

```bash
python tools/phare.py contexte retro_hebdo --periode <YYYY-Snn>
```
Séances (statut final), publications et brouillons de l'index, décisions de la rétro précédente. Puis lire les traces de la semaine (`## Traces de la semaine`) et les **bilans de pilote** de la semaine (`06_Syntheses/Retros/<jour>_bilan_pilote.md`) : leurs enseignements nourrissent les points 3–5, leurs recommandations deviennent des lignes de la table « Décisions » (retenues, ajournées ou écartées, avec motif). Le passage en production reste une décision du fondateur : la rétro peut la recommander, pas la prendre. Rien d'autre sauf besoin précis.

### B2. Les six points (sous-sections de `## Rétro`)

1. **Décisions précédentes** — reprendre chaque décision ouverte de la rétro précédente (table « Décisions »).
2. **Mise en œuvre** — pour chacune : faite, en cours, pas commencée ; preuve (ID, trace, commit, fichier).
3. **Résultats** — objectifs quotidiens tenus / non tenus par jour ; publiés, brouillons (motifs), incidents, reports ; contrôle prépublication (divergences a/b, cycles) ; soutenabilité du rythme ; ce que les décisions ont réellement changé.
4. **Problèmes et angles morts** — ce qui se répète, ce que personne ne regarde (thèmes absents, types jamais choisis, sources toujours les mêmes, articles sans suite).
5. **Ajustements proposés** — peu, concrets, vérifiables.
6. **Décisions** — table ci-dessous (les ouvertes reportées avec leur état à jour, puis les nouvelles).

### B3. Audit des fils éditoriaux

Mémoire §2 (**5 fils actifs au plus**) : à poursuivre (+ prochaine piste), à clôturer, à mettre de côté (+ condition de reprise). Une ligne de synthèse dans la rétro (point 3 ou 4).

### B4. Comité éditorial du Radar

`00_Systeme/Radar_editorial.md` (`plan.md` D14) :
- retirer le réalisé ; fusionner les doublons ;
- re-prioriser les blocs 1–3 (P1 = échéances fixes et suites naturelles fortes, sinon P2/P3) ; statuts (`approfondir`, `relier`, `à échéance (…)`, `conserver`) ;
- 3 à 5 pistes pour la semaine suivante (suites, nouveaux terrains pour les mêmes questions, TF nécessaires) — pas de programme de sept articles ;
- archiver ce qui a perdu sa raison d'être ; **30 entrées actives au plus** ; date « État au ».
Blocs 4–5 : mensuelle. Une ligne de synthèse dans la rétro.

### B5. Décisions

Dernière sous-section de `## Rétro` :
```markdown
### Décisions

| N° | Décision | Priorité | Échéance | État |
|---|---|---|---|---|
| D-2026-S42-1 | … | bloquante / importante / normale | AAAA-MM-JJ ou « prochaine rétro » | à faire / en cours / faite / abandonnée |
```
- Les décisions encore ouvertes de la rétro précédente sont **reportées** avec leur N° d'origine et leur état mis à jour ; une décision faite ou abandonnée n'apparaît qu'une fois, avec cet état.
- **bloquante** : suspend toute production (`phare.py next` → ARRÊT) jusqu'à ce que son état passe à « faite » — réservée à un problème qui rendrait la publication fautive (erreur de fait répétée, faille de contrôle, maillage cassé).
- **importante** : affichée par `next` à chaque séance, jusqu'à « faite ».
- Une semaine sans décision nouvelle : une ligne « normale — Ras » suffit.

### B6. Clore

`python tools/verify_publication.py` (signaler, ne pas publier les brouillons), `python tools/build_etat_courant.py`, puis `close retro_hebdo --statut termine` : `phare.py` refuse si `## Rétro` est vide ou la table absente.

---

## Rapports

```
Fil du Phare — semaine …
Fil : [question] — URL (ou : pas de Fil, motif)
Articles reliés : N (IDs) · Contrôle : a … / b … · cycles N
Vérification : N articles, X erreurs, Y avertissements
```
```
Rétro hebdomadaire — semaine … (fichier)
Décisions précédentes : N faites / N en cours / N non commencées
Objectifs : publiés N · brouillons N · incidents N · reports N · sans publication N
Fils : +X / Y clôturés / Z de côté · Radar : N actives
Nouvelles décisions : … (bloquantes : …)
```

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `cd … &&`, `;`, `|`, ni `python -c` multiligne. Read / Grep / Edit plutôt que `cat` / `grep` / `sed`. URLs de l'index : `python tools/index_lookup.py <IDs>`. Refresh WP : `python tools/wp_refresh_body.py "<chemin>"` ; ne jamais écrire le chemin d'un `tools/*.local.json` dans une commande.

## Ne pas faire

- Publier un Fil parce que le seuil est atteint, sans lien invisible réel ; résumé chronologique.
- Publier la rétro, ou y recopier les traces.
- Chercher le sujet d'actualité du jour ; créer un dossier, un TF ou un atelier (→ mensuelle).
- Marquer une décision « faite » sans preuve.
