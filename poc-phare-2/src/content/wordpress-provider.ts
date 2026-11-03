// Provider WordPress : esquisse fonctionnelle, LECTURE SEULE (GET publics de l'API REST, aucune authentification).
// Non utilisé par défaut. Limites documentées dans ARCHITECTURE.md §4.
import corpus from '../data/mock/corpus.json';
import { minutesDeLecture } from './util';
import type { Article, ArticleRef, ContentProvider, Format, Link, ListOptions, Section, Sentier } from './types';

const BASE = (import.meta.env.PHARE_WP_URL ?? 'https://le-phare.info').replace(/\/$/, '');
const API = `${BASE}/wp-json/wp/v2`;
const PAR_PAGE = 100;

interface WpTerm { taxonomy: string; slug: string }
interface WpPost {
  id: number;
  date: string;
  modified: string;
  slug: string;
  link: string;
  title: { rendered: string };
  excerpt: { rendered: string };
  content: { rendered: string };
  _embedded?: { 'wp:term'?: WpTerm[][] };
}

const THEME_PAR_TAG: Record<string, string> = {
  monde: 'MONDE',
  'politique-societe': 'POL',
  'economie-finance': 'ECON',
  'technologie-ia': 'TECH',
  'environnement-climat': 'CLIMAT',
  'science-sante': 'SCIENCE',
  'culture-philosophie': 'CULTURE',
};

// Aucun tag de pilier pour l'étape 3 (argumentation) dans la taxonomie actuelle.
const ETAPE_PAR_TAG: Record<string, number> = {
  'sentier-culture': 1,
  'sentier-critique': 2,
  'sentier-approfondissement': 4,
  'sentier-langues': 5,
  'sentier-science': 6,
  'sentier-transmission': 7,
  'sentier-vision': 8,
  'sentier-equilibre': 9,
};

function formatDe(categories: string[], tags: string[]): Format {
  if (categories.includes('experimental')) return 'experimental';
  if (categories.includes('cycle')) return 'fil';
  if (categories.includes('textes-fondateurs')) return 'texte-fondateur';
  if (categories.includes('dossier-hebdomadaire')) return 'dossier';
  if (categories.includes('sentier-du-savoir')) return 'atelier';
  if (categories.includes('livres')) return 'livre';
  if (tags.includes('type-question')) return 'question';
  if (tags.includes('type-application')) return 'application';
  return 'actualite';
}

const texte = (html: string) =>
  html.replace(/<[^>]+>/g, '').replace(/&#8217;/g, '’').replace(/&#8211;/g, '–').replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').trim();

const liens = (html: string): Link[] =>
  [...html.matchAll(/<a[^>]+href="([^"]+)"[^>]*>(.*?)<\/a>/g)].map((m) => ({ url: m[1], label: texte(m[2]) }));

/** Découpe le content.rendered produit par wp_push_draft.py (h2 + paragraphes + blocs finaux en <strong>). */
function decouper(html: string) {
  const blocs = { sources: '', nextQuestion: '', furtherLinks: '', sentierLinks: '' };
  const CIBLES: Record<string, keyof typeof blocs> = {
    'Repères de sources': 'sources',
    'La question suivante': 'nextQuestion',
    'Pour aller plus loin': 'furtherLinks',
    'Sur le Sentier du Savoir': 'sentierLinks',
  };
  let principal = html;
  const re = /<p>\s*<strong>(Repères de sources|La question suivante|Pour aller plus loin|Sur le Sentier du Savoir)<\/strong>\s*<\/p>/g;
  const marques = [...html.matchAll(re)];
  if (marques.length) {
    principal = html.slice(0, marques[0].index);
    marques.forEach((m, i) => {
      const fin = i + 1 < marques.length ? marques[i + 1].index : html.length;
      blocs[CIBLES[m[1]]] = html.slice(m.index! + m[0].length, fin);
    });
  }
  const morceaux = principal.split(/<h2[^>]*>(.*?)<\/h2>/);
  const chapeauHtml = morceaux[0].trim();
  const sections: Section[] = [];
  for (let i = 1; i < morceaux.length; i += 2) sections.push({ title: texte(morceaux[i]), html: morceaux[i + 1].trim() });
  return { chapeauHtml, sections, ...blocs };
}

function versArticle(p: WpPost): Article {
  const termes = (p._embedded?.['wp:term'] ?? []).flat();
  const categories = termes.filter((t) => t.taxonomy === 'category').map((t) => t.slug);
  const tags = termes.filter((t) => t.taxonomy === 'post_tag').map((t) => t.slug);
  const d = decouper(p.content.rendered);
  const resume = texte(p.excerpt.rendered);
  return {
    id: `wp-${p.id}`,
    title: texte(p.title.rendered),
    slug: decodeURIComponent(p.slug),
    url: p.link,
    format: formatDe(categories, tags),
    theme: tags.map((t) => THEME_PAR_TAG[t]).find(Boolean) ?? '',
    category: categories[0] ?? '',
    date: p.date.slice(0, 10),
    updated: p.modified.slice(0, 10),
    summary: resume,
    objective: '',
    question: '',
    posture: tags.find((t) => t.startsWith('posture-'))?.slice(8) ?? '',
    keywords: [],
    tags,
    relatedIds: [],
    dossierId: '',
    previousId: '',
    sentierEtapes: [...new Set(tags.map((t) => ETAPE_PAR_TAG[t]).filter((n): n is number => !!n))],
    metaDescription: resume,
    chapeauHtml: d.chapeauHtml,
    sections: d.sections,
    readingMinutes: minutesDeLecture(p.content.rendered),
    sources: liens(d.sources),
    nextQuestion: texte(d.nextQuestion),
    furtherLinks: liens(d.furtherLinks),
    sentierLinks: liens(d.sentierLinks),
  };
}

let cache: Promise<Article[]> | undefined;

async function tout(): Promise<Article[]> {
  cache ??= (async () => {
    const out: Article[] = [];
    for (let page = 1; ; page++) {
      const r = await fetch(`${API}/posts?per_page=${PAR_PAGE}&page=${page}&_embed=wp:term`, {
        headers: { Accept: 'application/json' },
      });
      if (!r.ok) throw new Error(`WordPress ${r.status} sur ${r.url}`);
      // Règle D15 : un article sans a-la-une est invisible sur le site actuel ; même règle ici.
      out.push(...((await r.json()) as WpPost[]).map(versArticle).filter((a) => a.tags.includes('a-la-une')));
      if (page >= Number(r.headers.get('X-WP-TotalPages') ?? '1')) break;
    }
    return out;
  })();
  return cache;
}

export const wordpressProvider: ContentProvider = {
  name: 'wordpress',
  async listArticles(options: ListOptions = {}) {
    let out = await tout();
    if (options.formats) out = out.filter((a) => options.formats!.includes(a.format));
    if (options.theme) out = out.filter((a) => a.theme === options.theme);
    return options.limit ? out.slice(0, options.limit) : out;
  },
  async getArticle(slug) {
    return (await tout()).find((a) => a.slug === slug);
  },
  async resolveRef(id): Promise<ArticleRef | undefined> {
    // WordPress ne connaît pas les IDs éditoriaux : on passe par le registre (index_editorial.csv, figé dans le snapshot).
    return (corpus.catalogue as ArticleRef[]).find((r) => r.id === id);
  },
  async getSentier() {
    // Le Sentier n'a pas de modèle structuré côté WordPress : la source reste le manifest du dépôt.
    return corpus.sentier as Sentier;
  },
};
