# Referentiel Sentier — fondamentaux, ateliers, triptyques

Source machine : `00_Systeme/Manifests/sentier_fondamentaux.csv` (9 etapes × 10 fondamentaux + hubs).

Colonnes utiles : `fondamental_id`, `url_canonique`, `nom_fichier`, `exclure_wiki` (`non` = canonique hors KB).

Arborescence depot : `00_Systeme/Arborescence_Sentier_par_etapes.md`.

Dedoublonnage Echo KB / URLs `wiki-du-phare` : `00_Systeme/Sentier_dedoublonnage_wiki.md`.

---

## Exclusion des doublons wiki-du-phare (Echo Knowledge Base)

**Ne jamais** prendre comme fondamental canonique un article dont l’URL contient :

`https://le-phare.info/wiki-du-phare/`

Ce sont des **copies KB** (souvent IDs `2026-3xx` dans l’index), en double des articles **racine** (`https://le-phare.info/{slug}/`, souvent IDs `2026-1xx` / `2026-2xx`).

Pour chaque fondamental du CSV :

- utiliser **`fondamental_id`** et **`url_canonique`** du manifeste ;
- ouvrir / mettre a jour **`nom_fichier`** (pas la copie wiki dans `05_Sentier/` si le CSV pointe vers `02_Fonds/`) ;
- liens internes et rubrique **Ateliers** : URL **racine** uniquement.

---

## Typologie (obligatoire pour les triptyques)

| Type | Role | Quand le creer | Sidebar « 10 fondamentaux » |
|------|------|----------------|------------------------------|
| **Fondamental** | Pilier intemporel de l'etape (~1200 mots) | Rare ; liste fixe dans le CSV | Oui (1 des 10) |
| **Sous-fondamental** | Approfondissement d'un pilier | Seulement si lacune structurelle validee | Non (lie au parent) |
| **Atelier** | Application sur l'actualite (article **SENTIER** du triptyque) | **Chaque triptyque** qui produit un SENTIER outil | Non — liste sous le fondamental parent |

**Regle d'or** : la routine quotidienne et les triptyques **n'ajoutent pas** un 11e fondamental. L'article SENTIER du triptyque est un **atelier** rattache a un fondamental existant.

Competences affichees sur WordPress (ex. « Mettre a distance les recits ») = **posture** ou **sous-titre** de l'atelier ; l'ancrage structurel reste **etape + fondamental #** du CSV.

---

## Etape triptyque : ancrage fondamental et rubrique Atelier

Executer **apres** la redaction du SENTIER et **avant** la micro-edition / calibrage (ou juste apres calibrage, mais **avant** copie dans `07_A_Publier`).

### 1. Choisir l'etape et le fondamental parent

1. Lire `00_Systeme/Manifests/sentier_fondamentaux.csv`.
2. Selectionner `etape_num` (1–9) et `fondamental_num` (1–10) **les plus proches** de la competence travaillee.
3. Noter `fondamental_id`, `url_canonique`, `nom_fichier` (ignorer toute ligne index `wiki-du-phare`).

**Grille rapide (triptyques recents, IDs canoniques hors wiki)** :

| Forme du SENTIER | Etape | Fond. # | ID parent |
|------------------|-------|---------|-----------|
| Lire une annonce institutionnelle / reglementaire / commerce / sante / climat | 2 | 5 | 2026-198 |
| Lire une annonce medicale ou scientifique (population, protocole) | 2 | 7 | 2026-196 |
| Decrypter discours publicitaire ou propagande | 2 | 9 | 2026-194 |
| Argumenter sur budget / debat politique complexe | 3 | 10 | 2026-182 |
| Expertise durable face a l'automatisation (metier, IA) | 4 | 2 ou 10 | 2026-180 / 2026-172 |
| Penser une crise sans court terme (energie, systeme) | 8 | 1 ou 9 | 2026-140 / 2026-131 |
| Vulgariser ou transmettre un savoir technique | 7 | 3 | 2026-352 |

Exemple **budget UE mai 2026** : etape **3**, fondamental **10** (**2026-182**), atelier **2026-468**.

### 2. Metadonnees du fichier SENTIER (atelier)

Completer l'en-tete :

```text
Etape du Sentier liee : Etape 02 — Maitriser la pensee critique
Fondamental lie (ID) : 2026-399
Fondamental numero : 5
Type Sentier : atelier
Posture Sentier : Mettre a distance les recits
```

Dans le corps, premiere section ou chapo : une phrase qui renvoie au **fondamental parent** (titre + lien WP quand `URL_WordPress` est connue).

### 3. Rubrique « Ateliers » en fin du fondamental parent

Ouvrir le fichier canonique du fondamental (`chemin_canonique` + nom depuis l'index ou le depot).

**Si la section n'existe pas**, l'ajouter **en dernier** du corps (apres conclusion / exercices existants) :

```markdown
## Ateliers (applications sur l'actualite)

Ces textes appliquent ce fondamental a un sujet d'actualite (triptyque Le Phare : ACTU + texte fondateur + outil Sentier). Ils entrainent la competence sur un cas reel ; ils ne remplacent pas le fondamental.

| Date | Triptyque | Atelier (SENTIER) |
|------|-----------|-------------------|
| YYYY-MM-DD | Titre court du triptyque | [Titre de l'atelier](URL_WP_atelier) (`ID`) |
```

**Regles** :

- Une **ligne par atelier** ; triptyques les plus recents en haut.
- Lien vers l'article SENTIER publie (ou laisser l'ID seul si pas encore sur WP).
- Ne pas dupliquer le contenu de l'atelier dans le fondamental : **titre + lien + date** suffisent.
- Si le fondamental a deja « Exercice pratique » generique, **conserver** ce bloc ; « Ateliers » vient **apres**.

### 4. Index et tags

- `index_editorial.csv` : colonne `Etape_sentier` = libelle etape ; dans `Remarques` ou `Tags_WP`, ajouter `atelier-sentier` + `fondamental-2026-399` (slug stable).
- ACTU et TF du meme triptyque : `Etape_sentier` + mention du fondamental en conclusion (deja prevu Instructions 3.6 / 3.8).

### 5. WordPress apres le triptyque

`daily_run.py --publish-existing` pousse et maille le **triptyque** (ACTU + TF + SENTIER) ; il **ne met pas a jour** le fondamental parent sur WordPress.

#### Fondamental parent — editeur uniquement

La rubrique `## Ateliers` est mise a jour dans le **fichier Markdown canonique** du fondamental (`02_Fonds/…`) par le flux redactionnel (Instructions 3.9). Pour que cette table soit **visible sur le site**, l'**editeur** repousse le corps du fondamental parent quand il le souhaite, par exemple :

```bash
python tools/wp_refresh_body.py "<chemin_fondamental_parent>.md" --allow-fonds
```

**Fichiers FOND** (`02_Fonds/…`) : `wp_push_draft` exige un `Slug propose` (bloc `# SEO` et/ou `## Bloc publication` en fin de fichier) — sinon erreur « Missing required field: Slug propose ».

L'**assistant** ne lance **pas** ce push sur le fondamental parent par defaut (decision editeur).

#### SENTIER atelier — assistant (corps WP)

Apres un `daily_run --publish-existing` reussi, si le **SENTIER atelier** a ete retouche en local (chapo, liens §3.10, corps) ou pour aligner WP sur la version **canonique** du depot, l'assistant peut repousser **uniquement** cet article :

```bash
python tools/wp_refresh_body.py "<chemin_sentier_atelier>.md"
```

**Ne pas** appliquer cette passe au fichier fondamental parent (`02_Fonds/…`) : reserve editeur (voir ci-dessus).

**Doublons Echo KB** (`wiki-du-phare`) : ne **jamais** pousser ces copies ; l'editeur **desactive** (brouillon) les articles doublons sur WordPress — voir `Sentier_dedoublonnage_wiki.md`.

---

## Inventaire par etape (resume)

Detail complet : `Manifests/sentier_fondamentaux.csv`.

| Etape | Nom | Hub ID |
|-------|-----|--------|
| 1 | Construire une culture generale solide | 2026-413 |
| 2 | Maitriser la pensee critique et l'analyse | 2026-059 |
| 3 | Apprendre a argumenter et a convaincre | 2026-060 |
| 4 | Approfondir un ou plusieurs domaines d'expertise | 2026-061 |
| 5 | Devenir polyglotte et cosmopolite | 2026-062 |
| 6 | Comprendre la methode scientifique et experimenter | 2026-063 |
| 7 | Ecrire, transmettre, enseigner | 2026-064 |
| 8 | Relier les savoirs et vision du monde | 2026-065 |
| 9 | Cultiver l'equilibre corps-esprit | 2026-066 |

**Ecarts connus** (ne pas traiter comme nouveaux fondamentaux) :

- Etape 1 fond. 8 → fichier `02_Fonds/Culture` (2026-205).
- Etape 4 fond. 9 → `02_Fonds/Culture` (2026-173).
- Etape 8 fond. 10 → article manquant au depot.
- Doublon legacy methode scientifique : 2026-161 vs 2026-364 (canonique : **364**).
- Slugs hubs WP parfois decales vs numero d'etape Sentier (voir CSV).

---

## Ateliers deja produits (a rattacher)

| ID atelier | Titre | Fondamental parent suggere |
|------------|-------|----------------------------|
| 2026-450 | Lire une annonce medicale… | Etape 2 / #7 (2026-397) |
| 2026-456 | Lire une annonce climat… | Etape 2 / #5 (2026-399) |
| 2026-459 | Dechiffrer une annonce commerce… | Etape 2 / #5 (2026-399) |
| 2026-462 | Lire une annonce donnees sante… | Etape 2 / #5 (2026-399) |
| 2026-465 | Lire une annonce IA reglementee… | Etape 2 / #5 (2026-399) |
| 2026-453 | Expertise durable ere IA | Etape 4 / #2 (2026-382) |
| 2026-438 | Crise energetique sans court terme | Etape 8 / #9 (2026-131) |

Migration : ajouter la rubrique Ateliers sur les fondamentaux parents dans le depot ; synchronisation WordPress du fondamental a la charge de l'editeur.

---

## Liens documents

- Instructions redaction : section **3.9** dans `Instructions_editoriales_officielles.md`
- Routine : etape **4 bis** dans `Routine_quotidienne.md`
- Checklist : section **A bis** dans `Checklist_publication.md`
- En-tete article : champs `Fondamental lie`, `Type Sentier` dans `Modele_Entete_Article.md`
