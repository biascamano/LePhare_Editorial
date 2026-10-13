# Livres — Nexus des mondes

Atelier d'écriture des livres de la collection (premier livre : **Vivons-nous tous dans le même réel ?**). Amélioration continue par cycles : **plan → version → critique → arbitrage → plan suivant**. Le savoir de chaque chapitre donne aussi des articles du Phare (catégorie WP `livres`, `plan.md` D23).

## Déclencheur

| Prompt | Action | Skill |
|--------|--------|-------|
| `atelier livre` (+ `— état` / `— plan` / `— rédaction [partie N]` / `— critique` / `— arbitrage` / `— article [chapitre NNN]`) | Une étape du cycle, déduite de `atelier/journal.md` (ou imposée) | `.claude/skills/atelier-livre/SKILL.md` |

## Structure

```
09_Livres/
  Articles/                  → articles « Savoir du livre » (type LIVRE, index_editorial.csv)
  carte_des_questions.md
  <Titre du livre>/
    V1/, V3/, *.docx           → versions historiques (docx), jamais modifiées
    V4/…                       → exports docx des nouvelles versions (tools/livre.py export)
    Srategie.docx, critiques.docx → réflexions de départ (lues, jamais modifiées)
    atelier/
      bible.md                 → canon du livre : promesse, périmètre, dispositif, voix, règles mesurables
      decisions.md             → décisions de l'auteur (D1, D2…), avec motif ; on ne revient sur une décision que par une nouvelle
      journal.md               → une ligne par étape ; la dernière dit où en est le cycle
      reserve.md               → matière sortie du livre (vers les livres suivants) : rien ne se perd
      sources.md               → références par chapitre, base du « Pour aller plus loin »
      articles.md              → chapitre → article du Phare (ID, statut)
      plans/plan_vN.md         → plan de la version N
      manuscrit/               → version en cours, un fichier Markdown par chapitre (NNN_slug.md)
      versions/vN/             → versions figées (snapshot), jamais réécrites
      mesures/vN.md            → mesures de style (tools/livre.py stats)
      critiques/critique_vN.md → critique de la version N (agent lecteur-critique + écart au plan)
```

## Règles

- Répondre en français. Rédiger soi-même (pas d'API externe).
- Ne jamais modifier ni supprimer un `.docx` existant ; les nouvelles versions sont exportées dans un nouveau fichier.
- `bible.md` et `decisions.md` : l'auteur décide. Claude propose, n'y écrit qu'après arbitrage.
- Un chapitre marqué `verrouillé` dans le plan n'est pas réécrit.
- Articles du Phare : règles communes de publication du `CLAUDE.md` racine (mode brouillons compris) ; jamais d'extrait du manuscrit.
- Une commande Bash simple par appel (pas de `&&`, `;`, `|`).

## Outils (depuis la racine du dépôt)

```bash
python tools/livre.py import "<docx>" "<dossier>"           # docx → un .md par chapitre
python tools/livre.py stats "<dossier>" --out "<mesures.md>" # mots, % paragraphes courts, formules récurrentes
python tools/livre.py snapshot "<manuscrit>" "<versions/vN>" # fige une version
python tools/livre.py export "<dossier>" "<sortie.docx>" --title "<titre>" [--toc] [--reference <modele.docx>]
python tools/new_article.py create --type livre …           # article « Savoir du livre »
```

pandoc : variable `PANDOC`, sinon `PATH`, sinon `D:/Logiciel/pandoc-3.9.0.2-windows-x86_64/pandoc-3.9.0.2/pandoc.exe`.
