Exécute la **routine quotidienne Le Phare** (V5) de bout en bout : le meilleur prochain article du Phare, son type choisi après le sujet ; paire Actualité + Question seulement si l'utilisateur dit `paire`.

1. Lis `.claude/skills/routine-quotidienne/SKILL.md` et suis-le.
2. Lis d'abord `00_Systeme/Etat_editorial_courant.md` puis `00_Systeme/Radar_editorial.md` ; la veille web vient ensuite.
3. Rédige toi-même (pas `editorial_pipeline.py` sauf si l'utilisateur a dit `api`).
4. Publie, relie, puis `memoire_append.py`, mise à jour du Radar et `build_etat_courant.py`.
5. Va jusqu'au rapport final sans interaction. Brouillons seulement si demandé (`--no-publish-final`).

Si l'utilisateur a précisé un sujet, un thème, un type ou une contrainte, respecte-la.
