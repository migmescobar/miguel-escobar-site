// Render the favicon into a 180x180 apple-touch-icon PNG (opaque, ink background).
// Run: node scripts/generate-icons.mjs
import { Resvg } from '@resvg/resvg-js';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180">
  <rect width="180" height="180" fill="#141414"/>
  <path d="M46 132 V54 L90 104 L134 54 V132" fill="none" stroke="#EAE7E1" stroke-width="13" stroke-linejoin="round" stroke-linecap="round"/>
</svg>`;

const resvg = new Resvg(svg, { fitTo: { mode: 'width', value: 180 } });
writeFileSync(path.join(root, 'public/apple-touch-icon.png'), resvg.render().asPng());
console.log('Wrote public/apple-touch-icon.png (180x180)');
