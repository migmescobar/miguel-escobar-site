// Generate the 1200x630 Open Graph card. Run: npm run assets:og
//
// The card is the Home hero in miniature (redesign-2026, NewHome): paper ground,
// the statement in ink at the top left, the name fitted edge to edge along the
// foot, and the soft cyan glow off to the right where the hero's arrow sits.
// The glow is the one colour in the identity, so it is what makes the card
// carry in a white feed; the name is what makes it legible as a thumbnail.
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

const PAPER = '#EAE7E1';
const INK = '#141414';

const W = 1200;
const H = 630;
const PAD = 56; // the hero's 64px side margin at 1440, scaled to the card
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
 * Same line count as a greedy wrap, broken so the lines come out even (the
 * site's text-wrap: balance). An article never ends a line, as on the site.
 */
function wrapBalanced(text, size, maxPx, lsEm) {
  const words = text.split(/\s+/);
  const target = wrap(text, size, maxPx, lsEm).length;
  if (target < 2) return [text];
  const ok = (line) => !/\b(a|an|the)$/i.test(line);

  let best = null;
  const walk = (start, remaining, acc) => {
    if (remaining === 1) {
      const lines = [...acc, words.slice(start).join(' ')];
      const widest = Math.max(...lines.map((l) => emWidth(l, lsEm) * size));
      if (widest <= maxPx && (!best || widest < best.widest)) best = { lines, widest };
      return;
    }
    for (let end = start + 1; end <= words.length - (remaining - 1); end++) {
      const line = words.slice(start, end).join(' ');
      if (emWidth(line, lsEm) * size > maxPx) break;
      if (ok(line)) walk(end, remaining - 1, [...acc, line]);
    }
  };
  walk(0, target, []);
  return best ? best.lines : wrap(text, size, maxPx, lsEm);
}

const CAP = 0.72; // Neue Montreal cap height, in em

// ── The statement (the hero's, verbatim), set as the hero sets it ──────────
const STATEMENT = 'Editorial instincts and creative acuity for clarifying a chaotic world';
const stmtSize = 60;
const stmtLS = -0.026;
const stmtLH = Math.round(stmtSize * 1.02);
// The hero holds the statement to 83% of the column.
const stmtLines = wrapBalanced(STATEMENT, stmtSize, INNER * 0.83, stmtLS);
const stmtTop = PAD + stmtSize * CAP;

// ── The name, fitted edge to edge, its baseline on the bottom margin ───────
const NAME = 'MIGUEL ESCOBAR';
const NAME_LS = -0.03;
const nameSize = fitSize(NAME, INNER, NAME_LS);
const nameBaseline = H - PAD + 6; // capitals sit on the baseline; nudge for the optical margin

// ── The glow: the hero's softened profile, centred where its arrow is ──────
const GLOW = [
  ['#1AB0E7', 0], ['#1BB4EA', 2.51], ['#1BB8EB', 4.98], ['#1CBCEC', 7.49], ['#1CBFEC', 10],
  ['#1FC1EB', 15.32], ['#27C1EA', 20.64], ['#43C2E8', 26.09], ['#59C6E6', 31.4], ['#6EC7E6', 36.72],
  ['#7DCBE4', 42.17], ['#8DCEE4', 47.49], ['#98D0E5', 52.81], ['#A6D4E4', 58.12], ['#B0D8E4', 63.57],
  ['#BCD9E4', 68.89], ['#C5DBE4', 74.21], ['#D0DFE4', 79.66], ['#D6E2E2', 84.98], ['#E2E4E3', 90.3],
  ['#E8E6E1', 95.75], ['#EAE7E1', 100],
];
const glowR = 210;
const glowCx = W - PAD - 30;
const glowCy = nameBaseline - nameSize * CAP - 92;

const svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="glow" cx="${glowCx}" cy="${glowCy}" r="${glowR}" gradientUnits="userSpaceOnUse">
      ${GLOW.map(([c, o]) => `<stop offset="${o}%" stop-color="${c}"/>`).join('')}
    </radialGradient>
  </defs>
  <rect width="${W}" height="${H}" fill="${PAPER}"/>
  <rect width="${W}" height="${H}" fill="url(#glow)"/>

  ${stmtLines
    .map(
      (l, i) =>
        `<text x="${PAD}" y="${(stmtTop + i * stmtLH).toFixed(1)}" font-family="${TEXT}" font-size="${stmtSize}" letter-spacing="${(stmtLS * stmtSize).toFixed(2)}" fill="${INK}">${esc(l)}</text>`
    )
    .join('\n  ')}

  <text x="${PAD}" y="${nameBaseline.toFixed(1)}" font-family="${TEXT}" font-size="${nameSize.toFixed(2)}"
        letter-spacing="${(NAME_LS * nameSize).toFixed(2)}" fill="${INK}">${esc(NAME)}</text>
</svg>`;

const png = new Resvg(svg, {
  fitTo: { mode: 'width', value: W },
  font: { fontFiles: [OTF], loadSystemFonts: false, defaultFontFamily: TEXT },
})
  .render()
  .asPng();

writeFileSync(path.join(outDir, 'og-image.png'), png);
console.log(
  `Wrote public/og-image.png (${W}x${H}) — statement ${stmtSize}px on ${stmtLines.length} line(s), name fitted at ${nameSize.toFixed(1)}px`
);
