// On-brand, labeled placeholder images for every image slot on the site, so Miguel
// can redo the art. Each is paper/ink with the slot's subject, so you can tell which
// is which. Swap one out by dropping a real photo in src/assets/images and pointing
// the slot at it (see the README "Swapping in your real images" section).
// Run: node scripts/generate-placeholders.mjs
import { Resvg } from '@resvg/resvg-js';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const fontDir = path.join(root, 'scripts/fonts');
const PAPER = '#EAE7E1';
const INK = '#141414';

// w/h define the aspect ratio: 1200x900 = 4:3 (work rows). The home cards and the
// Editorial page now use real art (src/assets/images/{home,editorial}_*.png), so only
// the Advertising-page slots are generated here.
const items = [
  // Advertising rows (4:3)
  { file: 'ph_ads_trust.png', w: 1200, h: 900, eyebrow: 'TRUST BANK · SINGAPORE', lines: ['Trust Bank'] },
  { file: 'ph_ads_nba.png', w: 1200, h: 900, eyebrow: 'NBA · ASIA-PACIFIC', lines: ['NBA Newsletters'] },
  { file: 'ph_ads_alcon.png', w: 1200, h: 900, eyebrow: 'ALCON · APAC', lines: ['Alcon Campaigns'] },
  { file: 'ph_ads_gotyme.png', w: 1200, h: 900, eyebrow: 'GOTYME BANK · PH', lines: ['GoTyme Bank'] },
];

const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

const svgFor = ({ w, h, eyebrow, lines }) => {
  const size = h > w ? 82 : 72;
  const lh = size * 1.12;
  const startY = h * 0.5 - ((lines.length - 1) * lh) / 2 + size * 0.34;
  const title = lines
    .map(
      (t, i) =>
        `<text x="72" y="${(startY + i * lh).toFixed(0)}" font-family="Geist Medium" font-size="${size}" letter-spacing="-2" fill="${INK}">${esc(t)}</text>`
    )
    .join('');
  return `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg">
    <rect width="${w}" height="${h}" fill="${PAPER}"/>
    <rect x="24" y="24" width="${w - 48}" height="${h - 48}" fill="none" stroke="${INK}" stroke-opacity="0.18" stroke-width="1.5"/>
    <line x1="72" y1="150" x2="${w - 72}" y2="150" stroke="${INK}" stroke-opacity="0.3" stroke-width="1.5"/>
    <text x="72" y="128" font-family="Geist Mono" font-size="24" letter-spacing="3" fill="${INK}" fill-opacity="0.55">${esc(eyebrow)}</text>
    ${title}
    <line x1="72" y1="${h - 150}" x2="${w - 72}" y2="${h - 150}" stroke="${INK}" stroke-opacity="0.2" stroke-width="1.5"/>
    <text x="72" y="${h - 110}" font-family="Geist Mono" font-size="22" letter-spacing="3" fill="${INK}" fill-opacity="0.55">PLACEHOLDER IMAGE</text>
  </svg>`;
};

const fontFiles = [
  path.join(fontDir, 'Geist-Medium.ttf'),
  path.join(fontDir, 'Geist-Regular.ttf'),
  path.join(fontDir, 'GeistMono-Regular.ttf'),
];

for (const item of items) {
  const resvg = new Resvg(svgFor(item), {
    fitTo: { mode: 'width', value: item.w },
    font: { fontFiles, loadSystemFonts: false, defaultFontFamily: 'Geist' },
  });
  writeFileSync(path.join(root, 'src/assets/images', item.file), resvg.render().asPng());
  console.log('Wrote src/assets/images/' + item.file);
}
