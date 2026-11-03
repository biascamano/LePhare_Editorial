import { marked } from 'marked';
import corpus from '../data/mock/corpus.json';
import { minutesDeLecture } from './util';
import type { Article, ArticleRef, ContentProvider, ListOptions, Sentier } from './types';

type Brut = Omit<Article, 'chapeauHtml' | 'sections' | 'readingMinutes' | 'format'> & {
  format: string;
  chapeau: string;
  sections: { title: string; md: string }[];
};

const md = (s: string) => marked.parse(s, { async: false, gfm: true });

function versArticle(b: Brut): Article {
  const { chapeau, sections, ...reste } = b;
  const texte = [chapeau, ...sections.map((s) => s.md)].join(' ');
  return {
    ...reste,
    format: b.format as Article['format'],
    chapeauHtml: chapeau ? md(chapeau) : '',
    sections: sections.map((s) => ({ title: s.title, html: md(s.md) })),
    readingMinutes: minutesDeLecture(texte),
  };
}

const articles = (corpus.articles as Brut[])
  .map(versArticle)
  .sort((a, b) => b.date.localeCompare(a.date) || b.id.localeCompare(a.id));
const refs = new Map<string, ArticleRef>((corpus.catalogue as ArticleRef[]).map((r) => [r.id, r]));
for (const a of articles) refs.set(a.id, a);

export const mockProvider: ContentProvider = {
  name: 'mock',
  async listArticles(options: ListOptions = {}) {
    let out = articles;
    if (options.formats) out = out.filter((a) => options.formats!.includes(a.format));
    if (options.theme) out = out.filter((a) => a.theme === options.theme);
    return options.limit ? out.slice(0, options.limit) : out;
  },
  async getArticle(slug) {
    return articles.find((a) => a.slug === slug);
  },
  async resolveRef(id) {
    return refs.get(id);
  },
  async getSentier() {
    return corpus.sentier as Sentier;
  },
};
