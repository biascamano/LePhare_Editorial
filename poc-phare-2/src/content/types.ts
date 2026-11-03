export type Format =
  | 'actualite'
  | 'question'
  | 'application'
  | 'fil'
  | 'texte-fondateur'
  | 'dossier'
  | 'atelier'
  | 'fondamental'
  | 'experimental'
  | 'livre';

export type Theme = 'MONDE' | 'POL' | 'ECON' | 'TECH' | 'CLIMAT' | 'SCIENCE' | 'CULTURE';

export interface Link {
  label: string;
  url: string;
}

export interface Section {
  title: string;
  /** HTML déjà rendu par le provider (depuis le Markdown local ou le content.rendered de WordPress). */
  html: string;
}

/** Entrée minimale : sert aux liens et aux cartes d'articles hors corpus détaillé. */
export interface ArticleRef {
  id: string;
  title: string;
  slug: string;
  url: string;
  format: Format;
  theme: Theme | string;
}

export interface Article extends ArticleRef {
  category: string;
  date: string;
  updated: string;
  summary: string;
  objective: string;
  question: string;
  posture: string;
  keywords: string[];
  tags: string[];
  relatedIds: string[];
  dossierId: string;
  previousId: string;
  sentierEtapes: number[];
  metaDescription: string;
  /** HTML ; vide si l'article n'a pas de chapeau (la page affiche alors le résumé). */
  chapeauHtml: string;
  sections: Section[];
  readingMinutes: number;
  sources: Link[];
  nextQuestion: string;
  furtherLinks: Link[];
  sentierLinks: Link[];
}

export interface Fondamental {
  num: number;
  id: string;
  titre: string;
  url: string;
}

export interface Etape {
  num: number;
  nom: string;
  hubId: string;
  hubTitre: string;
  hubUrl: string;
  fondamentaux: Fondamental[];
}

export interface Sentier {
  etapes: Etape[];
}

export interface ListOptions {
  formats?: Format[];
  theme?: string;
  limit?: number;
}

/**
 * Contrat indépendant de la source. Toute implémentation est en lecture seule.
 * Les pages Astro n'importent que ce contrat (via provider.ts), jamais une source précise.
 */
export interface ContentProvider {
  readonly name: 'mock' | 'wordpress';
  listArticles(options?: ListOptions): Promise<Article[]>;
  getArticle(slug: string): Promise<Article | undefined>;
  /** Résout un ID éditorial (YYYY-NNN) vers une référence, y compris hors corpus détaillé. */
  resolveRef(id: string): Promise<ArticleRef | undefined>;
  getSentier(): Promise<Sentier>;
}
