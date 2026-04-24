# Taxonomie WordPress - reference canonique projet Le Phare Editorial

Ce document fixe la **meilleure structure pour l'objectif** : construire petit a petit un **graphe de savoir**, nourrir l'**encyclopedie** (savoir relatif + absolu), le **Sentier du savoir** et le **moteur editorial**, tout en restant compatible avec la publication sur [le-phare.info](https://le-phare.info/).

**Tu peux ajuster la strategie du site et les categories/tags WordPress** : quand le site diverge, mets a jour ce fichier ou les champs `Categorie_WP` / `Tags_WP` dans `index_editorial.csv` pour **realigner**. Ce depot reste la **source de verite** pour la redaction et les scripts.

---

## 1. Objectif prioritaire (pourquoi ces regles)

| Objectif | Ce que la taxonomie doit permettre |
|----------|-----------------------------------|
| Graphe de savoir | Retrouver et relier les **concepts** dans le temps (tags stables + reutilisation). |
| Encyclopedie | Separer **actualite** (relatif) et **fond / methode** (plus absolu) via **categories** claires. |
| Sentier | Chaque contenu **ancre** une posture ou un theme Sentier **dans les tags**, pas seulement dans le texte. |
| Moteur editorial | Peu de categories, vocabulaire de tags **discipline** pour eviter le bruit. |

---

## 2. Categories WordPress : cinq familles seulement

**Une categorie principale par article.** Pas de double categorie pour un meme post dans la logique redactionnelle (le site peut avoir des plugins ; ici on simplifie).

| # | Categorie (slug conseille) | Quand l'utiliser |
|---|----------------------------|------------------|
| 1 | **actualites** | ACTU, decryptages, faits contextualises. |
| 2 | **textes-fondateurs** | TF, lectures d'auteurs, concepts ancres par une reference. |
| 3 | **sentier-du-savoir** | SENTIER, exercices de methode, outils cognitifs, articles du parcours Sentier. |
| 4 | **dossier-hebdomadaire** | DOSSIER, series, volets d'un dossier nomme (hors triptyque simple). |
| 5 | **le-phare** | Pages institutionnelles, charte, methode (rarement des articles de fond). |

**Triptyque quotidien (regle fixe)** :

| Volet | Categorie WP |
|-------|--------------|
| ACTU | actualites |
| TF | textes-fondateurs |
| SENTIER | sentier-du-savoir |

Si WordPress impose un libelle legerement different (accents, pluriel), **garde** la correspondance dans l'index avec le slug reel du site.

---

## 3. Tags : quatre couches (empilement)

Les tags servent le **graphe**. Ordre de priorite quand tu en remplis :

### Couche A — Theme editorial (obligatoire pour un triptyque)

Un tag issu du **theme** Le Phare (aligne sur `Theme` dans l'index) :

| Code index | Tag slug |
|------------|----------|
| MONDE | `monde` |
| POL | `politique-societe` |
| ECON | `economie-finance` |
| TECH | `technologie-ia` |
| CLIMAT | `environnement-climat` |
| SCIENCE | `science-sante` |
| CULTURE | `culture-philosophie` |

### Couche B — Pilier Sentier (obligatoire pour SENTIER ; recommande pour ACTU/TF si le sujet s'y prete)

Un parmi les **huit themes** Sentier du site :

`sentier-culture` | `sentier-critique` | `sentier-approfondissement` | `sentier-langues` | `sentier-science` | `sentier-transmission` | `sentier-vision` | `sentier-equilibre`

### Couche C — Concepts (cœur du graphe)

2 a 5 tags **reutilisables** : mots du sujet qui pourront servir a d'autres articles (`inflation`, `biais-cognitifs`, `transition-energetique`, `ordre-maritime`, …).  
**Slug** : minuscules, tirets, pas d'accents si possible (aligne sur les habitudes WP).

### Couche D — Meta (optionnel, avec parcimonie)

- **Posture** (les cinq temps de la methode homepage) : `posture-observer` | `posture-comprendre` | `posture-distance` | `posture-relier` | `posture-transmettre` — utile si tu veux filtrer la progression sans tout melanger dans les concepts.
- **Format** : `triptyque` si tu veux un filtre transversal (un seul tag, pas besoin de repeter par article).

**Plafond pratique** : **8 tags maximum** par article pour rester lisible ; **4 minimum** si on compte A + B + au moins 2 concepts.

---

## 4. Regles rapides par type d'article

| Type | Categorie | Tags minimum |
|------|-----------|--------------|
| ACTU | actualites | theme (A) + 2 concepts (C) ; + pilier Sentier (B) si l'article le permet |
| TF | textes-fondateurs | theme (A) + auteur ou titre d'oeuvre en concept (C) + 1 concept (C) |
| SENTIER | sentier-du-savoir | theme (A) + pilier Sentier (B) + 2 concepts (C) ; + posture (D) si pertinent |

---

## 5. index_editorial.csv et WordPress

- `Categorie_WP` : **un** libelle ou slug correspondant a la categorie principale.
- `Tags_WP` : **separateur point-virgule** `;` comme dans l'existant, dans l'ordre A puis B puis C puis D si utile.
- A la publication (`wp_push_draft.py`), les termes sont **creees ou associes** selon les slugs : garde une **cohérence** entre index et admin WP.

---

## 6. Si tu changes le site plus tard

- **Strategie editoriale** : adapte ce fichier en premier ou ajoute une section "ecarts volontaires".
- **Categories WP** : mets a jour le tableau section 2 et les regles triptyque.
- **Tags** : fusionne les doublons dans WP puis **remplace** dans l'index par lots (rechercher/remplacer prudent).

---

## 7. Liens utiles

- Site : [le-phare.info](https://le-phare.info/)
- Strategie routine + graphe : `Strategie_routine_quotidienne_graphe_taxonomie_WP.md`
- Routine quotidienne : `Routine_quotidienne.md`
