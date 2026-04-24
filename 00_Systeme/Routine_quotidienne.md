# Routine quotidienne Le Phare

## Objectif

Executer de bout en bout une routine editoriale assistee qui :

1. choisit un sujet du jour si aucun sujet manuel n'est fourni
2. redige manuellement un triptyque `ACTU + TF + SENTIER` selon les instructions editoriales
3. applique une micro-edition finale sur les 3 textes
4. ajoute des `Reperes de sources` avec URLs cliquables quand elles sont disponibles
5. cree les fichiers locaux
6. met a jour `index_editorial.csv`
7. copie dans `07_A_Publier`
8. pousse les brouillons dans WordPress
9. applique le maillage interne automatique du triptyque

## Fichiers

- `tools/daily_run.py`
- `tools/daily_run.cmd`
- `tools/editorial_pipeline.py`
- `tools/wp_push_draft.py`
- `tools/post_linking.py`

## Choix du sujet

Par defaut, la routine choisit directement un sujet pertinent via veille web ou flux d'actualite.

Le sujet n'est pas soumis a validation utilisateur avant redaction : la routine va jusqu'au brouillon WordPress, puis l'utilisateur verifie le resultat dans WordPress.

**Objectif long terme (graphe de savoir + Sentier + moteur editorial)** : le sujet du jour doit aussi **construire petit a petit l'architecture editoriale** du Phare : nouveaux concepts, liens entre themes, rotation des etapes du Sentier, categories et tags WordPress coherents. Strategie detaillee :

- `00_Systeme/Strategie_routine_quotidienne_graphe_taxonomie_WP.md`

Source possible de veille :

- `https://news.google.com/rss?hl=fr&gl=FR&ceid=FR:fr`

Puis elle :
- score les sujets selon les themes du Phare
- ignore les sujets peu pertinents
- evite de reutiliser les sujets recents quand c'est possible
- privilegie les sujets offrant un potentiel d'analyse durable
- applique la grille de choix (noeuds, Sentier, taxonomie) decrite dans la strategie ci-dessus lorsque l'assistant selectionne le sujet

## Lancement manuel

```bash
python tools/daily_run.py
```

## Lancement manuel avec sujet impose

```bash
python tools/daily_run.py --topic "Guerre usa israel iran" --theme POL
```

## Lancement sans push WordPress

```bash
python tools/daily_run.py --no-publish-drafts
```

## Workflow editorial reel

1. Choisir le sujet sans demander une validation intermediaire.
2. Rediger les 3 articles directement avec l'assistant.
3. Faire une micro-edition finale :
   resserrer les phrases, lisser le ton, verifier SEO, titres, transitions et fins d'articles.
4. Completer les blocs `Reperes de sources` avec des liens explicites vers les sources utilisees.
5. Integrer les fichiers dans les bons dossiers.
6. Dupliquer dans `07_A_Publier`.
7. Pousser les brouillons WordPress.
8. Ajouter les liens internes du triptyque.
9. Laisser l'utilisateur controler le resultat final dans WordPress.

## Logs

Chaque execution cree :

- `00_Systeme/Logs/daily_run_YYYY-MM-DD.log`
- `00_Systeme/Logs/daily_run_YYYY-MM-DD.json`

Le fichier JSON stocke :
- le sujet retenu
- le theme
- le statut
- stdout/stderr du pipeline

## Tache planifiee Windows

Nom de la tache :

- `LePhareRoutineQuotidienne`

Horaire :

- tous les jours a `04:00`

Commande executee :

- `D:\workspaces\LePhare_Editorial\tools\daily_run.cmd`

## Garde-fous

- une execution reussie par jour maximum, sauf avec `--force`
- publication WordPress en brouillons uniquement
- logs persistants

## Limites actuelles

- le choix du sujet reste perfectible
- les liens vers d'anciens articles pertinents ne sont pas encore automatiques
- la verification finale editoriale se fait dans WordPress par l'utilisateur
