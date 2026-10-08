# Page d'accueil de le-phare.info — textes V5

*Rédigé le 2026-10-07 (`plan.md` B21). Page éditée **à la main** dans WordPress : aucune routine ne la pousse. Le seul bloc de flux repose sur le tag `a-la-une`, déjà posé sur tout article publié (D15) : il se met à jour seul.*

---

## 0. À retirer de l'accueil actuel

| Bloc | Raison |
|------|--------|
| « 📌 Contexte » (écoblanchiment) | Corps d'article affiché en tête d'accueil — vérifier s'il s'agit d'un article épinglé et le désépingler. |
| « 🧭 À venir dans Le Phare Hebdo » (accélération, abondance, pouvoir) | Programme fixe annoncé ; la V5 n'en a pas (le Radar propose des pistes, `plan.md` §6). |
| « Comment fonctionne le Phare Info ? » | Décrit le rythme triptyque (actualité + texte fondateur + atelier chaque jour). Remplacé par le §4 ci-dessous. |
| « Lire les faits du présent » | Doublon du flux. Fusionné dans le §2. |
| Emojis dans les intertitres | Alignement sur la rénovation (titres sans emoji, `plan.md` §19). |

---

## 1. En-tête

**Devise** (inchangée) :

> Le Phare éclaire l'actualité autrement.

**Phrase de mission** (sous la devise) :

> Chaque jour, un fait du présent. Derrière lui, une question qui dure. Le Phare prend le temps de passer de l'un à l'autre — pour comprendre plutôt que réagir, et penser par soi-même.

---

## 2. Derniers articles

Un seul flux, tous types confondus, dans l'ordre de publication.

**Requête** : 9 articles, tag `a-la-une`, toutes catégories, du plus récent au plus ancien. Afficher titre, extrait, date, et un badge :

| Critère | Badge |
|---------|-------|
| tag `type-actualite` | Actualité |
| tag `type-question` | Question du Phare |
| tag `type-application` | Application |
| catégorie `textes-fondateurs` | Texte fondateur |
| catégorie `cycle` | Le Fil du Phare |
| catégorie `dossier-hebdomadaire` | Dossier |
| catégorie `sentier-du-savoir` | Sentier du Savoir |

**Intertitre** : Derniers articles

**Bouton** : Tous les articles

---

## 3. Pour aller plus loin

Trois blocs côte à côte, sans flux d'articles : un titre, deux phrases, un lien vers la rubrique.

**Dossiers** → `/category/dossier-hebdomadaire/`

> Quand plusieurs articles tournent autour d'une même question, le dossier les rassemble et les met en ordre. C'est la carte d'un sujet, à lire dans l'ordre ou à picorer.

**Textes fondateurs** → `/category/textes-fondateurs/`

> Une pensée ancienne pour regarder un problème présent. Les auteurs ne sont pas là pour avoir raison à notre place, mais pour nous prêter une grille de lecture.

**Le Sentier du Savoir** → `/category/sentier-du-savoir/`

> Des ateliers pour s'exercer : lire un chiffre, peser une source, reconnaître un raisonnement. Le Sentier transforme ce que l'actualité nous apprend en outils qui restent.

---

## 4. Comment lire le Phare

Remplace « Comment fonctionne le Phare Info ? ».

**Intertitre** : Comment lire le Phare

> Le Phare avance à trois vitesses.
>
> **Chaque jour**, un article. Le sujet vient de l'actualité ; la forme vient du sujet : une actualité décryptée, une Question du Phare qui prend du recul, ou une application qui met un outil de pensée à l'épreuve d'un cas réel.
>
> **Chaque semaine**, Le Fil du Phare relie les articles parus et dégage la question qui les traverse.
>
> **Chaque mois**, ce qui s'est accumulé prend forme durable : un dossier quand un sujet le mérite, un texte fondateur quand une pensée éclaire ce que nous traversons, un atelier du Sentier quand une méthode s'impose.
>
> Rien n'est publié pour remplir une case. Un mois sans dossier est un mois où aucun sujet n'était mûr.

**Parcours en une ligne** (sous le texte, en petit) :

> Voir l'actualité → l'interroger → la regarder autrement → la relier → en garder les outils.

---

## 5. Les archives

Bloc conservé ; texte ajusté :

**Intertitre** : Les archives

> Toutes les questions déjà ouvertes par Le Phare, classées par thème. Beaucoup restent d'actualité : c'est un peu le principe.

---

## 6. Menu principal

| Ordre | Libellé | Cible |
|-------|---------|-------|
| 1 | Accueil | `/` |
| 2 | Actualités | `/category/actualites/` |
| 3 | Le Fil du Phare | `/category/cycle/` |
| 4 | Dossiers | `/category/dossier-hebdomadaire/` |
| 5 | Le Sentier du Savoir | (cible actuelle, inchangée) |
| 6 | Le Phare | (cible actuelle, inchangée) |

« Nous rejoindre » : déplacer en pied de page.

---

## 7. Libellés de catégories à renommer

**Libellé seulement** : ne toucher ni au slug, ni à l'ID (URLs et requêtes inchangées).

| Slug | Libellé actuel | Nouveau libellé |
|------|----------------|-----------------|
| `cycle` (id 97) | Dossier hebdomadaire - Notre fil rouge | Le Fil du Phare |
| `dossier-hebdomadaire` | (à relever) | Dossiers |

Après renommage : mettre à jour la colonne libellé de `00_Systeme/Taxonomie_WordPress_le-phare_info.md` §2.

---

## 8. Ordre de mise en place

1. Renommer les libellés (§7).
2. Désépingler / retirer les blocs du §0.
3. Poser les blocs 1 à 5 dans cet ordre.
4. Menu (§6).
