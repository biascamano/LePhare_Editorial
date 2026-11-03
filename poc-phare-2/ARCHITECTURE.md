# Architecture du POC

## 1. Principe

```
Sources (lecture seule)                 Contrat                  Pages statiques (Astro)
──────────────────────                  ───────                  ───────────────────────
mock : corpus.json  ◄─ extract-mock.mjs ◄─ index_editorial.csv, .md, manifest Sentier
                       │                                         /            accueil (2 portes)
                       ├─► ContentProvider ──────────────────►   /explorer/   filtres
wordpress : GET /wp-json/wp/v2/posts                             /<slug>/     article progressif
                                                                 /sentier/    parcours libre
```

- Le site est 100 % statique (SSG) : un CDN ou un hébergement de fichiers suffit, sans Node en production.
- Le JavaScript se limite au filtre d'Explorer, environ 1 Ko en ligne. Les autres pages n'exécutent aucun script : seul le JSON-LD est présent.
- Les URLs sont celles de WordPress, `/<slug>/` avec un slash final (`trailingSlash: 'always'`). Une bascule future ne casserait donc aucun lien entrant.
- Toutes les pages portent `noindex, nofollow, noarchive` pendant le POC. Leur canonical est auto-référent sur `PHARE_SITE` (défaut `https://test.le-phare.info/<slug>/`). À la bascule, `PHARE_SITE=https://le-phare.info` suffira : les slugs sont identiques.

## 2. Contrat de contenu (`src/content/types.ts`)

```ts
interface ContentProvider {
  readonly name: 'mock' | 'wordpress';
  listArticles(options?: { formats?; theme?; limit? }): Promise<Article[]>;
  getArticle(slug: string): Promise<Article | undefined>;
  resolveRef(id: string): Promise<ArticleRef | undefined>;   // ID éditorial YYYY-NNN → lien
  getSentier(): Promise<Sentier>;
}
```

Les pages n'importent que `content` (`provider.ts`), qui est choisi par `PHARE_SOURCE`. Une valeur inconnue fait échouer le build : il n'y a pas de repli silencieux.

### Mode `mock` (par défaut)

- `scripts/extract-mock.mjs` lit le registre, les .md et le manifest Sentier, et écrit `src/data/mock/corpus.json`. C'est la seule écriture, et elle reste dans le POC.
- Le contenu de l'instantané :
  - 48 articles détaillés, d'ID ≥ 2026-530 ;
  - un catalogue de 513 références, qui sert à résoudre les `Articles_lies` hors instantané ;
  - les 9 étapes du Sentier.
- Les blocs nommés (« Repères de sources », « Pour aller plus loin »…) sont découpés depuis le Markdown, puis rendus par `marked`.

### Mode `wordpress` (esquisse, lecture seule)

- Il fait des GET publics sur `/wp/v2/posts?_embed=wp:term`, page par page (100 articles par page), sans authentification, et ne garde que les articles `a-la-une` (règle D15).
- Le format vient des catégories et des tags. Les sections et les blocs finaux sont découpés dans `content.rendered`, sur la forme produite par `wp_push_draft.py`.
- Les slugs sont décodés (`decodeURIComponent`), car WordPress renvoie les caractères non ASCII encodés en pourcents.

Ses limites, connues :

| Limite | Effet |
|---|---|
| WordPress ne connaît pas les IDs éditoriaux | `resolveRef` et `getSentier` restent servis par l'instantané du dépôt |
| Pas de champs `objective`, `question` ni `keywords` | Le bloc « L'essentiel » et la question du Phare disparaissent en mode wordpress |
| Rank Math non exposé | La méta description reprend l'extrait |
| Pas de cache ni d'incrémental | Le build refetche tout : 290 pages en ~10,6 s |
| Contenus anciens hétérogènes | Pas de chapeau ni de sections, des h1 et des astérisques visibles (AUDIT §6) |

**Recommandation pour la suite** : construire depuis le registre et les .md du dépôt, c'est-à-dire le mode `mock` généralisé, plutôt que depuis l'API. Le dépôt est la source de vérité, il porte les métadonnées éditoriales et il évite d'hériter des défauts de conversion. WordPress resterait l'outil d'édition humaine et de diffusion. Ce choix est une décision ouverte (PLAN_INTEGRATION.md §4).

## 3. Design system (`src/styles/tokens.css`)

Les jetons sont des variables CSS. Chaque valeur a une provenance explicite :

| Jeton | Valeur | Provenance |
|---|---|---|
| `--c-teal` | `#008d7f` | **Relevé** : `--td_theme_color` du thème Newspaper sur le-phare.info |
| `--c-teal-ink` | `#006b61` | **Dérivé** du teal, assombri pour passer AA sur papier |
| `--c-mist` | `#e6f3f1` | **Dérivé** (teinte claire du teal) |
| `--c-teal-deep` | `#0b3d39` | **Provisoire** (bandeau, hero) |
| `--c-amber` | `#e8a33d` | **Provisoire** (lumière du phare, halo de focus) |
| `--c-ink` | `#1d1a17` | **Provisoire** |
| `--c-paper`, `--c-muted`, `--c-line` | `#fbfaf7`, `#5a5650`, `#dcd8d0` | **Provisoires** |
| Polices | piles système (serif pour les titres, sans pour l'interface) | **Provisoire** : aucun téléchargement de police |

- Il y a un mode sombre automatique (`prefers-color-scheme`), qui peut être forcé par `data-theme="dark"` ou `"light"`.
- L'échelle typographique et les espacements sont fluides (`clamp`).

### Contrastes WCAG (mesurés par script)

| Paire | Ratio | AA texte normal |
|---|---|---|
| texte / papier | 16,59 | ✓ |
| muted / papier | 6,98 | ✓ |
| teal-ink / papier | 6,14 | ✓ |
| teal-ink / mist | 5,63 | ✓ |
| blanc / teal-deep | 12,06 | ✓ |
| ambre / teal-deep | 5,59 | ✓ |
| encre / ambre | 8,03 | ✓ |
| blanc / teal-ink | 6,41 | ✓ |
| teal brut / blanc | 4,10 | ✗ : réservé aux bordures et filets, jamais au texte |
| sombre : texte, muted, teal-ink | 15,51 / 7,44 / 9,01 | ✓ |

Le premier anneau de focus était ambre seul, à 2,07:1 sur papier, donc non conforme. Il est remplacé par un contour encre de 2 px, doublé d'un halo ambre.

### Accessibilité

- Lien d'évitement vers `main#contenu`, et un seul h1 par page.
- Landmarks : header, nav, main, footer.
- Les cartes sont cliquables par leur titre, et le focus de la carte est visible (`:has`).
- Explorer : formulaire GET classique, `role="status"` et `aria-live` sur le compteur.
- Cibles tactiles d'au moins 44 px, et `prefers-reduced-motion` respecté.

## 4. Page article : lecture progressive

L'ordre de la page (nouvelle orientation, 2026-11-03) :
1. format et thème (liens vers Explorer filtré), titre, « La rédaction du Phare », date, temps de lecture, lien « Méthode » ;
2. chapeau (ou le résumé, s'il n'y a pas de chapeau) ;
3. **L'essentiel en deux minutes** : le résumé (s'il ne sert pas déjà de chapeau), l'objectif, la question du Phare ;
4. sommaire « Analyse complète · n parties », dans un `<details>` fermé (allège le mobile), à partir de 3 sections ;
5. corps, en sections ancrées ; les parties « ce que l'on sait », « ce qui résiste » ou « limites » sont mises en relief ;
6. **La question suivante**, si elle diffère ;
7. **Double circulation** : « Les connaissances qui l'éclairent » (article d'actualité) ou « L'actualité qu'elle éclaire » (article de connaissance), 3 liens au plus, pris dans les références **et** les rétroliens (articles qui citent celui-ci) de l'autre porte ;
8. **Transparence** : rédaction, nombre de sources, lien vers la partie limites, rôle de l'IA (texte à valider), corrections et « Signaler une erreur » ;
9. **Repères de sources** : un `<details>` replié, mais présent dans le HTML ;
10. **Poursuivre** : 3 propositions au plus, une découverte, le dossier (lié, sinon du même thème), une étape du Sentier ;
11. **Toutes les références** : le reste, dédoublonné, dans un `<details>` replié.

Limite : faute de champ auteur dans les données, l'auteur affiché est « La rédaction du Phare ». La mention sur l'IA n'existe pas dans le contenu : elle est marquée « à valider » (`.a-valider`).

Le HTML contient tout le contenu. Le repli repose sur `<details>`, natif, sans JS : les moteurs indexent les blocs repliés, et un lecteur sans JS les ouvre d'un clic. Les blocs vides ne s'affichent pas.

Un lien vers un article de l'instantané reste interne au POC. Les autres liens pointent vers le site actuel, avec la mention « (site actuel) ».

## 5. Sobriété

| Mesure (mode mock) | Valeur |
|---|---|
| CSS | 1 fichier de ~4,5 Ko (1,7 Ko gzip) |
| HTML médian | 20,7 Ko |
| Page la plus lourde | Explorer, 134,4 Ko (28,9 Ko gzip) |
| Build | 52 pages en ~0,5 s |
| Images, polices, analytics | Aucune |

**Limite** : Explorer embarque tous les articles. Sur 290 articles (mode wordpress), la page pèse 410 Ko (74 Ko gzip). Au-delà de quelques centaines d'articles, il faudra un index JSON séparé, chargé à la demande, ou une pagination par famille.

## 6. Dépendances et télémétrie

- Les dépendances sont locales et figées :
  - `astro` 7.3.8 (la 7.4.5 exige Node ≥ 22.23.4 ; la machine a 22.23.2) ;
  - `marked` 18.1.1 ;
  - en développement, `@astrojs/check` 0.9.10 et `typescript` 6.0.3.
- `npm audit` : 0 vulnérabilité. `@img/sharp-wasm32` est signalé « extraneous » : c'est une dépendance optionnelle d'Astro, sans usage ici.
- `node_modules` pèse 209 Mo et il est hors git.
- Astro envoie une télémétrie anonyme par défaut. Le POC la neutralise par `ASTRO_TELEMETRY_DISABLED=1` par commande, sans configuration globale. Une exécution initiale l'avait active (TESTS.md).
