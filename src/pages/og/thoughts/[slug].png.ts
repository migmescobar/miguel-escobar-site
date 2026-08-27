// Build-time Open Graph card for each Thoughts post: /og/thoughts/<slug>.png
//
// Companion to the site card in scripts/generate-og.mjs. Same composition —
// eyebrow at the top, meta anchored to a rule at the bottom — but on paper
// rather than the blue flood: a shared article is a reading surface, and the
// tonal split makes a post distinguishable from the site card in a feed.
import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { Resvg } from '@resvg/resvg-js';
import { openSync } from 'fontkit';
import { fileURLToPath } from 'node:url';
import { plainTitle } from '../../../utils/postTitle';

const fontPath = (name: string) =>
  fileURLToPath(new URL(`../../../../scripts/fonts/${name}`, import.meta.url));
// resvg's font loader only reads OTF/TTF — a woff2 renders a silently blank
// image — and it matches fonts by internal family name.
const TEXT_OTF = fontPath('PPNeueMontreal-Regular.otf');
const fontFiles = [TEXT_OTF];
const font = openSync(TEXT_OTF) as any;
const TEXT = font.familyName as string;

const PAPER = '#EAE7E1';
const INK = '#141414';
const BLUE = '#0047BB';

const W = 1200;
const H = 630;
const PAD = 80;
const INNER = W - PAD * 2;
const CAP = 0.72; // Neue Montreal cap height, in em

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Width of a string in em, including SVG letter-spacing (applied per glyph). */
const emWidth = (s: string, lsEm: number) =>
  font.layout(s).advanceWidth / font.unitsPerEm + lsEm * s.length;

/** Greedy wrap — the minimum number of lines that fits. */
function wrap(text: string, size: number, maxPx: number, lsEm: number): string[] {
  const lines: string[] = [];
  let cur = '';
  for (const word of text.split(/\s+/)) {
    const test = cur ? `${cur} ${word}` : word;
    if (cur && emWidth(test, lsEm) * size > maxPx) {
      lines.push(cur);
      cur = word;
    } else cur = test;
  }
  if (cur) lines.push(cur);
  return lines;
}

/**
 * Same line count as greedy, but broken so the lines come out even — greedy
 * leaves one-word orphans, which read badly at card size. (Deliberately
 * duplicated from scripts/generate-og.mjs: that runs as a plain node script,
 * this runs through Astro's TS pipeline, so they can't share a module.)
 */
function wrapBalanced(text: string, size: number, maxPx: number, lsEm: number): string[] {
  const words = text.split(/\s+/);
  const target = wrap(text, size, maxPx, lsEm).length;
  if (target < 2) return [text];

  let best: { lines: string[]; widest: number } | null = null;
  const walk = (start: number, remaining: number, acc: string[]) => {
    if (remaining === 1) {
      const lines = [...acc, words.slice(start).join(' ')];
      const widest = Math.max(...lines.map((l) => emWidth(l, lsEm) * size));
      if (widest <= maxPx && (!best || widest < best.widest)) best = { lines, widest };
      return;
    }
    for (let end = start + 1; end <= words.length - (remaining - 1); end++) {
      const line = words.slice(start, end).join(' ');
      if (emWidth(line, lsEm) * size > maxPx) break;
      walk(end, remaining - 1, [...acc, line]);
    }
  };
  walk(0, target, []);
  return best ? best!.lines : wrap(text, size, maxPx, lsEm);
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

  // The card is a static image, so it always uses the plain title.
  const titleText = plainTitle(post.data.title);

  // Step the title down until it fits a tidy number of lines.
  const TITLE_LS = -0.014;
  let titleSize = 68;
  let lines = wrapBalanced(titleText, titleSize, INNER, TITLE_LS);
  if (lines.length > 3) {
    titleSize = 54;
    lines = wrapBalanced(titleText, titleSize, INNER, TITLE_LS);
  }
  if (lines.length > 4) {
    titleSize = 44;
    lines = wrapBalanced(titleText, titleSize, INNER, TITLE_LS);
  }
  const titleLH = Math.round(titleSize * 1.12);

  const eyebrowBaseline = PAD + 20 * CAP;
  const ruleY = H - 92;
  // Title hangs off the bottom rule so cards of different lengths stay anchored.
  const titleLastBaseline = ruleY - 96;
  const titleTop = titleLastBaseline - (lines.length - 1) * titleLH;

  const titleSvg = lines
    .map(
      (l, i) =>
        `<text x="${PAD}" y="${titleTop + i * titleLH}" font-family="${TEXT}" font-size="${titleSize}" letter-spacing="${(TITLE_LS * titleSize).toFixed(2)}" fill="${INK}">${esc(l)}</text>`
    )
    .join('\n  ');

  const svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${W}" height="${H}" fill="${PAPER}"/>

    <text x="${PAD}" y="${eyebrowBaseline}" font-family="${TEXT}" font-size="20" letter-spacing="2.6" fill="${BLUE}">THOUGHTS</text>

    ${titleSvg}

    <line x1="${PAD}" y1="${ruleY}" x2="${W - PAD}" y2="${ruleY}" stroke="${INK}" stroke-opacity="0.3" stroke-width="1"/>
    <text x="${PAD}" y="${ruleY + 40}" font-family="${TEXT}" font-size="20" letter-spacing="2.6" fill="${INK}" fill-opacity="0.7">MIGUEL-ESCOBAR.COM</text>
    <text x="${W - PAD}" y="${ruleY + 40}" text-anchor="end" font-family="${TEXT}" font-size="20" letter-spacing="2.6" fill="${INK}" fill-opacity="0.7">${esc(date)}</text>
  </svg>`;

  const png = new Resvg(svg, {
    fitTo: { mode: 'width', value: W },
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: TEXT },
  })
    .render()
    .asPng();

  return new Response(png, {
    headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=31536000, immutable' },
  });
};
