# Gabarit — pack social pour un article

Créer un fichier `pack.md` dans `02_Contenus/a-publier/YYYY-MM-DD_slug/pack.md` en copiant ce modèle. Un pack par article publié (Actualité, Question, Application ou Texte fondateur).

---

## Métadonnées

| Champ | Valeur |
|-------|--------|
| Date publication WP | |
| ID | `2026-___` |
| Type | Actualité / Question / Application / Texte fondateur |
| Thème | |
| URL article | |
| Question du Phare | |
| Article suivant (si la question a été traitée) | |
| Sentier (fondamental lié) | |
| Statut pack | brouillon / prêt / publié |

URLs : lues dans `index_editorial.csv` (`python tools/index_lookup.py <ID>`), jamais de lien `?p=`.

---

## LinkedIn — l’article (J+1)

**Texte :**

```
[Accroche — 1 phrase]

[Pourquoi ça compte — 1–2 phrases]

La question que pose Le Phare : [Question du Phare]

→ [URL article]

#EspritCritique #[tag-sujet]
```

**Image :** oui / non — fichier : `visuel.png`

**Date publication prévue :**

---

## Bluesky / Mastodon — l’article

**Texte (≤ 500 car.) :**

```
[Question ou fait saillant] — notre lecture sur le-phare.info : [URL article]
```

---

## Prolongement (optionnel, J+3 à J+7)

Un seul des deux, selon ce qui existe :

- **La question suivante** — si une Question ou une Application l’a traitée : « Hier, un fait. Aujourd’hui, la question qu’il pose. » → [URL article suivant]
- **Sur le Sentier du Savoir** — l’outil pour lire ce type de sujet :

```
[Une compétence concrète que le lecteur emporte]

Sur le Sentier du Savoir : [titre du fondamental]
→ [URL Sentier]
```

---

## Notes internes

- Angle à ne pas déformer :
- Commentaire à surveiller :
- Publié le : ___ par ___
