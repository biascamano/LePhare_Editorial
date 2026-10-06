Exécute la **routine de rénovation Le Phare** (stock ancien, `plan.md` D17 / §19).

1. Lis `.claude/skills/routine-renovation/SKILL.md` et suis-le.
2. Régénère d'abord l'inventaire (`python tools/build_inventaire_renovation.py`), puis prends le lot ouvert le plus bas.
3. Rédige toi-même (pas `editorial_pipeline.py` sauf si l'utilisateur a dit `api`).
4. Lots 2 et 3 : va jusqu'au rapport final sans interaction. Lot 1 : propose, puis attends les décisions humaines.

Si l'utilisateur a précisé un lot, des IDs ou `à blanc`, respecte-le.
