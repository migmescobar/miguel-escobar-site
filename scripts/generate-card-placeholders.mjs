// On-brand 3:4 placeholder images for the two home cards that don't have photos yet
// (Age Checks Matter, Online Safety Commission). Swap in real film/launch stills later
// by dropping a photo in src/assets/images and pointing the card at it.
// Run: node scripts/generate-card-placeholders.mjs
import { Resvg } from '@resvg/resvg-js';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const fonts = path.join(root, 'scripts/fonts');
const PAPER = '#EAE7E1';
const INK = '#141414';
const W = 900;
const H = 1200;

const cards = [
  { file: 'home_05_age_checks_placeholder.png', eyebrow: 'SINGAPORE · IMDA', lines: ['Age Checks', 'Matter'] },
  { file: 'home_06_osc_placeholder.png', eyebrow: 'SINGAPORE · ONLINE SAFETY', lines: ['Online Safety', 'Commission'] },
];

const svgFor = ({ eyebrow, lines }) => {
  const titleY = 560;
  const lh = 96;
  const title = lines
    .map((t, i) => `<text x="72" y="${titleY + i * lh}" font-family="Geist Medium" font-size="88" letter-spacing="-3" fill="${INK}">${t}</text>`)
    .join('');
  return `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${W}" height="${H}" fill="${PAPER}"/>
    <rect x="24" y="24" width="${W - 48}" height="${H - 48}" fill="none" stroke="${INK}" stroke-opacity="0.18" stroke-width="1.5"/>
    <line x1="72" y1="150" x2="${W - 72}" y2="150" stroke="${INK}" stroke-opacity="0.3" stroke-width="1.5"/>
    <text x="72" y="128" font-family="Geist Mono" font-size="24" letter-spacing="3" fill="${INK}" fill-opacity="0.55">${eyebrow}</text>
    ${title}
    <line x1="72" y1="${H - 150}" x2="${W - 72}" y2="${H - 150}" stroke="${INK}" stroke-opacity="0.2" stroke-width="1.5"/>
    <text x="72" y="${H - 110}" font-family="Geist Mono" font-size="22" letter-spacing="3" fill="${INK}" fill-opacity="0.55">PLACEHOLDER IMAGE</text>
  </svg>`;
};

for (const card of cards) {
  const resvg = new Resvg(svgFor(card), {
    fitTo: { mode: 'width', value: W },
    font: {
      fontFiles: [
        path.join(fonts, 'Geist-Medium.ttf'),
        path.join(fonts, 'Geist-Regular.ttf'),
        path.join(fonts, 'GeistMono-Regular.ttf'),
      ],
      loadSystemFonts: false,
      defaultFontFamily: 'Geist',
    },
  });
  writeFileSync(path.join(root, 'src/assets/images', card.file), resvg.render().asPng());
  console.log('Wrote src/assets/images/' + card.file);
}
