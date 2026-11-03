// Lecture seule : lit index_editorial.csv, le manifest du Sentier et les fichiers .md du dépôt,
// écrit uniquement src/data/mock/corpus.json dans le POC.
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const POC = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const REPO = resolve(POC, '..');
const OUT = join(POC, 'src', 'data', 'mock', 'corpus.json');
const PREMIER_ID = process.argv[2] ?? '2026-530';

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = '';
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (c === '"') quoted = false;
      else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(field); field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else field += c;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows;
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h.replace(/^﻿/, ''), r[i] ?? ''])));
}

const liste = (v) => (v ?? '').split(';').map((s) => s.trim()).filter(Boolean);
const lireCsv = (rel) => parseCsv(readFileSync(join(REPO, rel), 'utf-8'));

function parseLiens(bloc) {
  const liens = [];
  for (const m of bloc.matchAll(/\[([^\]]+)\]\(([^)\s]+)\)/g)) liens.push({ label: m[1].trim(), url: m[2].trim() });
  return liens;
}

const BLOCS_FINAUX = {
  'Repères de sources': 'sources',
  'Reperes de sources': 'sources',
  'La question suivante': 'nextQuestion',
  'Pour aller plus loin': 'furtherLinks',
  'Sur le Sentier du Savoir': 'sentierLinks',
};

function parseArticle(texte) {
  const lignes = texte.replace(/\r\n/g, '\n').split('\n');
  const meta = {};
  let i = 0;
  for (; i < lignes.length; i++) {
    const l = lignes[i].replace(/^﻿/, '');
    if (l.trim() === '---') { i++; break; }
    const m = l.match(/^([^:]{2,80}?)\s*:\s?(.*)$/);
    if (m) meta[m[1].trim()] = m[2].trim();
  }
  let corps = lignes.slice(i);
  const seoIdx = corps.findIndex((l) => /^#\s*SEO\s*$/i.test(l.trim()));
  const seo = {};
  if (seoIdx >= 0) {
    for (const l of corps.slice(seoIdx + 1)) {
      const m = l.match(/^([^:]+?)\s*:\s*(.*)$/);
      if (m) seo[m[1].trim().toLowerCase()] = m[2].trim();
    }
    corps = corps.slice(0, seoIdx);
  }
  while (corps.length && ['', '---'].includes(corps[corps.length - 1].trim())) corps.pop();

  const h1 = corps.findIndex((l) => l.startsWith('# '));
  const titreCorps = h1 >= 0 ? corps[h1].slice(2).trim() : '';
  corps = corps.slice(h1 + 1);

  const finaux = { sources: '', nextQuestion: '', furtherLinks: '', sentierLinks: '' };
  const principal = [];
  let cible = null;
  for (const l of corps) {
    const bloc = l.trim().match(/^\*\*(.+?)\*\*\s*$/);
    if (bloc && BLOCS_FINAUX[bloc[1].trim()]) { cible = BLOCS_FINAUX[bloc[1].trim()]; continue; }
    if (cible && l.startsWith('## ')) cible = null;
    if (cible) finaux[cible] += l + '\n';
    else principal.push(l);
  }

  let chapeau = '';
  const sections = [];
  let courante = null;
  for (const l of principal) {
    if (l.startsWith('## ')) {
      courante = { title: l.slice(3).trim(), md: '' };
      sections.push(courante);
    } else if (courante) courante.md += l + '\n';
    else chapeau += l + '\n';
  }
  for (const s of sections) s.md = s.md.replace(/\n*---\s*$/, '').trim();
  return {
    meta,
    seo,
    titreCorps,
    chapeau: chapeau.trim().replace(/^---\s*$/m, '').trim(),
    sections: sections.filter((s) => s.md || s.title),
    sources: parseLiens(finaux.sources),
    nextQuestion: finaux.nextQuestion.trim().replace(/^\*\*|\*\*$/g, ''),
    furtherLinks: parseLiens(finaux.furtherLinks),
    sentierLinks: parseLiens(finaux.sentierLinks),
  };
}

const FORMAT_PAR_TYPE_ARTICLE = {
  actualite: 'actualite',
  question: 'question',
  application: 'application',
  'texte fondateur': 'texte-fondateur',
  dossier: 'dossier',
};
const FORMAT_PAR_TYPE_INDEX = {
  ACTU: 'actualite',
  TF: 'texte-fondateur',
  DOSSIER: 'dossier',
  SYNTHESE: 'fil',
  SENTIER: 'atelier',
  FOND: 'fondamental',
  BRIEFING: 'actualite',
  LIVRE: 'livre',
};

function format(row, meta) {
  if (row.Categorie_WP === 'experimental') return 'experimental';
  const ta = (meta['Type article'] ?? '').toLowerCase().normalize('NFD').replace(/\p{M}/gu, '');
  return FORMAT_PAR_TYPE_ARTICLE[ta] ?? FORMAT_PAR_TYPE_INDEX[row.Type] ?? 'actualite';
}

const slugDeUrl = (url) => {
  try { return new URL(url).pathname.replace(/^\/|\/$/g, ''); } catch { return ''; }
};

const index = lireCsv('index_editorial.csv');
const publies = index.filter((r) => r.Statut === 'publie' && r.URL_WordPress && !r.URL_WordPress.includes('?p='));
const manifest = lireCsv('00_Systeme/Manifests/sentier_fondamentaux.csv');
const titreParId = Object.fromEntries(index.map((r) => [r.ID, r.Titre]));

// Le manifest stocke les noms sans accents : rétablissement orthographique, sans changement de sens.
const NOMS_ETAPES = {
  1: 'Construire une culture générale solide',
  2: "Maîtriser la pensée critique et l'analyse",
  3: 'Apprendre à argumenter et à convaincre',
  4: "Approfondir un ou plusieurs domaines d'expertise",
  5: 'Devenir polyglotte et cosmopolite',
  6: 'Comprendre la méthode scientifique et expérimenter',
  7: 'Écrire, transmettre, enseigner',
  8: 'Relier les savoirs et vision du monde',
  9: "Cultiver l'équilibre corps-esprit",
};

const etapes = [];
for (const r of manifest) {
  const num = Number(r.etape_num);
  let e = etapes.find((x) => x.num === num);
  if (!e) {
    e = { num, nom: NOMS_ETAPES[num] ?? r.etape_nom, nomManifest: r.etape_nom, hubId: r.hub_id, hubTitre: titreParId[r.hub_id] ?? '', hubUrl: '', fondamentaux: [] };
    etapes.push(e);
  }
  if (r.fondamental_num === '0') e.hubUrl = r.url_canonique;
  else e.fondamentaux.push({ num: Number(r.fondamental_num), id: r.fondamental_id, titre: titreParId[r.fondamental_id] || r.titre, url: r.url_canonique });
}
const etapeParUrl = new Map();
for (const e of etapes) {
  if (e.hubUrl) etapeParUrl.set(slugDeUrl(e.hubUrl), e.num);
  for (const f of e.fondamentaux) if (f.url) etapeParUrl.set(slugDeUrl(f.url), e.num);
}

const articles = [];
const absents = [];
for (const row of publies.filter((r) => r.ID >= PREMIER_ID)) {
  const chemin = join(REPO, row.Chemin_dossier, row.Nom_fichier);
  if (!existsSync(chemin)) { absents.push(`${row.ID} ${row.Chemin_dossier}/${row.Nom_fichier}`); continue; }
  const a = parseArticle(readFileSync(chemin, 'utf-8'));
  const etapesLiees = new Set();
  const etapeMeta = (a.meta['Etape du Sentier liee'] || row.Etape_sentier).match(/(\d{1,2})/);
  if (etapeMeta) etapesLiees.add(Number(etapeMeta[1]));
  for (const l of a.sentierLinks) {
    const n = etapeParUrl.get(slugDeUrl(l.url));
    if (n) etapesLiees.add(n);
  }
  articles.push({
    id: row.ID,
    slug: slugDeUrl(row.URL_WordPress) || row.Slug_WordPress,
    url: row.URL_WordPress,
    title: row.Titre || a.titreCorps,
    format: format(row, a.meta),
    theme: row.Theme,
    category: row.Categorie_WP,
    date: row.Date_publication_WP || row.Date_creation,
    updated: row.Date_derniere_maj,
    summary: a.meta['Resume court (500 caracteres max)'] || row.Resume_court,
    objective: a.meta["Objectif de l'article"] || row.Objectif,
    question: a.meta['Question du Phare'] || '',
    posture: a.meta['Posture Sentier'] || '',
    keywords: liste(row.Mots_cles),
    tags: liste(row.Tags_WP),
    relatedIds: liste(a.meta['Articles lies (IDs)'] || row.Articles_lies),
    dossierId: a.meta.Dossier || '',
    previousId: a.meta['Article precedent (ID)'] || '',
    sentierEtapes: [...etapesLiees].sort((x, y) => x - y),
    metaDescription: a.seo['meta description'] || '',
    chapeau: a.chapeau,
    sections: a.sections,
    sources: a.sources,
    nextQuestion: a.nextQuestion,
    furtherLinks: a.furtherLinks,
    sentierLinks: a.sentierLinks,
  });
}

const catalogue = publies.map((r) => ({
  id: r.ID,
  title: r.Titre,
  slug: slugDeUrl(r.URL_WordPress) || r.Slug_WordPress,
  url: r.URL_WordPress,
  format: FORMAT_PAR_TYPE_INDEX[r.Type] ?? 'actualite',
  theme: r.Theme,
}));

mkdirSync(dirname(OUT), { recursive: true });
writeFileSync(
  OUT,
  JSON.stringify({ generatedAt: new Date().toISOString(), premierId: PREMIER_ID, articles, catalogue, sentier: { etapes } }, null, 1),
  'utf-8',
);
console.log(`${articles.length} articles, ${catalogue.length} entrées de catalogue, ${etapes.length} étapes → ${OUT}`);
if (absents.length) console.log('Fichiers absents :', absents);
