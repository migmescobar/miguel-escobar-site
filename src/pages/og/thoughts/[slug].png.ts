// Build-time Open Graph image for each Thoughts post: /og/thoughts/<slug>.png
// (1200x630, on-brand — PP Editorial Old title + date, matching the site OG card).
// Generated with resvg; fontkit reads the font's family name and measures the
// title so it wraps to fit.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { Resvg } from '@resvg/resvg-js';
import { openSync } from 'fontkit';
import { fileURLToPath } from 'node:url';
import { plainTitle } from '../../../utils/postTitle';

const fontPath = (name: string) =>
  fileURLToPath(new URL(`../../../../scripts/fonts/${name}`, import.meta.url));
// resvg's font loader only reads OTF/TTF — a woff2 silently renders blank, so
// these point at the OTFs in scripts/fonts/ rather than the site's woff2.
const DISPLAY_OTF = fontPath('PPEditorialOld-Regular.otf');
const TEXT_OTF = fontPath('PPNeueMontreal-Regular.otf');
const fontFiles = [DISPLAY_OTF, TEXT_OTF];

// resvg matches fonts by their internal family name; read them once.
const serif = openSync(DISPLAY_OTF) as any;
const DISPLAY = serif.familyName as string;
const TEXT = (openSync(TEXT_OTF) as any).familyName as string;

const PAPER = '#EAE7E1';
const INK = '#141414';
const BRAND = '#0047bb';

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Greedy word-wrap using the actual display-serif metrics. */
function wrapTitle(text: string, fontSize: number, maxWidth: number): string[] {
  const measure = (s: string) => (serif.layout(s).advanceWidth * fontSize) / serif.unitsPerEm;
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

  // Pick a size that keeps the title to a tidy number of lines. The OG card is a
  // static image, not HTML, so it always uses the plain title (no *italic* markers).
  const titleText = plainTitle(post.data.title);
  let fontSize = 64;
  let lines = wrapTitle(titleText, fontSize, 1040);
  if (lines.length > 3) {
    fontSize = 50;
    lines = wrapTitle(titleText, fontSize, 1040);
  }
  if (lines.length > 4) {
    fontSize = 42;
    lines = wrapTitle(titleText, fontSize, 1040);
  }
  const lineHeight = Math.round(fontSize * 1.12);
  const startY = 250;
  const titleSvg = lines
    .map(
      (l, i) =>
        `<text x="80" y="${startY + i * lineHeight}" font-family="${DISPLAY}" font-size="${fontSize}" letter-spacing="-1" fill="${INK}">${esc(l)}</text>`
    )
    .join('');
  const dateY = startY + (lines.length - 1) * lineHeight + 56;

  const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
    <rect width="1200" height="630" fill="${PAPER}"/>
    <circle cx="102" cy="94" r="22" fill="${BRAND}"/>
    <text x="146" y="103" font-family="${TEXT}" font-size="22" letter-spacing="3" fill="${INK}" fill-opacity="0.55">THOUGHTS</text>
    <line x1="80" y1="150" x2="1120" y2="150" stroke="${INK}" stroke-opacity="0.3" stroke-width="1"/>
    ${titleSvg}
    <text x="80" y="${dateY}" font-family="${TEXT}" font-size="24" letter-spacing="2" fill="${INK}" fill-opacity="0.6">${esc(date)}</text>
    <line x1="80" y1="544" x2="1120" y2="544" stroke="${INK}" stroke-opacity="0.2" stroke-width="1"/>
    <text x="80" y="586" font-family="${TEXT}" font-size="20" letter-spacing="2" fill="${INK}" fill-opacity="0.55">MIGUEL-ESCOBAR.COM</text>
  </svg>`;

  const png = new Resvg(svg, {
    fitTo: { mode: 'width', value: 1200 },
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: TEXT },
  })
    .render()
    .asPng();

  return new Response(png, {
    headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=31536000, immutable' },
  });
};
