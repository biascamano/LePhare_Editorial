# Rétros et traces — interne, jamais publié sur WordPress

`plan.md` D21–D22. Un fichier par semaine ISO : `YYYY-Snn.md` (ex. `2026-S42.md`), créé par la première séance de la semaine s'il manque. Mensuelle : `YYYY-MM_retro_mensuelle.md` (gabarit dans `.claude/skills/routine-mensuelle/SKILL.md`, partie A). Première rétro hebdomadaire : 2026-S42 (le 19 octobre 2026) ; première mensuelle : 2026-10. Pas de reconstitution des périodes antérieures.

**Bilan de pilote** (mode brouillons, `00_Systeme/Mode_brouillons.md`) : `YYYY-MM-DD_bilan_pilote.md`, écrit juste après les quatre activités du jour par `routine phare — bilan pilote` (gabarit dans `.claude/skills/routine-phare/SKILL.md`). Distinct de la rétro hebdomadaire, qui le lit et reprend ses recommandations dans sa table « Décisions ».

Le **journal** des séances (statuts, étapes, reprises) est `00_Systeme/Journal_phare.csv`, tenu par `tools/phare.py` ; les traces ci-dessous en sont le contenu éditorial.

## Gabarit d'un fichier de semaine

```markdown
# Semaine YYYY-Snn

## Traces de la semaine

(un bloc par séance, ajouté en fin de séance — quotidienne, rattrapage ou Fil)

## Rétro

(remplie par la rétro hebdomadaire, `routine-hebdomadaire` partie B)

### Décisions précédentes
### Mise en œuvre
### Résultats
### Problèmes et angles morts
### Ajustements proposés
### Décisions

| N° | Décision | Priorité | Échéance | État |
|---|---|---|---|---|
```

## Décisions

- N° : `D-YYYY-Snn-k` (hebdomadaire) ou `D-YYYY-MM-k` (mensuelle), conservé quand la décision est reportée.
- Priorité : **bloquante** (suspend la production jusqu'à « faite »), **importante** (affichée à chaque séance), **normale**.
- État : à faire · en cours · faite · abandonnée.
- La rétro la plus récente qui a une table porte l'état courant : `phare.py next` ne lit qu'elle. Chaque rétro reporte donc les décisions encore ouvertes, avec leur état à jour.

## Bloc de séance (sobre : une ligne par rubrique, « — » si sans objet)

```markdown
### YYYY-MM-DD — <activité : générale | curiosité | question | rattrapage | fil> — <ID ou « aucun »>

- **Sujet et raisons** : … (candidats écartés : …)
- **Regard** : général | curiosité (bloc 6, ligne …)
- **Contrôle** : autocontrôle : codes relevés (B/m) · relecteur : codes relevés (B/m), verdict · trouvé par le relecteur seul : … · introduits par une correction : … · cycles : N
- **Corrections importantes** : …
- **Décision** : publié | brouillon (motif ; pilote : « contrôle PUBLIER, retenu par le mode ») | rattrapage : action, IDs
- **Relier en retour** : fait | à faire après publication : <origine> → <ID> | —
- **Radar** : retiré … · ajouté … (P1/P2) · vers Curiosités/Archives …
- **Questions ouvertes** : …
- **À revoir** : …
- **Durée / coût** : (noté par le fondateur)
```

Ce qui est déjà ailleurs n'est pas recopié : URL et métadonnées (index), ligne d'article (mémoire §1), détail des vérifications de liens (`verify_publication.py`).
