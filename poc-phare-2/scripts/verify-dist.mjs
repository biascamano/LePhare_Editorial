// Vérifie le site produit dans dist/ : liens internes, métadonnées, structure, poids. Aucun accès réseau.
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzipSync } from 'node:zlib';

const DIST = resolve(dirname(fileURLToPath(import.meta.url)), '..', process.argv[2] ?? 'dist');
const SITE = (process.env.PHARE_SITE ?? 'https://test.le-phare.info').replace(/\/$/, '');
const reCanonical = new RegExp(`<link rel="canonical" href="${SITE.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}/([^"]*/)?"`);
const fichiers = (d) => readdirSync(d).flatMap((f) => (statSync(join(d, f)).isDirectory() ? fichiers(join(d, f)) : [join(d, f)]));
const tous = fichiers(DIST);
const pages = tous.filter((f) => f.endsWith('.html'));
const erreurs = [];
const poids = [];
let liensInternes = 0;
let liensExternes = 0;
let assetsRefs = 0;

const existe = (href) => {
  const p = href.split(/[?#]/)[0];
  if (!p || p === '/') return existsSync(join(DIST, 'index.html'));
  const cible = join(DIST, decodeURI(p));
  return existsSync(cible) && statSync(cible).isFile() ? true : existsSync(join(cible, 'index.html'));
};

for (const f of pages) {
  const rel = '/' + relative(DIST, f).replace(/\\/g, '/');
  const html = readFileSync(f, 'utf-8');
  const un = (re) => html.match(re)?.[1];
  const verifier = (cond, msg) => { if (!cond) erreurs.push(`${rel} : ${msg}`); };

  verifier(/<html lang="fr"[\s>]/.test(html), 'lang="fr" absent');
  verifier(un(/<title>([^<]+)<\/title>/), 'title absent');
  verifier((un(/<meta name="description" content="([^"]*)"/) ?? '').length >= 50, 'description absente ou < 50 caractères');
  verifier(rel === '/404.html' || reCanonical.test(html), `canonical absente, hors ${SITE} ou sans slash final`);
  verifier(/<meta name="robots" content="noindex[^"]*"/.test(html), 'meta robots noindex absente');
  verifier((html.match(/<h1[\s>]/g) ?? []).length === 1, `${(html.match(/<h1[\s>]/g) ?? []).length} h1 (attendu : 1)`);
  verifier(/<main id="contenu"/.test(html), 'main#contenu absent');
  verifier(!/\*[^*\s][^*]{3,}\*/.test(html.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>/g, '')), 'astérisques Markdown visibles');
  verifier(!/<img(?![^>]*\balt=)/.test(html), 'img sans alt');

  const ids = [...html.matchAll(/\sid="([^"]+)"/g)].map((m) => m[1]);
  const doublons = ids.filter((x, i) => ids.indexOf(x) !== i);
  verifier(!doublons.length, `id dupliqués : ${[...new Set(doublons)].join(', ')}`);

  for (const m of html.matchAll(/<a\b[^>]*\bhref="([^"]+)"/g)) {
    const href = m[1];
    if (href.startsWith('#')) {
      verifier(ids.includes(href.slice(1)), `ancre cassée ${href}`);
    } else if (href.startsWith('/')) {
      liensInternes++;
      verifier(existe(href), `lien interne cassé ${href}`);
      const p = href.split(/[?#]/)[0];
      verifier(p.endsWith('/') || /\.\w+$/.test(p), `lien interne sans slash final ${href}`);
    } else liensExternes++;
  }
  for (const m of html.matchAll(/<(?:img|script|source)\b[^>]*\bsrc="([^"]+)"|<link\b[^>]*\bhref="([^"]+)"/g)) {
    const ref = m[1] ?? m[2];
    if (ref.startsWith('/') && !ref.startsWith('//')) {
      assetsRefs++;
      const cible = join(DIST, decodeURI(ref.split(/[?#]/)[0]));
      verifier(existsSync(cible) && statSync(cible).isFile(), `ressource absente ${ref}`);
    } else if (/^https?:/.test(ref) && /<(img|script|source)/.test(m[0])) {
      verifier(false, `ressource externe chargée ${ref}`);
    }
  }
  const brut = Buffer.byteLength(html);
  poids.push({ page: rel, ko: brut / 1024, gzKo: gzipSync(html).length / 1024 });
}

const assets = tous.filter((f) => /\.(js|css)$/.test(f)).map((f) => ({ f: relative(DIST, f), ko: statSync(f).size / 1024, gzKo: gzipSync(readFileSync(f)).length / 1024 }));
poids.sort((a, b) => b.ko - a.ko);
const fmt = (n) => n.toFixed(1);
console.log(`${pages.length} pages, ${liensInternes} liens internes, ${liensExternes} liens externes (non testés : hors ligne), ${assetsRefs} références de ressources locales`);
console.log(`Site attendu : ${SITE}`);
console.log('Pages les plus lourdes (HTML, Ko brut / gzip) :');
for (const p of poids.slice(0, 5)) console.log(`  ${fmt(p.ko)} / ${fmt(p.gzKo)}  ${p.page}`);
console.log(`Médiane HTML : ${fmt(poids[Math.floor(poids.length / 2)].ko)} Ko`);
console.log('Assets JS/CSS (Ko brut / gzip) :');
for (const a of assets) console.log(`  ${fmt(a.ko)} / ${fmt(a.gzKo)}  ${a.f}`);
const scriptsInline = pages.filter((f) => /<script type="module"/.test(readFileSync(f, 'utf-8'))).map((f) => '/' + relative(DIST, f).replace(/\\/g, '/'));
console.log(`Pages avec un script exécutable : ${scriptsInline.length ? scriptsInline.join(', ') : 'aucune'}`);
if (erreurs.length) {
  console.log(`\n${erreurs.length} erreur(s) :`);
  for (const e of erreurs) console.log('  - ' + e);
  process.exit(1);
}
console.log('\nOK : aucune erreur.');
