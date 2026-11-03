import type { Format } from './types';

export function minutesDeLecture(texte: string): number {
  const mots = texte.replace(/<[^>]+>/g, ' ').split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(mots / 230));
}

export const LIBELLE_FORMAT: Record<Format, string> = {
  actualite: 'Actualité décryptée',
  question: 'Question du Phare',
  application: 'Application',
  fil: 'Fil du Phare',
  'texte-fondateur': 'Texte fondateur',
  dossier: 'Dossier',
  atelier: 'Atelier du Sentier',
  fondamental: 'Fondamental',
  // Hypothèse POC : la « Découverte du Phare » des maquettes n'existe pas dans les données ; la catégorie WP « experimental » en tient lieu.
  experimental: 'Découverte du Phare',
  livre: 'Savoir du livre',
};

/** Ordre d'affichage des formats dans les filtres. */
export const ORDRE_FORMATS: Format[] = ['actualite', 'question', 'application', 'experimental', 'dossier', 'texte-fondateur', 'atelier', 'fondamental', 'livre', 'fil'];

/** Les deux portes de l'accueil : ce qui part du présent / ce qui dure. */
export const FORMATS_ACTUALITE: Format[] = ['actualite', 'question', 'application', 'fil'];
export const FORMATS_CONNAISSANCE: Format[] = ['texte-fondateur', 'dossier', 'atelier', 'fondamental', 'experimental', 'livre'];

export const LIBELLE_THEME: Record<string, string> = {
  MONDE: 'Monde',
  POL: 'Politique et société',
  ECON: 'Économie',
  TECH: 'Technologie et IA',
  CLIMAT: 'Climat et transition',
  SCIENCE: 'Science et santé',
  CULTURE: 'Culture et philosophie',
};

export function dateFr(iso: string): string {
  const d = new Date(`${iso.slice(0, 10)}T12:00:00Z`);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' });
}

const BASE_LIVE = 'https://le-phare.info/';

/** Réécrit en liens relatifs les liens du corps qui pointent vers un article rendu par le POC. */
export function relocaliser(html: string, slugsLocaux: Set<string>): string {
  return html.replace(/href="https:\/\/le-phare\.info\/([a-z0-9-]+)\/?"/g, (m, slug: string) =>
    slugsLocaux.has(slug) ? `href="/${slug}/"` : m,
  );
}

/** Lien interne si l'article est rendu par le POC, sinon lien vers le site en ligne. */
export function hrefDeUrl(url: string, slugsLocaux: Set<string>): { href: string; externe: boolean } {
  if (!url.startsWith(BASE_LIVE)) return { href: url, externe: true };
  const slug = url.slice(BASE_LIVE.length).replace(/\/$/, '').split(/[?#]/)[0];
  return slugsLocaux.has(slug) ? { href: `/${slug}/`, externe: false } : { href: url, externe: true };
}
