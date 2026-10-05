Exécute l'**ancienne routine quotidienne (triptyque) Le Phare** de bout en bout.

1. Lis `.claude/skills/routine-triptyque/SKILL.md` et suis la checklist complète.
2. Mode **assisté** par défaut : rédige ACTU + TF + SENTIER toi-même (pas `editorial_pipeline.py` sauf si l'utilisateur a dit `api`).
3. Ne demande pas validation du sujet — choisis-le par veille web si non imposé.
4. Publie avec `python tools/daily_run.py --publish-existing "07_A_Publier/<dossier>" --keep-publish-folder` sauf si l'utilisateur a demandé brouillons seulement (`--no-publish-final`).
5. Va jusqu'au rapport final sans interaction (pas de question, pas de confirmation intermédiaire).

Si l'utilisateur a précisé un sujet ou un thème dans sa commande, respecte-le.
