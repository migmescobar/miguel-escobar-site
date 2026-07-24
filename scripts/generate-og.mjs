// Generate a 1200x630 Open Graph card that matches the site's design
// (paper #EAE7E1, ink #141414, Geist type). Run with: npm run assets:og
import { Resvg } from '@resvg/resvg-js';
import { writeFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const fonts = path.join(root, 'scripts/fonts');
const outDir = path.join(root, 'public');
mkdirSync(outDir, { recursive: true });

const PAPER = '#EAE7E1';
const INK = '#141414';

const svg = `<svg width="1200" height="630" viewBox="0 0 1200 630" xmlns="http://www.w3.org/2000/svg">
  <rect width="1200" height="630" fill="${PAPER}"/>
  <line x1="80" y1="132" x2="1120" y2="132" stroke="${INK}" stroke-opacity="0.3" stroke-width="1"/>
  <text x="80" y="112" font-family="Geist Mono" font-size="22" letter-spacing="3" fill="${INK}" fill-opacity="0.55">MIGUEL-ESCOBAR.COM</text>
  <text x="76" y="322" font-family="Geist Medium" font-size="130" letter-spacing="-5" fill="${INK}">Miguel Escobar</text>
  <text x="80" y="410" font-family="Geist" font-size="33" fill="${INK}" fill-opacity="0.72">Strategic Communications · Content Governance ·</text>
  <text x="80" y="456" font-family="Geist" font-size="33" fill="${INK}" fill-opacity="0.72">Editorial Operations · APAC Markets</text>
  <line x1="80" y1="522" x2="1120" y2="522" stroke="${INK}" stroke-opacity="0.2" stroke-width="1"/>
  <text x="80" y="566" font-family="Geist Mono" font-size="20" letter-spacing="2" fill="${INK}" fill-opacity="0.55">SINGAPORE · COMMUNICATIONS &amp; EDITORIAL</text>
</svg>`;

const resvg = new Resvg(svg, {
  fitTo: { mode: 'width', value: 1200 },
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
writeFileSync(path.join(outDir, 'og-image.png'), resvg.render().asPng());
console.log('Wrote public/og-image.png (1200x630)');
