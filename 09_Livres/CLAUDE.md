# Livres — Nexus des mondes

Atelier d'écriture des livres de la collection (premier livre : **Vivons-nous tous dans le même réel ?**). Amélioration continue par cycles : **plan (cartographie) → version → critique → transmission → audit de la direction → arbitrage → plan suivant**, puis clôture. Le savoir de chaque chapitre donne aussi des articles du Phare (catégorie WP `livres`, `plan.md` D23).

## Déclencheur

| Prompt | Action | Skill |
|--------|--------|-------|
| `atelier livre` (+ `— état` / `— plan` / `— rédaction [partie N]` / `— critique` / `— transmission` / `— audit` / `— arbitrage` / `— clôture` / `— article [chapitre NNN]`) | Une étape du cycle, déduite de `atelier/journal.md` (ou imposée) | `.claude/skills/atelier-livre/SKILL.md` |

## Rôles

- **Auteur** : vision, intentions, décisions finales.
- **Direction éditoriale** (ChatGPT, hors dépôt) : audit indépendant de chaque version, orientations. Reçoit le DOCX et le dossier de transmission ; son audit est déposé dans `atelier/direction/`.
- **Claude** : rédaction et exécution. Peut contester, par un argument littéraire, narratif ou scientifique, jamais par l'autorité d'un modèle.

Aucune orientation de la direction n'est appliquée avant l'arbitrage de l'auteur. Double validation de chaque réécriture : littéraire ET scientifique.

## Structure

```
09_Livres/
  Articles/                  → articles « Savoir du livre » (type LIVRE, index_editorial.csv)
  vision_collection.md       → vision de la collection (direction éditoriale) : orientation, cycles et titres provisoires
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
      critiques/lecteurs_vN/   → sorties brutes des trois lecteurs
      transmission_direction_editoriale_vN.md → dossier pour la direction éditoriale (lisible sans le dépôt)
      direction/audit_vN.md    → audit de la direction (déposé par l'auteur, tel quel)
      direction/reponse_vN.md  → réponse argumentée de Claude (accords, désaccords, nuances)
```

## Règles

- Répondre en français. Rédiger soi-même (pas d'API externe).
- Ne jamais modifier ni supprimer un `.docx` existant ; les nouvelles versions sont exportées dans un nouveau fichier.
- `bible.md` et `decisions.md` : l'auteur décide. Claude propose, n'y écrit qu'après arbitrage.
- Un chapitre marqué `préservé` (ou `verrouillé`) dans le plan n'est pas réécrit, hors erreurs factuelles. Aucune réécriture avant validation de la cartographie entière.
- Une mesure améliorée au prix de la spontanéité est un recul.
- `vision_collection.md` oriente, ne décide pas : un écart avec la bible ou `decisions.md` est soumis à l'auteur. Chaque livre ne traite que sa question (préparer sans annoncer, ne pas épuiser les tomes suivants) ; l'architecture de la collection n'apparaît jamais comme structure visible pour le lecteur. Cartographie : ajouter les six questions de la vision (§ 12) à chaque chapitre.
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
