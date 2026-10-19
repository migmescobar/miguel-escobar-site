// Generate the 1200x630 Open Graph card. Run: npm run assets:og
//
// The card is Home's masthead in miniature (the sketch rebuild, board SkHome):
// butter paper, the nav's hairline across the top, the name in Writer capitals
// fitted edge to edge under it, the dateline, and the deck in its white box with
// the heavy black frame, centred below.
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
const SERIF_OTF = path.join(fonts, 'PPWriter-RegularText.otf');
const SANS_OTF = path.join(fonts, 'PPNeueYork-NormalMedium.otf');
const serif = openSync(SERIF_OTF);
const sans = openSync(SANS_OTF);
const SERIF = serif.familyName;
const SANS = sans.familyName;

const PAPER = '#F8F5D7';
const WHITE = '#FFFFFF';
const INK = '#000000';

const W = 1200;
const H = 630;
const PAD = 56;
const INNER = W - PAD * 2;
const CAP = 0.71; // Writer's and Neue York's cap height, in em

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Width of a string in em in a font, including SVG letter-spacing (applied per glyph). */
const emWidth = (font, s, lsEm) => font.layout(s).advanceWidth / font.unitsPerEm + lsEm * s.length;

// ── The nav's hairline ──────────────────────────────────────────────────────
const ruleY = PAD;

// ── The name: Writer capitals at the display tracking, fitted to the measure ─
const NAME = 'MIGUEL ESCOBAR';
const NAME_LS = -0.05;
const nameSize = (INNER / emWidth(serif, NAME, NAME_LS)) * 0.998;
const nameBaseline = ruleY + 0.2 * nameSize + nameSize * CAP;
const nameX = PAD - 0.03 * nameSize; // the site's optical margin for the M

// ── The dateline, as the site sets it from tablets up: 12px capitals, scaled ─
const LABEL = 17;
const labelBaseline = nameBaseline + 0.3 * nameSize - 0.125 * nameSize + LABEL * CAP;

// ── The deck: Neue York in three lines, centred in its framed white box ─────
const DECK = ['Editorial instincts and', 'creative acuity for', 'work that illuminates'];
const DECK_SIZE = 38;
const DECK_LH = DECK_SIZE * 1.25;
const FRAME = 6;
const deckW = Math.max(...DECK.map((l) => emWidth(sans, l, 0) * DECK_SIZE));
const boxW = deckW + 2 * 1.25 * DECK_SIZE + 2 * FRAME;
const padY = (1.25 - 0.268) * DECK_SIZE;
const boxH = DECK.length * DECK_LH - (DECK_LH - DECK_SIZE * CAP) + 2 * padY + 2 * FRAME;
const free = H - PAD - (labelBaseline + 24);
const boxY = labelBaseline + 24 + (free - boxH) / 2;
const boxX = (W - boxW) / 2;
const deckFirst = boxY + FRAME + padY + DECK_SIZE * CAP;

const svg = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
  <rect width="${W}" height="${H}" fill="${PAPER}"/>
  <rect x="${PAD}" y="${ruleY}" width="${INNER}" height="1" fill="${INK}"/>

  <text x="${nameX.toFixed(1)}" y="${nameBaseline.toFixed(1)}" font-family="${SERIF}" font-size="${nameSize.toFixed(2)}"
        letter-spacing="${(NAME_LS * nameSize).toFixed(2)}" fill="${INK}">${esc(NAME)}</text>

  <text x="${PAD}" y="${labelBaseline.toFixed(1)}" font-family="${SANS}" font-size="${LABEL}" fill="${INK}">SINGAPORE</text>
  <text x="${W - PAD}" y="${labelBaseline.toFixed(1)}" text-anchor="end" font-family="${SANS}" font-size="${LABEL}" fill="${INK}">MIGUEL-ESCOBAR.COM</text>

  <rect x="${(boxX + FRAME / 2).toFixed(1)}" y="${(boxY + FRAME / 2).toFixed(1)}" width="${(boxW - FRAME).toFixed(1)}" height="${(boxH - FRAME).toFixed(1)}"
        fill="${WHITE}" stroke="${INK}" stroke-width="${FRAME}"/>
  ${DECK.map(
    (l, i) =>
      `<text x="${W / 2}" y="${(deckFirst + i * DECK_LH).toFixed(1)}" text-anchor="middle" font-family="${SANS}" font-size="${DECK_SIZE}" fill="${INK}">${esc(l)}</text>`
  ).join('\n  ')}
</svg>`;

const png = new Resvg(svg, {
  fitTo: { mode: 'width', value: W },
  font: { fontFiles: [SERIF_OTF, SANS_OTF], loadSystemFonts: false, defaultFontFamily: SERIF },
})
  .render()
  .asPng();

writeFileSync(path.join(outDir, 'og-image.png'), png);
console.log(`Wrote public/og-image.png (${W}x${H}) — name fitted at ${nameSize.toFixed(1)}px`);
