# Memo - prompts courts pour la routine quotidienne

## Principe

Le projet doit pouvoir fonctionner avec des prompts tres courts.

Exemples attendus :

- `routine quotidienne`
- `routine quotidienne api`
- `triptyque`
- `triptyque api`
- `routine quotidienne sur ...`
- `micro-edition`

L'assistant ne doit pas demander a l'utilisateur de reexpliquer les preferences deja fixes dans le projet.

## Defauts a appliquer

- Pas d'Ollama local par defaut pour la redaction.
- Redaction assistee par l'assistant, avec vraie qualite editoriale.
- Pas d'appel API LLM par defaut pour la redaction.
- Le backend API compatible OpenAI reste une option technique explicite, pas le mode normal.
- Respect de `Instructions_editoriales_officielles.md`.
- Choix du sujet direct si aucun sujet n'est fourni.
- Pas de demande de validation du sujet avant redaction.
- Production de bout en bout jusqu'au brouillon WordPress.
- Micro-edition finale incluse par defaut.
- Bloc `Reperes de sources` avec URLs cliquables quand elles existent.
- Maillage interne du triptyque apres push WordPress.
- Controle final par l'utilisateur directement dans WordPress.

## Sortie attendue pour `routine quotidienne`

1. Choisir le sujet.
2. Rediger le triptyque `ACTU + TF + SENTIER`.
3. Faire la micro-edition.
4. Ajouter les sources cliquables.
5. Integrer les fichiers localement.
6. Mettre a jour `index_editorial.csv`.
7. Copier dans `07_A_Publier`.
8. Pousser les brouillons WordPress.
9. Ajouter les liens internes du triptyque.

## Variante explicite

Si l'utilisateur demande explicitement :

- `routine quotidienne api`
- `triptyque api`

alors le pipeline technique avec backend API peut etre utilise volontairement.

Sinon, le mode normal reste :
- redaction par l'agent
- scripts utilises surtout pour integration, push WordPress et maillage

## Rappel

Si une preference importante apparait en conversation et doit servir plus tard, elle doit etre integree dans :

- `.cursor/rules/`
- `00_Systeme/Routine_quotidienne.md`
- ou un memo de fonctionnement comme celui-ci

Le but est de reduire la longueur des prompts futurs, pas de reposer sur la memoire implicite de la conversation.
