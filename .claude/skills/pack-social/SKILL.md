---
name: pack-social
description: Pack réseaux sociaux Le Phare — rédige le pack de posts (LinkedIn, Bluesky/Mastodon, prolongement) d'un article publié, dans 08_Social/02_Contenus/a-publier/. Sans ID, prend le dernier article publié qui n'a pas encore de pack. Ne poste rien. Déclenché par « pack social [<ID>] » ou /pack-social.
---

# Pack social — un article publié, un pack

Référence : `08_Social/03_Operation/workflow-apres-publication.md`, gabarit `08_Social/02_Contenus/gabarit-post-article.md`, ton et hashtags `08_Social/00_Strategie/ligne-editoriale-reseaux.md`, rythme `08_Social/00_Strategie/calendrier-type.md`. Exemple abouti : `08_Social/02_Contenus/a-publier/2026-10-13_question-du-phare-fusion-promesses-qui-verifie/pack.md`.

**Rien n'est posté** : le pack est un brouillon que le fondateur copie-colle. Hors routines, hors journal du phare, sans mémoire ni Radar.

## Variantes du prompt

- `pack social` : article choisi par la règle de l'étape 1.
- `pack social <ID>` : article imposé.
- `pack social <ID> <ID> …` : un pack par article, dans l'ordre donné.

## 1. Choisir l'article

**ID donné** : `python tools/index_lookup.py <ID>`. Statut autre que `publie` → s'arrêter : pas de post sur un brouillon (mode brouillons compris).

**Sans ID** :
```bash
python tools/index_lookup.py --statut publie --limit 10
```
Prendre le plus récent qui remplit les deux conditions :
- type ACTU, TF, DOSSIER ou SYNTHESE (pas SENTIER ni FOND : le Sentier sert de prolongement, pas de sujet) ;
- pas encore de pack : Grep de `` `<ID>` `` dans `08_Social/02_Contenus/` (dossiers `a-publier/` et `archives/`).

Aucun candidat dans les 10 → le dire et s'arrêter.

**Rythme** (signalé, non bloquant) : compter les packs `a-publier/` dont la date prévue tombe dans la semaine. À 4 ou plus, le signaler dans le rapport ; le calendrier vise 2 à 4 posts par semaine.

## 2. Lire

- L'article canonique (Glob `**/<ID>_*_V1.md` hors `07_A_Publier/`) : en-tête (Type article, Theme, Question du Phare, Article precedent), corps, navigation finale.
- **Article suivant** : Grep `Article precedent \(ID\) : <ID>` dans `01_Actualites/` et `04_Textes_fondateurs/` ; s'il existe et qu'il est `publie`, il devient le prolongement.
- **Sentier** : lien de « Sur le Sentier du Savoir » de l'article, vérifié dans `00_Systeme/Manifests/sentier_fondamentaux.csv` (jamais `wiki-du-phare`).
- URLs (article, origine, suivant) : `python tools/index_lookup.py <IDs>` uniquement, jamais de `?p=`.

## 3. Rédiger

Dossier : `08_Social/02_Contenus/a-publier/<Date_publication_WP>_<slug WP>/pack.md`, structure du gabarit.

- **Métadonnées** : toutes remplies ; `Statut pack` = `brouillon`.
- **LinkedIn (J+1)** : accroche factuelle, pourquoi ça compte, « La question que pose Le Phare : … », lien, 2 à 4 hashtags dont `#EspritCritique`. Date prévue = date de publication + 1 jour.
- **Bluesky / Mastodon** : ≤ 500 caractères, lien compris (compter).
- **Prolongement (J+3 à J+7)** : l'article suivant s'il existe, sinon le Sentier.
- Liens avec UTM : `?utm_source=<linkedin|bluesky>&utm_medium=social&utm_campaign=<ID>`.
- **Image** : idée et texte alternatif ; `visuel.png` reste « à préparer ».
- **Notes internes** : l'angle à ne pas déformer (ce que l'article ne dit pas), les faits datés à ne pas présenter comme actuels, les commentaires à surveiller.

Règles : pas un fait absent de l'article ; pas de clickbait ni de superlatif ; nuances et incertitudes de l'article conservées ; citations reprises telles quelles, avec l'auteur.

## 4. Relire (grille du workflow, §3)

- [ ] Le post ne contredit pas l'article
- [ ] Pas de clickbait
- [ ] Liens = URLs de l'index (+ UTM), aucun `?p=`
- [ ] Hashtags ≤ 4 ; Bluesky ≤ 500 caractères

## Rapport

```
Pack social — <ID> <titre court>
Choix : imposé / dernier publié sans pack (écartés : …)
Fichier : 08_Social/02_Contenus/a-publier/<dossier>/pack.md
LinkedIn prévu le <date> · prolongement : <suivant | Sentier>
Rythme : N packs prévus cette semaine
À faire (fondateur) : visuel, publication, puis statut « publié » et archivage
```

Pas de commit sans demande.

## Commandes sans demande de permission

Une commande Bash **simple** par appel : pas de `&&`, `;`, `|`, ni `python -c` multiligne. Read / Grep / Glob plutôt que `cat` / `grep` / `find`.

## Ne pas faire

- Poster, planifier ou appeler une API de réseau social.
- Faire un pack pour un article non publié dans l'index.
- Inventer une URL ou un fait, ou citer un chiffre absent de l'article.
- Modifier l'article, l'index, la mémoire ou le Radar.
