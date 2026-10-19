// Build-time Open Graph card for each Thoughts post: /og/thoughts/<slug>.png
//
// Companion to the site card in scripts/generate-og.mjs: the same paper and the
// nav's hairline across the top, then the post as its page sets it (board
// SkPost) — the headline in Writer at the statement tracking, a hairline, and
// the date in Neue York capitals under it.
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
const SERIF_OTF = fontPath('PPWriter-RegularText.otf');
const SANS_OTF = fontPath('PPNeueYork-NormalMedium.otf');
const fontFiles = [SERIF_OTF, SANS_OTF];
const font = openSync(SERIF_OTF) as any;
const SERIF = font.familyName as string;
const SANS = (openSync(SANS_OTF) as any).familyName as string;

const PAPER = '#F8F5D7';
const INK = '#000000';

const W = 1200;
const H = 630;
const PAD = 56;
const INNER = W - PAD * 2;
const CAP = 0.71; // Writer's and Neue York's cap height, in em
const LABEL = 17; // the site's 10px labels, scaled for a card

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
    .toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'UTC' })
    .toUpperCase();

  // The card is a static image, so it always uses the plain title.
  const titleText = plainTitle(post.data.title);

  // Step the headline down until it fits a tidy number of lines.
  const TITLE_LS = -0.05;
  let titleSize = 76;
  let lines = wrapBalanced(titleText, titleSize, INNER, TITLE_LS);
  if (lines.length > 3) {
    titleSize = 60;
    lines = wrapBalanced(titleText, titleSize, INNER, TITLE_LS);
  }
  if (lines.length > 4) {
    titleSize = 48;
    lines = wrapBalanced(titleText, titleSize, INNER, TITLE_LS);
  }
  const titleLH = titleSize * 1.167;
  // A headline that opens on a quote mark hangs it in the margin, as on the page.
  const hang = /^[“‘"']/.test(titleText) ? emWidth(titleText[0], TITLE_LS) * titleSize : 0;

  const labelTop = PAD + 26 + LABEL * CAP;
  const dateBaseline = H - PAD;
  const ruleY = dateBaseline - LABEL * CAP - 22;
  // The headline hangs off the rule, so cards of different lengths stay anchored.
  const titleLastBaseline = ruleY - 44;
  const titleTop = titleLastBaseline - (lines.length - 1) * titleLH;

  const titleSvg = lines
    .map(
      (l, i) =>
        `<text x="${(PAD - (i === 0 ? hang : 0)).toFixed(1)}" y="${(titleTop + i * titleLH).toFixed(1)}" font-family="${SERIF}" font-size="${titleSize}" letter-spacing="${(TITLE_LS * titleSize).toFixed(2)}" fill="${INK}">${esc(l)}</text>`
    )
    .join('\n  ');

  const svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${W}" height="${H}" fill="${PAPER}"/>
    <rect x="${PAD}" y="${PAD}" width="${INNER}" height="1" fill="${INK}"/>
    <text x="${PAD}" y="${labelTop}" font-family="${SANS}" font-size="${LABEL}" fill="${INK}">MIGUEL ESCOBAR</text>
    <text x="${W - PAD}" y="${labelTop}" text-anchor="end" font-family="${SANS}" font-size="${LABEL}" fill="${INK}">THOUGHTS</text>

    ${titleSvg}

    <rect x="${PAD}" y="${ruleY}" width="${INNER}" height="1" fill="${INK}"/>
    <text x="${PAD}" y="${dateBaseline}" font-family="${SANS}" font-size="${LABEL}" fill="${INK}">${esc(date)}</text>
  </svg>`;

  const png = new Resvg(svg, {
    fitTo: { mode: 'width', value: W },
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: SERIF },
  })
    .render()
    .asPng();

  return new Response(png, {
    headers: { 'Content-Type': 'image/png', 'Cache-Control': 'public, max-age=31536000, immutable' },
  });
};
