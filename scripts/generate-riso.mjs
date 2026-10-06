// Risograph halftone versions of Home's three glows (the hero arrow's, Policy's,
// and Singapore's pulse on the map). Run: npm run assets:riso
//
// Each is a disc of cyan dots on a rotated screen whose dots shrink from the
// centre out, overprinted (multiply) on the site's paper with the paper's grain
// — Mig's reference sketch, its settings verbatim: #1ab0e7 ink, 9px screen at
// 20°, dots up to 6.5px radius, size ∝ (1 − d/reach)^0.4, grain ±6.6.
//
// The overprint is baked in rather than left to mix-blend-mode: every glow lies
// on paper, so ink × paper is known, and the browser needn't composite it. The
// grain lives only where the print does and fades out with it, so the disc has
// no edge on the flat paper around it. Output is 2× (sharp on retina screens)
// and transparent outside the print; WebP, as the grain doesn't compress losslessly.
//
// Toggle on the site: RISO_GLOWS in src/consts.ts.
import sharp from 'sharp';
import { mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';
const outDir = path.join(root, 'public/media/riso');
mkdirSync(outDir, { recursive: true });

const INK = [0x1a, 0xb0, 0xe7];
const PAPER = [0xea, 0xe7, 0xe1];
const SPACING = 9;
const MAX_R = 6.5;
const ANGLE = (20 * Math.PI) / 180;
const FALLOFF = 0.4;
const GRAIN = 13.25; // the sketch's (Math.random() - 0.5) * 13.25
const SCALE = 2;

// A fixed seed, so regenerating gives the same grain (and a clean git diff).
let seed = 20261006;
const rand = () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 4294967296);

const cos = Math.cos(ANGLE);
const sin = Math.sin(ANGLE);

/** One disc of reach `R` CSS px, rendered at 2×. */
function disc(name, R) {
  const N = Math.ceil(2 * R * SCALE);
  const c = N / 2 / SCALE; // centre, in CSS px
  const px = Buffer.alloc(N * N * 4);
  const intensity = (d) => Math.pow(Math.max(0, 1 - d / R), FALLOFF);

  for (let y = 0; y < N; y++) {
    for (let x = 0; x < N; x++) {
      const ux = (x + 0.5) / SCALE - c;
      const uy = (y + 0.5) / SCALE - c;
      // Into the screen's frame (rotated by −20°), lattice anchored at the centre.
      const lx = ux * cos + uy * sin;
      const ly = -ux * sin + uy * cos;
      const i0 = Math.round(lx / SPACING);
      const j0 = Math.round(ly / SPACING);
      let cover = 0;
      for (let i = i0 - 1; i <= i0 + 1; i++) {
        for (let j = j0 - 1; j <= j0 + 1; j++) {
          const gx = i * SPACING;
          const gy = j * SPACING;
          // The dot's centre back in page space, and its size from its distance out.
          const dx = gx * cos - gy * sin;
          const dy = gx * sin + gy * cos;
          const r = MAX_R * intensity(Math.hypot(dx, dy));
          if (r <= 0.3) continue;
          const d = Math.hypot(ux - dx, uy - dy);
          cover = Math.max(cover, Math.min(1, Math.max(0, (r - d) * SCALE + 0.5)));
        }
      }
      const n = (rand() - 0.5) * GRAIN;
      const paper = [PAPER[0] + n, PAPER[1] + n * 0.95, PAPER[2] + n * 0.85];
      // Ink overprinted on grained paper; paper alone where there's no ink.
      const col = paper.map((p, k) => p * (1 - cover) + ((p * INK[k]) / 255) * cover);
      // The grain shows only within the print, fading out with it.
      const reach = intensity(Math.hypot(ux, uy));
      const alpha = Math.max(cover, reach > 0 ? Math.min(1, reach * 1.2) : 0);
      const o = (y * N + x) * 4;
      px[o] = Math.round(Math.min(255, Math.max(0, col[0])));
      px[o + 1] = Math.round(Math.min(255, Math.max(0, col[1])));
      px[o + 2] = Math.round(Math.min(255, Math.max(0, col[2])));
      px[o + 3] = Math.round(alpha * 255);
    }
  }
  return sharp(px, { raw: { width: N, height: N, channels: 4 } })
    // Lossy colour (the grain is noise; no one sees it compressed), near-lossless
    // alpha (the dots' edges).
    .webp({ quality: 78, alphaQuality: 100, effort: 6 })
    .toFile(path.join(outDir, `${name}.webp`))
    .then((info) => console.log(`${name}.webp  ${N}×${N}  ${(info.size / 1024).toFixed(0)} KB`));
}

// Reaches, in CSS px, of the glows they replace (src/styles/home.css and the maps).
await disc('cue-d', 220); // hero arrow, desktop (440px box, closest-side)
await disc('cue-m', 180); // hero arrow, phone
await disc('pol-d', 430); // Policy, desktop (860px)
await disc('pol-m', 200); // Policy, phone (400px)
await disc('map-d', 113.1); // Singapore's pulse, desktop map (1 unit ≈ 1px)
await disc('map-m', 54.1); // Singapore's pulse, phone map
