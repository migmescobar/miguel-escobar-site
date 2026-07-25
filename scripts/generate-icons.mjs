// Derive a 180x180 apple-touch-icon from the site favicon (public/favicon.png).
// Apple touch icons must be opaque, so the transparent PNG is flattened onto white.
// Run: node scripts/generate-icons.mjs
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';

await sharp(path.join(root, 'public/favicon.png'))
  .resize(180, 180, { fit: 'contain', background: '#ffffff' })
  .flatten({ background: '#ffffff' })
  .png()
  .toFile(path.join(root, 'public/apple-touch-icon.png'));

console.log('Wrote public/apple-touch-icon.png (180x180) from public/favicon.png');
