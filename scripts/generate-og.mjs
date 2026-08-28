// Generate the 1200x630 Open Graph card. Run: npm run assets:og
//
// The card echoes the home page's one big gesture: MIGUEL ESCOBAR set on a
// single line, fitted edge to edge, on a flood colour with light type. Social
// feeds are overwhelmingly white, so the saturated ground is what makes it
// carry at thumbnail size.
//
// Two elements only — the name and the positioning line. A URL and a location
// were tried along a bottom rule and cut: at the size a card actually gets
// looked at they were unreadable furniture, and the space buys the positioning
// line enough size to be read in the feed instead of after the click.
import { Resvg } from '@resvg/resvg-js';
import { openSync } from 'fontkit';
import { writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const fonts = path.join(root, 'scripts/fonts');
const outDir = path.join(root, 'public');
mkdirSync(outDir, { recursive: true });

// resvg's font loader only reads OTF/TTF — handing it a woff2 renders a
// silently blank image — and it matches fonts by internal family name.
const OTF = path.join(fonts, 'PPNeueMontreal-Regular.otf');
const font = openSync(OTF);
const TEXT = font.familyName;

const BLUE = '#0047BB'; // the About door's flood colour; the site's one accent
const PAPER = '#EAE7E1';

const W = 1200;
const H = 630;
const PAD = 80;
const INNER = W - PAD * 2;

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Width of a string in em, including SVG letter-spacing (applied per glyph). */
const emWidth = (s, lsEm) => font.layout(s).advanceWidth / font.unitsPerEm + lsEm * s.length;

/** Largest font-size that fits `s` into `maxPx` at the given tracking. */
const fitSize = (s, maxPx, lsEm) => (maxPx / emWidth(s, lsEm)) * 0.998;

/** Greedy wrap at a fixed size — the minimum number of lines that fits. */
function wrap(text, size, maxPx, lsEm) {
  const lines = [];
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
 * Same line count as a greedy wrap, but broken so the lines come out even —
 * greedy leaves a one-word orphan ("… and stakes of / tech"), which reads badly
 * at card size. Searches every split into N lines and keeps the one whose
 * longest line is shortest.
 */
function wrapBalanced(text, size, maxPx, lsEm) {
  const words = text.split(/\s+/);
  const target = wrap(text, size, maxPx, lsEm).length;
  if (target < 2) return words.length ? [text] : [];

  let best = null;
  const walk = (start, remaining, acc) => {
    if (remaining === 1) {
      const last = words.slice(start).join(' ');
      const lines = [...acc, last];
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
  return best ? best.lines : wrap(text, size, maxPx, lsEm);
}

// ── Name, fitted edge to edge like the home hero ───────────────────────────
const NAME = 'MIGUEL ESCOBAR';
const NAME_LS = -0.03;
const nameSize = fitSize(NAME, INNER, NAME_LS);

// ── Positioning line ───────────────────────────────────────────────────────
// Set as display type, not body copy: 60px is the largest size that still
// breaks on the comma into two even lines, and the tracking goes slightly
// negative the way the site's own large headings do.
const LEDE = 'Editorial instincts and creative acuity, rewired for the scale and stakes of tech';
const ledeSize = 60;
const ledeLS = -0.006;
const ledeLines = wrapBalanced(LEDE, ledeSize, INNER, ledeLS);
const ledeLH = Math.round(ledeSize * 1.22);

// Composition mirrors the home page: the name sits at the top, the positioning
// line is pinned to the bottom, and the space between them is deliberate rather
// than leftover. The name is cap-aligned to the top padding and the lede's last
// line is baseline-aligned to the bottom padding, so both optical margins match
// the 80px sides.
const CAP = 0.72; // Neue Montreal cap height, in em
const nameBaseline = PAD + nameSize * CAP;
const ledeLastBaseline = H - PAD;
const ledeTop = ledeLastBaseline - (ledeLines.length - 1) * ledeLH;

const svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="${W}" height="${H}" fill="${BLUE}"/>

  <text x="${PAD}" y="${nameBaseline}" font-family="${TEXT}" font-size="${nameSize.toFixed(2)}"
        letter-spacing="${(NAME_LS * nameSize).toFixed(2)}" fill="${PAPER}">${esc(NAME)}</text>

  ${ledeLines
    .map(
      (l, i) =>
        `<text x="${PAD}" y="${ledeTop + i * ledeLH}" font-family="${TEXT}" font-size="${ledeSize}" letter-spacing="${(ledeLS * ledeSize).toFixed(2)}" fill="${PAPER}" fill-opacity="0.85">${esc(l)}</text>`
    )
    .join('\n  ')}
</svg>`;

const png = new Resvg(svg, {
  fitTo: { mode: 'width', value: W },
  font: { fontFiles: [OTF], loadSystemFonts: false, defaultFontFamily: TEXT },
})
  .render()
  .asPng();

writeFileSync(path.join(outDir, 'og-image.png'), png);
console.log(
  `Wrote public/og-image.png (${W}x${H}) — name fitted at ${nameSize.toFixed(1)}px, lede ${ledeSize}px on ${ledeLines.length} line(s)`
);
