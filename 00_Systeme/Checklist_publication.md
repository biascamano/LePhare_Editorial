# Checklist publication - Le Phare

Utiliser cette checklist avant chaque publication WordPress.

## A. Positionnement editorial

- [ ] Le sujet est traite en logique slow journalism (fond, recul, contextualisation).
- [ ] L'article relie l'actualite a un savoir durable.
- [ ] Le lien au Sentier du Savoir est explicite (etape/fondamental/competence).

## A bis. Atelier Sentier (routine mensuelle, routine triptyque)

- [ ] Le SENTIER est declare `Type Sentier : atelier` (pas un nouveau fondamental).
- [ ] `Fondamental lie (ID)` et `Fondamental numero` renseignes (CSV `sentier_fondamentaux.csv`).
- [ ] Rubrique `## Ateliers (applications sur l'actualite)` mise a jour en fin du **fondamental canonique** (`02_Fonds/…`, URL racine — pas `wiki-du-phare`).
- [ ] (Routine triptyque) ACTU et TF renvoient a la meme etape / fondamental en conclusion.
- [ ] Apres `daily_run --publish-existing` : si besoin, **passe WP** `wp_push_draft --refresh-body` sur le **SENTIER atelier** uniquement (`Sentier_fondamentaux_referentiel.md` §5) — **pas** sur le fondamental parent.
- [ ] **Fondamental parent sur WordPress** : republication du corps (pour la table Ateliers) **a la charge de l'editeur** — pas d'action automatique assistant ; prerequis `Slug propose` si `wp_push_draft` : voir `Sentier_fondamentaux_referentiel.md` §5.
- [ ] Doublons KB : l'editeur met en **brouillon** les posts `/wiki-du-phare/*` (l'assistant ne le fait pas).

## B. Structure du contenu

- [ ] H1 clair, impactant, SEO-friendly.
- [ ] Section Contexte presente (enjeux + perspective historique/scientifique).
- [ ] Section Donnees et tendances (chiffres, comparaisons, cas concrets).
- [ ] Section Decryptage des biais (mediatiques/politiques/cognitifs).
- [ ] Section Solutions et initiatives (avec limites).
- [ ] Conclusion avec synthese + question ouverte.

## C. Verification et fiabilite

- [ ] Recherche web actualisee faite avant publication.
- [ ] Sources sensibles (geo, eco, science) double-verifiees.
- [ ] Les faits sont dates et sourcés.
- [ ] Les interpretations sont distinguees des faits.
- [ ] `Repères de sources` : liens `[libellé](url)` (pas d'URL nue apres « : » — voir Instructions 3.10).
- [ ] (Routines v3) Navigation finale : `Repères de sources` / `La question suivante` / `Pour aller plus loin` / `Sur le Sentier du Savoir` ; liens internes reels (index, `sentier_fondamentaux.csv`) ; **pas** de `Dans ce triptyque`.
- [ ] (Routine triptyque) `Dans ce triptyque` : libelle hors lien (`Approfondir… :`, `Prolonger… :`) ; seul le titre de l'article lie est cliquable (Instructions 3.10).

## D. SEO et WordPress

- [ ] En-tete v3 complet (`Type article`, `Question du Phare`, `Dossier`, `Article precedent (ID)`, `Prolongement envisage`) — `Modele_Entete_Article.md`.
- [ ] Bloc `# SEO` avec `Slug propose` (requis par `wp_push_draft`).
- [ ] Mot-cle principal defini.
- [ ] Meta description redigee (150-160 caracteres).
- [ ] Hierarchie H2/H3 propre.
- [ ] Liens internes ajoutes (Sentier + articles Le Phare).
- [ ] Liens externes fiables ajoutes (officiels/academiques/presse de reference).
- [ ] Texte final adapte WordPress (pas de Markdown brut a publier).

## E. Media visuel

- [ ] Image de tete preparee en 1792x1024 px.
- [ ] Format .jpg.
- [ ] Style sobre, lisible, sans surcharge.
- [ ] Legende coherente avec l'angle editorial.

## F. Classement editorial

- [ ] Categorie thematique principale assignee (Monde, POL&SOC, ECON, TECH&IA, CLIMAT, SCIENCE&SANTE).
- [ ] Etape Sentier associee (1-9 ou Bonus memoire).
- [ ] Tags coherents et reutilisables.

## G. Systeme source (obligatoire)

- [ ] En-tete article rempli dans le fichier source.
- [ ] Statut mis a jour (`pret_a_publier` -> `publie`).
- [ ] `index_editorial.csv` mis a jour (date + URL WordPress + categorie + tags).
- [ ] Version article verifiee (V1/V2...).

## H. Controle final

- [ ] Relecture orthographe/style.
- [ ] Coherence avec la charte et le ton Le Phare.
- [ ] Verification mobile (titres, longueur paragraphes, lisibilite).
- [ ] Publication validee.
