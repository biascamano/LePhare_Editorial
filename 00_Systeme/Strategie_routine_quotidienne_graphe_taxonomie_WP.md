# Strategie - Routine quotidienne, graphe de savoir et taxonomie WordPress

> **Routines v3 (depuis 2026-10-05)** : quotidienne = **un** article + Question du Phare ; hebdomadaire = Fil du Phare ; mensuelle = dossiers, textes fondateurs, ateliers Sentier, synthese. Le triptyque `ACTU + TF + SENTIER` devient la **routine triptyque** (archive, declenchement explicite). Reference : `plan.md` (racine). Dans ce fichier, « triptyque » vaut pour la routine triptyque ; pour la quotidienne v3, lire « un article ». La logique graphe / Sentier / taxonomie reste valable pour les trois routines.

## Positionnement

**Production quotidienne** : **un article** par jour (routine quotidienne v3, `plan.md`) ; le **triptyque** (`ACTU + TF + SENTIER`) reste disponible via la **routine triptyque** (agent-first, qualite editoriale, micro-edition, integration, brouillons WordPress, maillage).

**Construction dans le temps** : chaque triptyque **ajoute une maille** a l'**architecture editoriale** du Phare : ce n'est pas obligatoirement un gros dossier multi-triptyques, mais une **accumulation ordonnee** de noeuds (concepts), de contenus et de liens.

Trois objectifs imbriques :

1. **Encyclopedie du savoir relatif et absolu**  
   - *Relatif* : l'actualite, le contexte, l'evenement (souvent porte par l'ACTU).  
   - *Absolu* : references durables, concepts, textes fondateurs, methodes (souvent portes par le TF et le SENTIER).  
   Au fil des jours, le site **densifie** une base lisible et reliable.

2. **Enrichir le Sentier du Savoir**  
   Chaque triptyque **ancre explicitement** une (ou plusieurs) **posture(s) / etape(s)** du Sentier dans les en-tetes et le corps. Le graphe gagne une dimension **pedagogique** stable.

3. **Moteur editorial du Phare**  
   Meme rythme (un triptyque), mais **sujets choisis** pour servir la coherence globale : themes, concepts manquants, fils rouges, reprises intelligentes.

---

## Comment choisir les sujets (pour l'agent)

Sans imposer une validation utilisateur avant redaction (comme la routine actuelle), l'agent **oriente** le choix du jour vers :

| Priorite | Intention |
|----------|-----------|
| **Nouveaux noeuds** | Sujets qui introduisent un **concept** ou un **angle** peu encore traites dans l'index recent. |
| **Renforcement du graphe** | Sujets qui **relient** deux domaines deja presents (ex. economie + geopolitique + methode). |
| **Rotation du Sentier** | Varier les **etapes du Sentier** dans le temps pour equilibrer le parcours global. |
| **Rotation thematique** | Alterner MONDE, ECON, TECH, CLIMAT, SCIENCE, CULTURE, POL pour eviter l'enfermement thematique. |
| **Profondeur** | Revenir sur un theme deja aborde avec un **angle distinct** (nuance, mise a jour, contre-recit) plutot que dupliquer. |
| **Durable** | Privilegier les sujets avec **potentiel d'outils de lecture** et de references reutilisables. |

Ce n'est pas une liste de scores automatique : c'est une **grille de decision** a appliquer lors du choix du sujet du jour.

---

## Categories et tags WordPress : role dans le graphe

Les champs `Categorie_WP` et `Tags_WP` dans `index_editorial.csv` (puis sur WordPress) servent a :

- **naviguer** le site comme une base de connaissances ;
- **retrouver** les contenus par grand domaine et par **concept** ;
- **relier** les articles entre eux (maillage + filtrage).

### Categories (peu nombreuses, stables)

**Reference detaillee et regles triptyque** : `00_Systeme/Taxonomie_WordPress_le-phare_info.md` (six familles, correspondance routines / types, couches de tags).

En resume : une **categorie principale** par article ; le depot peut servir de **contrat** avant alignement complet avec l'admin WordPress. Si la strategie du site change, mettre a jour la taxonomie puis les champs `Categorie_WP` / `Tags_WP` dans l'index.

### Tags (vocabulaire du graphe)

**Detail des couches** (theme, pilier Sentier, concepts, postures optionnelles) : `00_Systeme/Taxonomie_WordPress_le-phare_info.md`.

Principes : **4 a 8 tags** par article, slugs stables, **concepts reutilisables** plutot que tags uniques ; le theme editorial et l'ancrage Sentier structurent la navigation long terme.

---

## Lien avec l'architecture editoriale

L'**architecture editoriale** (noeuds, tensions, parcours) se **construit progressivement** :

- un triptyque = **un increment** minimal publiable ;
- la repetition = **graphe** ;
- la taxonomie WordPress = **couche de navigation** et de recherche alignee sur ce graphe.

On ne doit pas obligatoirement produire un manifest `architecture_editoriale` chaque jour : le **plan** peut rester implicite dans le choix du sujet + les tags + le Sentier.

---

## Amelioration continue et agilite

Objectif : garder le **meme rythme editorial** (triptyque + verification dans WordPress) tout en **ajustant souvent et peu** le process, sans lourd bureaucratisme.

### Definition rapide (qualite)

- **Pret a lancer `daily_run`** : trois `.md` dans `07_A_Publier/<dossier>/`, en-tetes alignes avec `index_editorial.csv`, blocs `Reperes de sources` avec URLs cliquables quand c'est possible.
- **Termine** : publication verifiee sur le site (ou en admin) ; la ligne d'index reflete les URLs / slugs a jour.

### Boucle courte (apres verification WP)

Environ **deux minutes**, une fois par semaine (ou apres une semaine chargee) : ouvrir une copie du gabarit `00_Systeme/Retro_routine_hebdo_TEMPLATE.md`, renommer ou dupliquer avec la date, et noter :

1. une chose qui a bien fonctionne ;
2. une friction (outil, taxonomie, doublon WP, temps de relecture, etc.) ;
3. **une seule** action pour la semaine suivante (priorisee).

### Rythme adaptable

- **Defaut** : un article par jour (routine quotidienne v3), un Fil du Phare par semaine, une consolidation par mois.
- **Sans culpabiliser le calendrier** : jour dedie au maillage transversal, mise a jour d'un pilier Sentier, ou triptyque « allonge » (ACTU courte + renvoi vers fond existant + Sentier cible) si la charge ou le sujet l'exigent.

### Experimentation

Changer **une variable a la fois** sur une courte periode (format ACTU, densite de liens internes, angle Sentier), avec un critere de succes simple (temps de verification WP, clarte du maillage, coherence des tags). Si le gain est net, mettre a jour les instructions ou la taxonomie ; sinon revenir en arriere.

### Sources de backlog « process »

- Logs `00_Systeme/Logs/daily_run_YYYY-MM-DD.log` (erreurs recurrentes, surprises WP/index).
- `index_editorial.csv` : trous de concepts, desequilibre de themes ou de piliers Sentier.
- Ce fichier : faire evoluer le tableau **Comment choisir les sujets** quand une priorite editoriale change.

---

## Fichiers de reference

- Plan de reference des routines : `plan.md` ; skills `.claude/skills/routine-{quotidienne,hebdomadaire,mensuelle}/SKILL.md`
- Routine triptyque (archive) : `00_Systeme/Routine_quotidienne.md`
- Strategie historique graphe / architecture : `00_Systeme/Strategie_graphe_de_savoir.md`
- Instructions redactionnelles : `00_Systeme/Instructions_editoriales_officielles.md`
- **Taxonomie WordPress alignee sur le site** (categories, tags, correspondance routines / types) : `00_Systeme/Taxonomie_WordPress_le-phare_info.md`
- **Retro hebdo (gabarit)** : `00_Systeme/Retro_routine_hebdo_TEMPLATE.md`

---

## Rappel pour l'agent (Cursor)

- Mode de production par defaut : **routine quotidienne v3** (un article), redige par l'agent ; triptyque uniquement sur demande explicite (`routine triptyque`).
- Choisir le sujet du jour en pensant **graphe de savoir**, **Sentier**, **coherence des categories et tags WordPress**.
- Ne pas lancer `editorial_pipeline.py` comme moteur de redaction sans demande explicite API.
- Pour l'**amelioration continue** : si l'utilisateur ouvre une retro de la semaine, en tenir compte pour ajuster le choix de sujet, les tags ou une friction process (voir section **Amelioration continue et agilite** ci-dessus).
