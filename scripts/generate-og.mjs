// Generate a 1200x630 Open Graph card that matches the site's design
// (paper #EAE7E1, ink #141414, Geist type). Run with: npm run assets:og
import { Resvg } from '@resvg/resvg-js';
import { openSync } from 'fontkit';
import { writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const fonts = path.join(root, 'scripts/fonts');
const outDir = path.join(root, 'public');
mkdirSync(outDir, { recursive: true });

// resvg matches fonts by their internal family name. The Fontshare Gambarino
// WEBfont has an obfuscated internal name (the site's @font-face renames it to
// "Gambarino"), so read whatever the file actually declares and use that.
const GAMBARINO = openSync(path.join(fonts, 'Gambarino-Regular.ttf')).familyName;

const PAPER = '#EAE7E1';
const INK = '#141414';
const BRAND = '#0047bb';

const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="${PAPER}"/>
  <circle cx="102" cy="94" r="22" fill="${BRAND}"/>
  <text x="146" y="103" font-family="Geist Mono" font-size="22" letter-spacing="3" fill="${INK}" fill-opacity="0.55">MIGUEL-ESCOBAR.COM</text>
  <line x1="80" y1="150" x2="1120" y2="150" stroke="${INK}" stroke-opacity="0.3" stroke-width="1"/>
  <text x="74" y="348" font-family="${GAMBARINO}" font-size="122" letter-spacing="-1.5" fill="${INK}">Miguel Escobar</text>
  <text x="80" y="438" font-family="Geist" font-size="33" fill="${INK}" fill-opacity="0.72">Strategic Communications · Content Governance ·</text>
  <text x="80" y="484" font-family="Geist" font-size="33" fill="${INK}" fill-opacity="0.72">Editorial Operations · APAC Markets</text>
  <line x1="80" y1="544" x2="1120" y2="544" stroke="${INK}" stroke-opacity="0.2" stroke-width="1"/>
  <text x="80" y="586" font-family="Geist Mono" font-size="20" letter-spacing="2" fill="${INK}" fill-opacity="0.55">SINGAPORE · COMMUNICATIONS &amp; EDITORIAL</text>
</svg>`;

const resvg = new Resvg(svg, {
  fitTo: { mode: 'width', value: 1200 },
  font: {
    fontFiles: [
      path.join(fonts, 'Gambarino-Regular.ttf'),
      path.join(fonts, 'Geist-Medium.ttf'),
      path.join(fonts, 'Geist-Regular.ttf'),
      path.join(fonts, 'GeistMono-Regular.ttf'),
    ],
    loadSystemFonts: false,
    defaultFontFamily: 'Geist',
  },
});
writeFileSync(path.join(outDir, 'og-image.png'), resvg.render().asPng());
console.log('Wrote public/og-image.png (1200x630)');
