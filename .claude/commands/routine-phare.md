Exécute **l'Orchestrateur du Phare** (`plan.md` D22).

1. Lis `.claude/skills/routine-phare/SKILL.md` et suis-le.
2. Commence par `python tools/phare.py next` : la décision lui appartient. En cas d'ARRÊT, affiche le message et arrête-toi.
3. Une seule activité, exécutée avec la routine spécialisée désignée, puis `close` avec le statut réel.

Si l'utilisateur a précisé `état`, `reprendre`, `reporter`, `brouillons seulement` ou `à blanc`, respecte-le.
