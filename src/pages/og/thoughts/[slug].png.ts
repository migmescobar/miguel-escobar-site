// Build-time Open Graph image for each Thoughts post: /og/thoughts/<slug>.png
// (1200x630, on-brand — Gambarino title + date, matching the site OG card).
// Generated with resvg; fontkit reads the webfont's obfuscated family name and
// measures the title so it wraps to fit.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { Resvg } from '@resvg/resvg-js';
import { openSync } from 'fontkit';
import { fileURLToPath } from 'node:url';

const fontPath = (name: string) =>
  fileURLToPath(new URL(`../../../../scripts/fonts/${name}`, import.meta.url));
const GAMBARINO_TTF = fontPath('Gambarino-Regular.ttf');
const fontFiles = [GAMBARINO_TTF, fontPath('Geist-Medium.ttf'), fontPath('GeistMono-Regular.ttf')];

// resvg matches fonts by their internal (obfuscated) family name; read it once.
const gamb = openSync(GAMBARINO_TTF) as any;
const GAMBARINO = gamb.familyName as string;

const PAPER = '#EAE7E1';
const INK = '#141414';
const BRAND = '#0047bb';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Greedy word-wrap using the actual Gambarino metrics. */
function wrapTitle(text: string, fontSize: number, maxWidth: number): string[] {
  const measure = (s: string) => (gamb.layout(s).advanceWidth * fontSize) / gamb.unitsPerEm;
  const lines: string[] = [];
  let cur = '';
  for (const word of text.split(/\s+/)) {
    const test = cur ? `${cur} ${word}` : word;
    if (cur && measure(test) > maxWidth) {
      lines.push(cur);
      cur = word;
    } else {
      cur = test;
    }
  }
  if (cur) lines.push(cur);
  return lines;
}

export async function getStaticPaths() {
  const posts = await getCollection('thoughts', ({ data }) => !data.draft);
  return posts.map((post) => ({ params: { slug: post.id }, props: { post } }));
}

export const GET: APIRoute = ({ props }) => {
  const { post } = props as any;
  const date = new Date(post.data.pubDate)
    .toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })
    .toUpperCase();

  // Pick a size that keeps the title to a tidy number of lines.
  let fontSize = 64;
  let lines = wrapTitle(post.data.title, fontSize, 1040);
  if (lines.length > 3) {
    fontSize = 50;
    lines = wrapTitle(post.data.title, fontSize, 1040);
  }
  if (lines.length > 4) {
    fontSize = 42;
    lines = wrapTitle(post.data.title, fontSize, 1040);
  }
  const lineHeight = Math.round(fontSize * 1.12);
  const startY = 250;
  const titleSvg = lines
    .map(
      (l, i) =>
        `<text x="80" y="${startY + i * lineHeight}" font-family="${GAMBARINO}" font-size="${fontSize}" letter-spacing="-1" fill="${INK}">${esc(l)}</text>`
    )
    .join('');
  const dateY = startY + (lines.length - 1) * lineHeight + 56;

  const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
    <rect width="1200" height="630" fill="${PAPER}"/>
    <circle cx="102" cy="94" r="22" fill="${BRAND}"/>
    <text x="146" y="103" font-family="Geist Mono" font-size="22" letter-spacing="3" fill="${INK}" fill-opacity="0.55">THOUGHTS</text>
    <line x1="80" y1="150" x2="1120" y2="150" stroke="${INK}" stroke-opacity="0.3" stroke-width="1"/>
    ${titleSvg}
    <text x="80" y="${dateY}" font-family="Geist Mono" font-size="24" letter-spacing="2" fill="${INK}" fill-opacity="0.6">${esc(date)}</text>
    <line x1="80" y1="544" x2="1120" y2="544" stroke="${INK}" stroke-opacity="0.2" stroke-width="1"/>
    <text x="80" y="586" font-family="Geist Mono" font-size="20" letter-spacing="2" fill="${INK}" fill-opacity="0.55">MIGUEL-ESCOBAR.COM</text>
  </svg>`;

  const png = new Resvg(svg, {
    fitTo: { mode: 'width', value: 1200 },
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: 'Geist' },
  })
    .render()
    .asPng();

  return new Response(png, {
    headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=31536000, immutable' },
  });
};
