// Draw the site's icons: a plain circle in the site's cyan (#00AEEF, process
// cyan, the colour of the editorial work).
// Run: npm run assets:icons
//
//   public/favicon.svg           the icon browsers prefer; crisp at any size
//   public/favicon.png           512×512 fallback, transparent
//   public/apple-touch-icon.png  180×180, opaque (Apple requires it): the circle
//                                on the site's paper, inset so iOS's rounded
//                                corners never clip it
import sharp from 'sharp';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const out = (f) => path.join(root, 'public', f);

const CYAN = '#00AEEF';
const PAPER = '#F8F5D7';

// The circle fills 90% of the favicon's box, as the previous mark did.
const favicon = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><circle cx="256" cy="256" r="231" fill="${CYAN}"/></svg>\n`;
writeFileSync(out('favicon.svg'), favicon);

await sharp(Buffer.from(favicon)).resize(512, 512).png().toFile(out('favicon.png'));

const touch = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 180 180"><rect width="180" height="180" fill="${PAPER}"/><circle cx="90" cy="90" r="54" fill="${CYAN}"/></svg>`;
await sharp(Buffer.from(touch)).resize(180, 180).flatten({ background: PAPER }).png().toFile(out('apple-touch-icon.png'));

console.log('Wrote public/favicon.svg, favicon.png (512×512) and apple-touch-icon.png (180×180)');
