# Workflow éditorial Le Phare — triptyque (ancienne routine quotidienne, archivée)

> Ne s'applique qu'à `routine triptyque`. Ne pas charger pour les routines quotidienne / hebdomadaire / mensuelle actuelles.

Aligné sur `.cursor/rules/editorial-assisted-writing.mdc` et `00_Systeme/Routine_quotidienne_V2.md`.

## 1. Choix du sujet

- Pas de validation utilisateur avant rédaction.
- Veille web autorisée (RSS Google News FR, sources institutionnelles, presse sérieuse).
- **Rotation thématique** (si sujet libre) :
  1. Prioriser **TECH** et **CULTURE** (sous-représentés).
  2. Modérer **SCIENCE** et **ECON**.
  3. Maintenir **CLIMAT** et **POL**.
- Enrichir le **graphe de savoir** : liens cross-thèmes, tags WP cohérents (`00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md`).
- Éviter sujets déjà traités récemment dans `index_editorial.csv`.

## 2. Rédaction du triptyque

### ACTU
- Posture **Observer** ; slow journalism, pas sensationnalisme.
- ACTU institutionnelle / législative : §3.8 Instructions (accroche concrète, tension, dates précises, encadrés « ce que ça ne fait pas »).
- Titres et sections **adaptés au sujet** (§3.0), pas la même grille générique à chaque fois.
- `**gras**` parcimonieux (quelques phrases à fort signal).

### TF
- Posture **Comprendre** ; auteur ou concept ancré, lien explicite avec l'ACTU du jour.
- ~900–1600 mots selon matière.

### SENTIER
- Outil réutilisable (grille, méthode, posture) — **atelier** d'un fondamental existant.
- **Rotation étape** : consulter les 3 derniers SENTIER publiés (IDs desc dans `05_Sentier/`). Si `Etape_02_Pensee_critique` ≥ 2 fois sur 3, choisir une autre étape. Prioriser : `Etape_03_Argumentation`, `Etape_04_Expertise`, `Etape_01_Culture_generale`, `Etape_05_Polyglotte`, `Etape_06_Methode_scientifique`, `Etape_07_Transmission`, `Etape_09_Equilibre_corps_esprit`.
- **Diversité de titre** : si ≥ 2 des 3 derniers SENTIER utilisent « Lire X sans confondre Y », **ne pas réutiliser**. Alternatives : `Cartographier`, `Construire`, `Argumenter sur`, `Naviguer entre`, `Décoder`, `Distinguer`, `Ce que X révèle sur Y`.
- **3 règles densité SENTIER** (§3.7) — obligatoires avant validation :
  1. Mini-cas ancré sur l'**ACTU réelle** du jour (pas d'exemple fictif générique).
  2. ≥ 2 **sources nommées** dans le mini-cas + ce que chacune dit / ne dit pas.
  3. Chaque item de la grille résolu avec une application directe sur l'ACTU.

## 3. Ancrage SENTIER atelier (§3.9)

1. Lire `00_Systeme/Manifests/sentier_fondamentaux.csv` — **jamais** URL `wiki-du-phare`.
2. Choisir `fondamental_id`, étape, numéro fondamental.
3. En-tête SENTIER : `Type Sentier : atelier`, `Fondamental lie (ID)`, `Fondamental numero`, `Posture Sentier`.
4. Chapo : renvoi au fondamental parent (titre + lien WP si connu).
5. Fin du `.md` **fondamental parent** (`02_Fonds/…` ou chemin CSV) — section :

```markdown
## Ateliers (applications sur l'actualite)

| Date | Triptyque | Atelier (SENTIER) |
|------|-----------|-------------------|
| YYYY-MM-DD | Titre triptyque | [Titre atelier](URL) (`ID`) |
```

6. Tags index : `atelier-sentier` + `fondamental-YYYY-NNN`.

## 4. Micro-édition + calibrage (automatique, sans demander)

| Type | Longueur indicative | Promesse |
|------|---------------------|----------|
| ACTU | ~650–1100 mots | Décrypter le signal, contextualiser |
| TF | ~900–1600 mots | Ancrage durable, nuances |
| SENTIER | ~900–1400 mots | Le lecteur sait quoi faire / comment lire |

Exécuter **avant** copie dans `07_A_Publier`. Ne pas diluer pour le SEO.

## 5. Métadonnées et format Markdown

Modèle en-tête : `00_Systeme/Modele_Entete_Article.md` + blocs `# SEO` (mot-clé, meta, slug).

**Repères de sources** — liens Markdown obligatoires :
```markdown
- Commission : [communiqué du 3 juin](https://...)
```

**Dans ce triptyque** — libellés hors lien :
```markdown
Approfondir avec le texte fondateur : [Titre seul](url)
Prolonger avec le Sentier du Savoir : [Titre seul](url)
```

## 6. Fichiers et index

1. Chemins canoniques :
   - ACTU → `01_Actualites/<Theme>/`
   - TF → `04_Textes_fondateurs/Auteurs/`
   - SENTIER → `05_Sentier/Etape_XX_.../`
2. Copie identique → `07_A_Publier/<YYYY-MM-DD_slug-court>/`
3. Index : append via Python uniquement :

```python
from pathlib import Path
import sys
sys.path.insert(0, "tools")
from index_editorial_utils import append_rows_to_index, build_index_row

# build_index_row(...) × 3 puis append_rows_to_index(Path("index_editorial.csv"), rows)
```

Ou script one-shot équivalent. **Jamais** `csv.writer` manuel (colonnes décalées → doublons WP).

Validation optionnelle : `python tools/validate_index_editorial.py`

## 7. Publication

```bash
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>"
```

Séquence : push WP → `post_linking` → **publish** (sauf `--no-publish-final`).

Après succès : supprimer le sous-dossier staging sous `07_A_Publier` (sauf `--keep-publish-folder`).

**Second passage** (retouches locales post-maillage) :
```bash
python tools/daily_run.py --publish-existing "<dossier>" --skip-wp-push
```

**Même jour, second run complet** : `--force`

## 8. Post-publication (assistant)

- `wp_push_draft --refresh-body` sur le **SENTIER atelier** (`05_Sentier/…`) si corps modifié après maillage :
  ```bash
  python tools/wp_push_draft.py --refresh-body --index index_editorial.csv --config tools/wp_config.local.json "<chemin_sentier>"
  ```
- **Ne jamais** push `02_Fonds/…` (fondamental parent).
- Lire `00_Systeme/Logs/daily_run_YYYY-MM-DD.json` → `parent_refresh_reminder`.
- Rappeler à l'utilisateur : vérifier WP ; désactiver doublons `wiki-du-phare` ; rafraîchir fondamental parent **manuellement** sur WP.

## 9. Exceptions explicites

| Demande | Comportement |
|---------|--------------|
| `routine quotidienne api` | `editorial_pipeline.py --use-api-llm` |
| `--seo-enrich-after-link` | Seulement si `seo_enrich_api_enabled: true` + clé API |
| Ollama / local LLM | Uniquement si demandé explicitement |

## 10. Taxonomie WP (triptyque)

| Volet | Categorie_WP |
|-------|--------------|
| ACTU | actualites |
| TF | textes-fondateurs |
| SENTIER | sentier-du-savoir |

Tags : theme (couche A) + famille Sentier (couche B) + concepts (couche C) + `triptyque` + `posture-*`. Détail : `00_Systeme/Taxonomie_WordPress_le-phare_info.md`.
