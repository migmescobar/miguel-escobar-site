// One-off: make an on-brand 16:9 placeholder hero for the seed writing post.
// Miguel can replace it by dropping a real photo in src/assets/images and
// pointing the post's heroImage at it. Run: node scripts/generate-placeholder-hero.mjs
import { Resvg } from '@resvg/resvg-js';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const fonts = path.join(root, 'scripts/fonts');
const PAPER = '#EAE7E1';
const INK = '#141414';

const svg = `<svg width="1600" height="900" viewBox="0 0 1600 900" xmlns="http://www.w3.org/2000/svg">
  <rect width="1600" height="900" fill="${PAPER}"/>
  <line x1="120" y1="176" x2="1480" y2="176" stroke="${INK}" stroke-opacity="0.3" stroke-width="1.5"/>
  <text x="120" y="150" font-family="Geist Mono" font-size="26" letter-spacing="4" fill="${INK}" fill-opacity="0.55">MIGUEL ESCOBAR · WRITING</text>
  <text x="116" y="500" font-family="Geist Medium" font-size="128" letter-spacing="-5" fill="${INK}">Welcome</text>
  <text x="120" y="740" font-family="Geist" font-size="34" fill="${INK}" fill-opacity="0.6">Placeholder header image — swap me for a real photo.</text>
  <line x1="120" y1="760" x2="1480" y2="760" stroke="${INK}" stroke-opacity="0.2" stroke-width="1.5"/>
</svg>`;

const resvg = new Resvg(svg, {
  fitTo: { mode: 'width', value: 1600 },
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
writeFileSync(path.join(root, 'src/assets/images/writing_welcome_hero.png'), resvg.render().asPng());
console.log('Wrote src/assets/images/writing_welcome_hero.png (1600x900)');
