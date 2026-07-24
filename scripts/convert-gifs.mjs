// Convert the two animated GIFs to looping, muted MP4 + WebM (plus a poster frame).
// GIFs are enormous (8.3 MB + 4.4 MB); H.264/VP9 cut that by ~90% with no visible loss.
// Run with: npm run assets:video
import { execFileSync } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import ffmpeg from 'ffmpeg-static';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const SRC = path.join(root, '_source/site-export/images');
const OUT = path.join(root, 'public/videos');
mkdirSync(OUT, { recursive: true });

// name in /public/videos  <-  source GIF
const jobs = [
  { name: 'alcon_bts', gif: 'ads_03_alcon_bts.gif' },
  { name: 'gotyme', gif: 'ads_04_gotyme.gif' },
];

const run = (args) => execFileSync(ffmpeg, ['-y', '-hide_banner', '-loglevel', 'error', ...args], { stdio: 'inherit' });
// keep dimensions even (yuv420p requirement)
const evenScale = 'scale=trunc(iw/2)*2:trunc(ih/2)*2';

for (const { name, gif } of jobs) {
  const input = path.join(SRC, gif);
  console.log(`→ ${gif}`);
  // MP4 (H.264) — universal fallback
  run(['-i', input, '-movflags', '+faststart', '-pix_fmt', 'yuv420p', '-vf', evenScale,
       '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-an', path.join(OUT, `${name}.mp4`)]);
  // WebM (VP9) — smaller where supported
  run(['-i', input, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '34', '-vf', evenScale,
       '-an', path.join(OUT, `${name}.webm`)]);
  // Poster (first frame) — shown before playback / as reduced-motion still
  run(['-i', input, '-vframes', '1', '-q:v', '3', path.join(OUT, `${name}.jpg`)]);
}
console.log('Done. Output in public/videos/');
