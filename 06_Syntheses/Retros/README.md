# Rétros et traces — interne, jamais publié sur WordPress

`plan.md` D21. Un fichier par semaine ISO : `YYYY-Snn.md` (ex. `2026-S42.md`), créé par la première séance de la semaine s'il manque. Mensuelle : `YYYY-MM_retro_mensuelle.md` (lot 2).

## Gabarit d'un fichier de semaine

```markdown
# Semaine YYYY-Snn

## Traces de la semaine

(un bloc par séance, ajouté en fin de séance — quotidienne ou rattrapage)

## Rétro

(remplie par l'hebdomadaire : décisions antérieures reprises et vérifiées, ce qui a réellement changé)
```

## Bloc de séance (sobre : une ligne par rubrique, « — » si sans objet)

```markdown
### YYYY-MM-DD — <activité : générale | curiosité | question | rattrapage> — <ID ou « aucun »>

- **Sujet et raisons** : … (candidats écartés : …)
- **Regard** : général | curiosité (bloc 6, ligne …)
- **Contrôle** : auto : codes relevés · relecteur : codes relevés · divergences : … · cycles : N
- **Corrections importantes** : …
- **Décision** : publié | brouillon (motif) | rattrapage : action, IDs
- **Radar** : retiré … · ajouté … (P1/P2) · vers Curiosités/Archives …
- **Questions ouvertes** : …
- **À revoir** : …
- **Durée / coût** : (noté par le fondateur)
```

Ce qui est déjà ailleurs n'est pas recopié : URL et métadonnées (index), ligne d'article (mémoire §1), détail des vérifications de liens (`verify_publication.py`).
