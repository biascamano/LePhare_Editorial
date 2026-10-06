# Le Phare Editorial — Claude Code

Dépôt de rédaction assistée pour [le-phare.info](https://le-phare.info/) : trois routines légères (quotidienne / hebdomadaire / mensuelle) partageant une mémoire éditoriale, publication WordPress, maillage interne.

> Le quotidien produit les briques. L'hebdomadaire crée les connexions. Le mensuel construit l'architecture.

Plan de référence (décisions, état, backlog) : **`plan.md`** — à mettre à jour à chaque évolution des routines.

## Déclencheurs utilisateur (manuels, pas de cron)

| Prompt | Action | Skill |
|--------|--------|-------|
| `routine quotidienne` | **Un** article : le meilleur prochain article du Phare, type choisi après le sujet (Actualité, Question, Application, exceptionnellement TF) — `plan.md` D12 | `.claude/skills/routine-quotidienne/SKILL.md` |
| `routine quotidienne — sujet : …, thème TECH` | Même routine, sujet imposé | idem |
| `routine quotidienne — type application` / `type texte fondateur` / `type actualite` | Type imposé | idem |
| `routine quotidienne — type question — sur <ID>` | Question sur la question finale de `<ID>` | idem |
| `routine quotidienne — paire` | Actualité + Question le même jour, liens croisés | idem |
| `routine quotidienne — brouillons seulement` | `--no-publish-final` | idem |
| `routine hebdomadaire` / `fil du phare` | Le Fil du Phare (`SYNTHESE`, catégorie WP `cycle`) + fils éditoriaux + comité du Radar | `.claude/skills/routine-hebdomadaire/SKILL.md` |
| `routine mensuelle` | Dossiers, TF, ateliers Sentier, audit, synthèse mensuelle, cap du mois | `.claude/skills/routine-mensuelle/SKILL.md` |
| `routine triptyque` / `triptyque` | **Ancienne** routine ACTU+TF+SENTIER (archivée, secours) | `.claude/skills/routine-triptyque/` |
| `… api` | **Exception** : `editorial_pipeline.py --use-api-llm` | — |

**Mémoire partagée** : `00_Systeme/Memoire_editoriale.md` — lue par l'hebdomadaire et la mensuelle, mise à jour en fin de chaque routine (§1 via `tools/memoire_append.py`).
**Quotidienne** : lit seulement `00_Systeme/Etat_editorial_courant.md` (généré par `tools/build_etat_courant.py`, jamais édité à la main), `00_Systeme/Radar_editorial.md` et la veille web — pas le catalogue.

**Ne pas demander** validation du sujet avant de rédiger. Choisir le sujet directement si absent.

## Mode rédaction (défaut)

- **Rédiger toi-même** (pas Ollama, pas API externe pour la rédaction initiale).
- Ligne éditoriale : `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` ; qualité rédactionnelle : `00_Systeme/Instructions_editoriales_officielles.md` (écart → le signaler, `plan.md` D10).
- `daily_run.py` / `editorial_pipeline.py` = **outils techniques** (index, WP, maillage), pas moteurs d'écriture par défaut.
- `post_linking.py` accepte un dossier de publication à **1 article** (routines v3) ou **3** (triptyque) : la variante `paire` passe par deux dossiers de transit (`plan.md` §5.9).

## Structure du dépôt

```
01_Actualites/<Theme>/     → ACTU
04_Textes_fondateurs/Auteurs/ → TF
05_Sentier/Etape_XX_.../   → SENTIER (atelier)
03_Dossiers/<Theme>/       → DOSSIER (routine mensuelle)
06_Syntheses/              → SYNTHESE : Fil_du_Phare/, Mensuelles/, Rapports_mensuels/
07_A_Publier/<dossier>/    → transit avant publication (supprimé après succès)
index_editorial.csv        → registre canonique (IDs, slugs, URLs WP)
tools/                     → scripts Python (daily_run, wp_push_draft, post_linking)
00_Systeme/                → instructions, taxonomie, manifests Sentier, logs
```

**Dossiers ACTU par thème** : `Technologie_IA`, `Climat_Transition`, `Economie_Finance`, `Science_Sante`, `Politique_Societe`, `Culture`.

## IDs articles

Lire la **dernière ligne** de `index_editorial.csv` pour réserver les prochains IDs (`YYYY-NNN`). Ne jamais réutiliser un ID existant.

Convention nom de fichier : `YYYY-NNN_TYPE_THEME_slug_descriptif_V1.md` (TYPE ∈ ACTU, TF, SENTIER, FOND, DOSSIER, SYNTHESE).

## Règles communes de publication

1. `Repères de sources` en `[libellé](url)`.
2. Sauver chemin canonique + copie `07_A_Publier/<YYYY-MM-DD_slug>/` (un dossier par article hors triptyque).
3. Index : **uniquement** via `tools/index_editorial_utils.append_rows_to_index` (jamais `csv.writer` brut).
4. `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder` (`--force` si un run a déjà réussi le même jour).
5. Mettre à jour `00_Systeme/Memoire_editoriale.md`.
6. Signaler à l'utilisateur : vérifier sur WordPress ; refresh **manuel** de tout fondamental parent (`02_Fonds/…`) modifié.

## Prérequis locaux (non versionnés)

| Fichier | Rôle |
|---------|------|
| `tools/wp_config.local.json` | Auth WordPress (copier depuis `wp_config.example.json`) |
| `tools/wp_featured_media.local.json` | Images à la une par tag (optionnel) |
| `tools/editorial_config.local.json` | API LLM — **seulement** si demande explicite `api` |

## Commandes utiles

```bash
# Publication (défaut : push WP + maillage + publish)
python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>"

# Variantes
python tools/daily_run.py --publish-existing "<dossier>" --no-publish-final
python tools/daily_run.py --publish-existing "<dossier>" --force
python tools/validate_index_editorial.py
```

## Docs de référence (lire au besoin)

| Fichier | Contenu |
|---------|---------|
| `00_Systeme/Instructions_editoriales_officielles.md` | Ton, calibrage §3.7–3.10, ancrage §3.9 |
| `00_Systeme/Memoire_editoriale.md` | Mémoire partagée des 3 routines |
| `00_Systeme/Routine_quotidienne_V2.md` | (archivé) workflow triptyque V2 |
| `00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md` | Choix de sujet, graphe éditorial |
| `00_Systeme/Taxonomie_WordPress_le-phare_info.md` | Catégories / tags WP |
| `00_Systeme/Manifests/sentier_fondamentaux.csv` | Fondamentaux parent (atelier) |
| `00_Systeme/Sentier_fondamentaux_referentiel.md` | Règles atelier ; **ne pas** push `02_Fonds/` |
| `00_Systeme/Sentier_dedoublonnage_wiki.md` | Doublons `wiki-du-phare` |

## Interdits

- Appel API silencieux pour rédaction ou calibrage (flags `calibration_api_enabled` / `seo_enrich_api_enabled` requis).
- `editorial_pipeline.py` comme moteur d'écriture sans demande explicite `api`.
- Push WP sur fondamental parent (`02_Fonds/…`) — éditeur humain.
- URLs nues dans `Repères de sources` (WordPress ne les rend pas cliquables).
- Créer un 11e fondamental Sentier : un SENTIER = **atelier** d'un fondamental existant (proposition seulement, en routine mensuelle).
