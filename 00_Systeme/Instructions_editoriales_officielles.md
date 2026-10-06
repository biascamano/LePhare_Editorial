# Instructions editoriales officielles - Le Phare

## 1) Vision et objectifs

> Ligne editoriale de reference : `SOCLE ÉDITORIAL CONSOLIDÉ — LE PHARE INFO.docx` (racine). Le present document regle la qualite redactionnelle. Routine quotidienne = paire A (Actualite) + B (Question du Phare) : exigences dans `plan.md` §5.6 a §5.8. En cas d'ecart entre les deux documents, le signaler plutot que trancher.

Le media suit une approche de slow journalism :

- produire du savoir durable et de l'analyse de fond,
- eviter la reaction a chaud et le sensationnalisme,
- relier l'actualite au Sentier du Savoir.

Objectifs principaux :

- synthetiser l'actualite avec analyse multi-sources,
- relier chaque sujet aux etapes/fondamentaux du Sentier,
- creer des ressources pedagogiques durables et accessibles,
- encourager la reflexion critique (infographies, fiches, dossiers),
- rester independant (sans pub, sans course au clic).

## 2) Referentiel categories + Sentier

Chaque article est classe dans une categorie thematique :

- Monde
- Politique & Societe
- Economie & Finance
- Technologie & IA
- Environnement & Climat
- Science & Sante

En parallele, l'article peut etre rattache au Sentier du Savoir :

- Etapes 1 a 9
- Bonus : Art de la memoire

Un article peut donc exister a la fois dans un flux thematique et dans une etape du Sentier.

## 3) Structure de production des articles

Chaque article suit une **structure logique** (meme fil) mais **pas un canevas visuel fige** : le lecteur doit retrouver sans peine ou sont le cadrage, les faits, la nuance critique, les pistes et la cloture, sans que tous les textes du site aient les memes cinq titres de section.

1. Titre principal (H1), clair, impactant, SEO-friendly
2. Contexte (fonction : pourquoi ce sujet maintenant, pour qui)
3. Donnees et tendances (fonction : faits, ordres de grandeur, comparaisons utiles)
4. Decryptage des biais (fonction : angles morts, lectures concurrentes, pieges de lecture)
5. Solutions et initiatives (fonction : leviers, limites, ce qui change ou non)
6. Conclusion (fonction : synthese, lien Sentier, ouverture)

### 3.0 Souplesse de forme (lisibilite et interet)

Les six points ci-dessus decrivent le **contenu a couvrir**, pas des **intitules obligatoires** a recopier mot pour mot d'un article a l'autre.

- Formuler les **H2 / H3** dans un **langage concret** lie au sujet (eviter la repetition mecanique des memes libelles generiques sur tout le depot).
- **ACTU** : un fil chronologique, une tension (decision / contre-decision) ou une question dominante peut structurer le texte autant qu'une liste « premier / second biais ».
- **TF** : la progression peut suivre l'auteur, une these, une epoque ou un paradoxe plutot qu'une grille administrative symetrique.
- **SENTIER** : privilegier l'**outil** (grille, questions, mini-cas, erreurs frequentes) plutot que cinq chapitres paralleles peu denses.

Rester **sobre** : pas d'effet « magazine » artificiel ; l'interet vient de la **precision**, du **contrepoint** et du **lien** au parcours du lecteur.

### 3.1 Contexte

- importance du sujet,
- mise en perspective historique/scientifique,
- lien explicite avec une etape/fondamental du Sentier.

### 3.2 Donnees et tendances

- chiffres clefs,
- comparaisons (regions, periodes, contextes),
- cas concrets.

### 3.3 Decryptage des biais

- biais mediatiques et politiques,
- interpretations concurrentes,
- lien avec la pensee critique (Etape 2).

### 3.4 Solutions et initiatives

- innovations politiques/sociales/scientifiques,
- actions collectives possibles,
- limites des solutions.

### 3.5 Images

Chaque article peut avoir une **image WordPress de presentation** (a la une / cartes / partage social), **sans** l'inserer dans le corps du texte si tu utilises la carte `tools/wp_featured_media.local.json` : pour l instant on **cartographie surtout les tags** (`by_tag_slug`, themes et familles stables) ; categorie optionnelle. Valeurs : ID numerique ou nom de fichier du media deja en ligne (ex. `economie.png`).

Pour le corps editorial et les legendes, tu peux toujours garder une suggestion dans le bloc « Bloc image WordPress » du Markdown ; la generation unitaire (IA ou banque d'images) reste **optionnelle** lorsque la featured image commune couvre la presentation.

Si tu produis une image dediee :

- format : 1792x1024 px
- extension : .jpg
- style : sobre, percutant, sans surcharge ni texte inutile
- source : IA ou libres de droit
- usage : image de tete + legende adaptee

### 3.6 Conclusion

- synthese des points clefs,
- lien clair au Sentier (competence/etape/fondamental),
- question ouverte.

### 3.7 Phase de calibrage par type (longueur, densite, qualite)

Apres la redaction et une **micro-edition** sur les trois textes du triptyque, une phase **dediee au calibrage** est **systematique** : ajuster **volume**, **densite d'argument** et **niveau de detail** selon le **Type** declare dans les metadonnees (`ACTU`, `TF`, `SENTIER`). Elle est executee **automatiquement** avant mise en `07_A_Publier`, **sans demander une validation prealable** pour savoir si elle doit avoir lieu. L'objectif est la **qualite percue par un lecteur engage**, pas un score SEO ou un compteur de mots.

Pour cette passe, privilegier un **modele Cursor / agent a forte capacite de revision long-form** (par exemple **Claude Sonnet 4.6** ou **GPT-5.5** ou leur successeur direct), mieux a meme que les modeles legers de preserver nuances et faits tout en resserrant la forme.

**Cibles indicatives (repères de lecture, pas des obligations rigides)**

| Type | Role | Longueur indicative | Priorite qualite |
|------|------|----------------------|------------------|
| **ACTU** | Decrypter le signal, contextualiser, renvoyer au Sentier | ~650–1100 mots | Une question dominante, sources identifiables, pas d'allonge artificielle |
| **TF** | Ancrage durable, nuances historiques ou conceptuelles | ~900–1600 mots (selon matiere) | Proposition claire, citations/sources propres, pas de catalogue gratuit |
| **SENTIER** | Outil reutilisable (grille, methode, posture) | ~900–1400 mots | Le lecteur sait **quoi faire** ou **comment lire** apres la lecture ; exemple ou mini-cas |

Si un texte est **nettement sous** la zone basse pour son type **et** que la promesse editoriale n'est pas tenue (outil incomplet, contexte trop thin), **enrichir** avec du contenu utile (precision factuelle, exemple, contre-exemple, limite des solutions). Si un texte **depasse** la zone haute sans ajouter de valeur, **couper** ou **deporter** vers une suite / un autre volet.

**Densité SENTIER — 3 consignes de rédaction (V2)**

Ces trois points s'appliquent **pendant la rédaction initiale** et **pendant la passe de calibrage**. Un SENTIER qui ne les respecte pas doit être enrichi avant mise en `07_A_Publier`.

1. **Ancrer le mini-cas ou l'exemple sur l'ACTU réelle du triptyque** — pas un exemple fictif générique (« imaginez un titre du type… »). Utiliser les faits, dates, protagonistes et sources déjà posés dans l'ACTU du jour. Le lecteur doit reconnaître le sujet qu'il vient de lire.

2. **Nommer au moins 2 sources concrètes dans le mini-cas** — pas « la source A » / « la source B », mais une dépêche identifiée, un communiqué institutionnel précis, un article de presse nommé. Pour chaque source : ce qu'elle dit, ce qu'elle ne dit pas, et pourquoi le lecteur doit affiner sa lecture avant de partager.

3. **Résoudre chaque item de la grille avec au moins une application sur le sujet** — chaque question ou point de méthode de la grille SENTIER doit avoir une illustration directe tirée de l'ACTU du jour, pas une formulation abstraite valable pour n'importe quel sujet. Une grille générique non ancrée ne tient pas la promesse de l'atelier.

**Garde-fous (toujours)**

- Ne pas diluer pour les plugins SEO ; le volume sert la **promesse** du format.
- Preserver les faits, dates, liens et `Repères de sources` ; toute compression doit rester **exacte**.
- Garder le **fil logique** (cadrage, faits, nuances, pistes, cloture) ; les **titres et le decoupage** des sections sont **libres** s'ils servent le sujet et la promesse du type (ACTU / TF / SENTIER). Eviter le formatage « meme grille visualisable partout » qui lasse le lecteur.

**Execution par defaut (assistant Cursor)**

La revision/calibrage est faite **par l'assistant dans la meme conversation**, sans API HTTP obligatoire. Consigne minimale integree dans la passe :

- type d'article (`ACTU` / `TF` / `SENTIER`) et **promesse au lecteur** ;
- respect strict des **sources et faits** ; pas d'invention ;
- objectif : **longueur et densite** alignees sur le tableau ci-dessus, ton Le Phare (slow journalism, pas sensationnaliste) ;
- pour un **SENTIER** : verifier les **3 consignes de densite** ci-dessus avant de valider la passe ;
- **forme** : titres de sections **adaptes au sujet** (pas la meme grille generique d'un triptyque a l'autre) ; voir **3.0 Souplesse de forme** ;
- sortie : Markdown coherent avec les chemins canoniques du depot ; la **responsabilite finale** (exactitude, ton, publication) reste celle de la redaction / de l'assistant principal du depot.

**Option reviseur API (hors session Cursor)**

Si `calibration_api_enabled` est `true` dans `tools/editorial_config.local.json` **et** que les scripts du depot invoquent cette option, une passe HTTP peut compléter le calibrage ; elle reste **desactivee par defaut** et **sans appel silencieux** lorsque l'indicateur est absent ou `false`.

### 3.8 Couche « Le Phare » sur l'ACTU (cadre institutionnel, loi, technique)

En complement de la **souplesse de forme** (3.0) et du **calibrage** (3.7), pour les sujets **lourds en documents officiels** (Union europeenne, reglementation, grands plans numeriques ou sanitaires), viser une **lecture engagee** sans quitter le slow journalism :

- **Accroche** : une **scene ou une paire de questions** concretes (citoyen, soignant, chercheur, territoire) plutot qu'une ouverture uniquement « l'Union a decide… ».
- **Tension** : formuler explicitement le **paradoxe** ou le **risque** utile au lecteur (ex. mieux faire circuler les donnees **sans** deposseder ; promesse transfrontiere **vs** delais reels) — **sans** polemique gratuite ni titre-rubrique sensationnaliste.
- **Terminologie** : aligner les libelles sur les **sources primaires** (institutions, JO, glossaires officiels) ; eviter les glissades de traduction (ex. distinguer resume patient, compte rendu de sortie, categories de donnees et **dates** associees quand le texte les fixe).
- **Calendrier** : lorsque l'actualite repose sur des **jalons** officiels, les presenter en **dates precises** (tableau ou liste datee), pas seulement sous une formule vague du type « plus tard » ou « a moyen terme » sans repere.
- **Encadres utiles** (optionnels, si la matiere s'y prete) : par exemple **ce que le dispositif ne fait pas** (anti-amalgame mediatique) et **ce que le citoyen pourra encadrer ou refuser** (sous reserve des actes d'execution), sans inventer de droits absents des sources citees.
- **Sentier** : le lien avec l'**etape** ou la **posture** du Sentier doit se **lire dans le corps** (chapou ou developpement), pas seulement comme un **bloc final** colle au triptyque.

Ces reperes s'appliquent surtout a l'**ACTU** ; le **TF** et le **SENTIER** gardent leurs promesses propres (3.7), avec la meme exigence de **clarte** et de **non-faux resume institutionnel**.

### 3.9 Ancrage fondamental et rubrique Atelier (triptyques)

Chaque triptyche produit un article **SENTIER** qui est, par defaut, un **atelier** : application d'un **fondamental existant** (parmi les 10 de l'etape) a l'actualite du jour. On **ne cree pas** un nouveau fondamental a chaque triptyque.

**Referentiel obligatoire** : `00_Systeme/Manifests/sentier_fondamentaux.csv` (colonnes `url_canonique`, `nom_fichier`) et guide `00_Systeme/Sentier_fondamentaux_referentiel.md`. **Exclure** les articles dont l'URL contient `wiki-du-phare` (doublons Echo KB) — voir `00_Systeme/Sentier_dedoublonnage_wiki.md`.

**Apres redaction du SENTIER** (avant ou juste apres calibrage 3.7, avant copie `07_A_Publier`) :

1. Choisir `etape_num` + `fondamental_num` + `fondamental_id` dans le CSV.
2. Renseigner l'en-tete SENTIER : `Type Sentier : atelier`, `Fondamental lie (ID)`, `Fondamental numero`, `Posture Sentier` (libelle affiche, ex. « Mettre a distance »).
3. Mentionner le fondamental parent en chapo ou premiere section (titre + lien WP si connu).
4. Ajouter ou mettre a jour, **en fin du fichier Markdown du fondamental parent**, la section :

```markdown
## Ateliers (applications sur l'actualite)

| Date | Triptyque | Atelier (SENTIER) |
|------|-----------|-------------------|
| YYYY-MM-DD | Titre du triptyque | [Titre atelier](URL) (`ID`) |
```

5. Index : `Etape_sentier` + tag ou remarque `atelier-sentier` + reference au fondamental parent.
6. **WordPress — fondamental parent** : apres `daily_run --publish-existing`, la mise a jour du **corps** du fondamental parent sur le site (pour afficher la table `## Ateliers`) est **a la charge de l'editeur** ; l'assistant ne lance pas ce push (commande et prerequis `Slug propose` : `Sentier_fondamentaux_referentiel.md` §5).
7. **WordPress — SENTIER atelier** : l'assistant peut repousser le **corps** du SENTIER atelier seul avec `python tools/wp_refresh_body.py "<chemin>"` sur le `.md` canonique du Sentier quand le fichier a ete retouche apres publication ou pour aligner WP sur le depot — **jamais** sur le fondamental parent. Voir `Sentier_fondamentaux_referentiel.md` §5. Ne pas pousser les doublons `wiki-du-phare` ; **desactivation des doublons sur WP = editeur** (`Sentier_dedoublonnage_wiki.md`).

L'**ACTU** et le **TF** du triptyque renvoient a la meme etape / fondamental en conclusion ; seul le SENTIER porte la grille operatoire detaillee.

### 3.10 Liens cliquables — `Repères de sources` et `Dans ce triptyque`

Les fichiers `.md` utilisent le Markdown converti par `wp_push_draft.py` : seuls les liens `[texte](url)` deviennent des hyperliens cliquables sur WordPress. **Ne pas** coller une URL nue apres un libelle.

**`## Repères de sources`** — chaque entree doit etre cliquable :

```markdown
- Parlement européen, budget 2026 : [dossier de presse PE](https://www.europarl.europa.eu/...)
```

**A eviter** (URL en dur, non cliquable apres push) :

```markdown
- Parlement européen, budget 2026 : https://www.europarl.europa.eu/...
```

**`## Dans ce triptyque`** — le libelle d'orientation reste en **texte brut** ; seul le **titre de l'article lie** est dans le lien :

```markdown
- Approfondir avec le texte fondateur : [Fritz Scharpf : le « piège des décisions conjointes »…](https://le-phare.info/?p=4235)
- Prolonger avec le Sentier du Savoir : [Argumenter sur un budget européen sans se laisser enfermer…](https://le-phare.info/?p=4236)
```

**A eviter** (toute la ligne dans le crochet, y compris « Approfondir… » / « Prolonger… ») :

```markdown
- [Approfondir avec le texte fondateur : Fritz Scharpf : …](https://le-phare.info/?p=4235)
```

Meme logique pour **Revenir à l'actualité** sur TF et SENTIER. A l'avenir, aligner `tools/post_linking.py` sur ce format lors du maillage automatique.

## 4) Verification et mise a jour

- recherche web systematique avant publication,
- enrichissement Sentier pour les contenus relies,
- revisions regulieres si l'actualite evolue,
- double verification des sources (geopolitique, economie, sciences).

## 5) Format et optimisation WordPress

Les articles doivent etre prets a publier :

- SEO integre (mots-cles + meta description 150-160 caracteres),
- hierarchie H2/H3 propre, avec des **intitules lies au sujet** (pas seulement des etiquettes generiques repetees),
- liens internes (Sentier + autres articles Le Phare),
- liens externes fiables (officiels, academiques, presse internationale),
- texte final sans Markdown dans la version publiee WordPress.

**Depot (fichiers `.md`)** : le corps peut utiliser un **Markdown restreint** converti par `tools/wp_push_draft.py` lors du push : titres `#` / `##` / `###`, listes `-` ou `1.`, liens `[texte](url)`, gras `**texte**` (genere `<strong>` en HTML). Ce n'est pas un moteur Markdown complet (pas de tableaux GFM, italique `*`, etc. dans le convertisseur actuel — les tableaux en `.md` peuvent necessiter un bloc HTML ou une mise en forme manuelle cote WP si le rendu ne suffit pas).

**Graisse (`**…**`)** : sur WordPress tout `**` devient du gras ; un usage trop frequent lasse et fait perdre la hierarchie visuelle. Reserver le gras a peu d'elements par texte : une tension ou formule porteuse, un jalon ou une date qui concentrent l'enjeu, un terme juridique a ne pas confondre (une fois), eventuellement la phrase de these en conclusion — pas une emphase sur chaque notion ni sur toutes les puces d'une liste. Viser au plus une ou deux plages `**` par paragraphe de corps en moyenne (hors un seul intitule d'encadre si utile).

## 6) Cohérence editoriale

- Articles d'actualite : relies au Sentier comme cas pratiques.
- Fondamentaux du Sentier : ~1200 mots, structures en dossiers ; rubrique finale **« Ateliers (applications sur l'actualite) »** listant les SENTIER des triptyques (voir 3.9).
- Ateliers (SENTIER de triptyque) : outils reutilisables sur l'actu, rattaches a un fondamental parent ; pas de 11e pilier dans la sidebar.
- Hubs d'etapes : pages synthetiques (10 fondamentaux + objectifs + contributions).
- Syntheses visuelles : tableaux/infographies par etape.

Objectif global :

Allier decryptage utile de l'actualite et progression du lecteur vers l'erudition.
