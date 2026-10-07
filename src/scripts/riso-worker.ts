// Draws one risograph halftone glow, off the main thread. See riso-glow.ts.
//
// Colour: the glow's own CSS gradient (all its stops) is reproduced exactly on
// average. At each radius the gradient's colour G is split into a dot coverage
// `a` (the share of a halftone cell under ink) and an ink colour X, with
// paper × (1 − a) + X × a = G. Coverage comes from fitting one cyan ink to the
// whole gradient, so dot sizes change smoothly; the ink then drifts a little
// with radius (it stays within a narrow cyan band) to make the sum exact.
//
// Texture, after a riso print: a 12px screen at 45°, round dots that grow and
// merge into a mesh with star-shaped paper gaps; ragged dot edges (ink spread),
// slight dot misregistration, low-frequency ink mottling, fine ink grain, and
// the paper's grain showing through, fading out with the print. Every
// irregularity averages to zero, so the colour stays exact, and every random
// number is seeded, so the print is the same on every visit.

export interface RisoJob {
  id: number;
  /** CSS px. */
  w: number;
  h: number;
  dpr: number;
  /** Gradient stops: radius in CSS px from the centre, sRGB colour. */
  stops: { r: number; rgb: [number, number, number] }[];
}

const PAPER = [0xea, 0xe7, 0xe1];
const INK_FIT = [0, 178, 237]; // the single cyan ink that best fits the gradient
const SPACING = 12;
const ANGLE = (45 * Math.PI) / 180;
const COS = Math.cos(ANGLE);
const SIN = Math.sin(ANGLE);

// ── Seeded noise ────────────────────────────────────────────────────────────
function hash(x: number, y: number, seed: number): number {
  let h = Math.imul(x | 0, 374761393) ^ Math.imul(y | 0, 668265263) ^ Math.imul(seed, 2246822519);
  h = Math.imul(h ^ (h >>> 13), 1274126177);
  h ^= h >>> 16;
  return (h >>> 0) / 4294967296;
}
/** Smooth value noise in [0, 1), feature size `scale` (same units as x, y). */
function vnoise(x: number, y: number, scale: number, seed: number): number {
  const fx = x / scale;
  const fy = y / scale;
  const ix = Math.floor(fx);
  const iy = Math.floor(fy);
  let tx = fx - ix;
  let ty = fy - iy;
  tx = tx * tx * (3 - 2 * tx);
  ty = ty * ty * (3 - 2 * ty);
  const a = hash(ix, iy, seed);
  const b = hash(ix + 1, iy, seed);
  const c = hash(ix, iy + 1, seed);
  const d = hash(ix + 1, iy + 1, seed);
  return a + (b - a) * tx + (c - a) * ty + (a - b - c + d) * tx * ty;
}

// The jitter and edge noise every dot gets (render() uses these too).
const jitterX = (i: number, j: number) => (hash(i, j, 11) - 0.5) * 0.7;
const jitterY = (i: number, j: number) => (hash(i, j, 12) - 0.5) * 0.7;
const roughAt = (lx: number, ly: number) => (vnoise(lx, ly, 1.6, 21) - 0.5) * 0.9;

// Where dots are big enough to merge, a point can lie under a neighbour's dot
// (misregistration moves them), so coverage there is the union over the 3×3
// dots around the point; smaller dots only ever cover their own cell.
const MERGE = 0.42 * SPACING;

/** Ink coverage (0..1) of the point (lx, ly) in the screen's frame; `size(i, j, gx, gy)` gives a dot's radius. */
function coverAt(lx: number, ly: number, dpr: number, size: (i: number, j: number, gx: number, gy: number) => number): number {
  const i0 = Math.round(lx / SPACING);
  const j0 = Math.round(ly / SPACING);
  const rough = roughAt(lx, ly);
  const one = (i: number, j: number) => {
    const gx = i * SPACING + jitterX(i, j);
    const gy = j * SPACING + jitterY(i, j);
    const r = size(i, j, gx, gy);
    if (r <= 0) return { r, c: 0 };
    return { r, c: Math.min(1, Math.max(0, (r + rough - Math.hypot(lx - gx, ly - gy)) * dpr + 0.5)) };
  };
  const own = one(i0, j0);
  if (own.r < MERGE || own.c >= 1) return own.c;
  let c = own.c;
  for (let i = i0 - 1; i <= i0 + 1; i++) {
    for (let j = j0 - 1; j <= j0 + 1; j++) {
      if (i === i0 && j === j0) continue;
      c = Math.max(c, one(i, j).c);
      if (c >= 1) return 1;
    }
  }
  return c;
}

// Dot gain, calibrated: misregistration and ragged edges change how much of a
// cell a dot of a given size really covers (where dots merge, they open more
// paper than they close), so the size each coverage needs is measured on this
// screen itself, the way a print shop calibrates its screen, rather than taken
// from the ideal geometry: 160 dot sizes, each over 16×16 cells at 64 random
// points a cell, with the same rule render() uses.
const RADIUS_FOR = (() => {
  const SIZES = 160;
  const rMax = Math.SQRT1_2 * SPACING + 1.5;
  const measured = new Float32Array(SIZES + 1);
  const CELLS = 16;
  const PER = 8; // stratified samples per cell side
  for (let s = 0; s <= SIZES; s++) {
    const r = (s / SIZES) * rMax;
    let sum = 0;
    let n = 0;
    for (let cy = 0; cy < CELLS; cy++) {
      for (let cx = 0; cx < CELLS; cx++) {
        for (let sy = 0; sy < PER; sy++) {
          for (let sx = 0; sx < PER; sx++) {
            const lx = (cx - 0.5 + (sx + hash(cx * PER + sx, cy * PER + sy, 61)) / PER) * SPACING;
            const ly = (cy - 0.5 + (sy + hash(cx * PER + sx, cy * PER + sy, 62)) / PER) * SPACING;
            sum += r > 0 ? coverAt(lx, ly, 8, () => r) : 0;
            n++;
          }
        }
      }
    }
    measured[s] = sum / n;
  }
  // Coverage only grows with size; then invert: coverage (0..1, 1024 steps) → radius in px.
  for (let s = 1; s <= SIZES; s++) measured[s] = Math.max(measured[s], measured[s - 1]);
  const n = 1024;
  const t = new Float32Array(n + 1);
  let s = 0;
  for (let k = 1; k <= n; k++) {
    const want = k / n;
    while (s < SIZES && measured[s + 1] < want) s++;
    if (s >= SIZES) {
      t[k] = rMax;
      continue;
    }
    const a = measured[s];
    const b = measured[s + 1];
    const f = b > a ? Math.min(1, Math.max(0, (want - a) / (b - a))) : 0;
    t[k] = ((s + f) / SIZES) * rMax;
  }
  return t;
})();

// ── The gradient, split into coverage and ink ──────────────────────────────
function colourAt(stops: RisoJob['stops'], r: number): number[] {
  if (r <= stops[0].r) return stops[0].rgb.slice();
  for (let i = 1; i < stops.length; i++) {
    if (r <= stops[i].r) {
      const a = stops[i - 1];
      const b = stops[i];
      const t = b.r === a.r ? 1 : (r - a.r) / (b.r - a.r);
      return [0, 1, 2].map((k) => a.rgb[k] + (b.rgb[k] - a.rgb[k]) * t);
    }
  }
  return stops[stops.length - 1].rgb.slice();
}
function split(g: number[]): { a: number; ink: number[] } {
  // Best coverage for the fitted ink…
  let num = 0;
  let den = 0;
  for (let k = 0; k < 3; k++) {
    num += (g[k] - PAPER[k]) * (INK_FIT[k] - PAPER[k]);
    den += (INK_FIT[k] - PAPER[k]) ** 2;
  }
  let a = Math.max(0, Math.min(1, num / den));
  // …raised where needed so the exact ink stays a real (in-gamut) colour.
  for (let k = 0; k < 3; k++) {
    const d = g[k] - PAPER[k];
    if (d < 0) a = Math.max(a, -d / PAPER[k]);
    else if (d > 0) a = Math.max(a, d / (255 - PAPER[k]));
  }
  a = Math.min(1, a);
  if (a < 0.004) return { a: 0, ink: INK_FIT.slice() };
  let ink = [0, 1, 2].map((k) => Math.min(255, Math.max(0, PAPER[k] + (g[k] - PAPER[k]) / a)));
  // Where the print thins out, the exact ink would drift towards violet-blue,
  // which no single ink does; there the dots keep to the fitted cyan, at the
  // coverage that best matches the gradient with it (a few 1/255ths off, on
  // dots too sparse to tell).
  const HOLD = 0.4;
  if (a < HOLD) {
    const t = (HOLD - a) / HOLD;
    ink = ink.map((v, k) => v + (INK_FIT[k] - v) * t);
    let n2 = 0;
    let d2 = 0;
    for (let k = 0; k < 3; k++) {
      n2 += (g[k] - PAPER[k]) * (ink[k] - PAPER[k]);
      d2 += (ink[k] - PAPER[k]) ** 2;
    }
    a = Math.max(0, Math.min(1, n2 / d2));
  }
  return { a, ink };
}

function render(job: RisoJob): Uint8ClampedArray {
  const { w, h, dpr, stops } = job;
  const W = Math.round(w * dpr);
  const H = Math.round(h * dpr);
  const out = new Uint8ClampedArray(W * H * 4);
  const cx = w / 2;
  const cy = h / 2;
  const reach = stops[stops.length - 1].r;

  // Coverage, dot radius and ink tabulated by radius (every ¼ px).
  const STEP = 0.25;
  const N = Math.ceil(reach / STEP) + 2;
  const covT = new Float32Array(N);
  const radT = new Float32Array(N);
  const inkT = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const { a, ink } = split(colourAt(stops, i * STEP));
    covT[i] = a;
    radT[i] = RADIUS_FOR[Math.round(a * 1024)];
    inkT[i * 3] = ink[0];
    inkT[i * 3 + 1] = ink[1];
    inkT[i * 3 + 2] = ink[2];
  }
  const at = (r: number) => Math.min(N - 1, Math.round(r / STEP));

  for (let py = 0; py < H; py++) {
    for (let px = 0; px < W; px++) {
      const ux = (px + 0.5) / dpr - cx; // CSS px from the centre
      const uy = (py + 0.5) / dpr - cy;
      const rp = Math.hypot(ux, uy);
      if (rp > reach + SPACING) continue;

      // Into the screen's frame. Each dot's size and ink are those of its own
      // centre's radius; misregistration moves each dot up to ±0.35px and ink
      // spread makes its edge wander by up to ±0.45px (see coverAt).
      const lx = ux * COS + uy * SIN;
      const ly = -ux * SIN + uy * COS;
      const i = Math.round(lx / SPACING);
      const j = Math.round(ly / SPACING);
      const ogx = i * SPACING + jitterX(i, j);
      const ogy = j * SPACING + jitterY(i, j);
      const ti = at(Math.hypot(ogx * COS - ogy * SIN, ogx * SIN + ogy * COS));
      const cover = coverAt(lx, ly, dpr, (_i, _j, gx, gy) => radT[at(Math.hypot(gx * COS - gy * SIN, gx * SIN + gy * COS))]);

      // Paper grain under the print, fading out with the print's density.
      const pi = at(rp);
      const grainAlpha = Math.min(1, covT[pi] / 0.85);
      const n = (hash(px, py, 31) - 0.5) * 9;
      const paper = [PAPER[0] + n, PAPER[1] + n * 0.95, PAPER[2] + n * 0.85];

      // Ink: mottled at a ~28px scale (±3%), with fine grain, and overprinted
      // on the grained paper (multiply).
      const mottle = 1 + (vnoise(ux, uy, 28, 41) - 0.5) * 0.06;
      const fine = 1 + (hash(px, py, 51) - 0.5) * 0.05;
      const k = mottle * fine;
      const ink = [0, 1, 2].map((c) => Math.min(255, inkT[ti * 3 + c] * k * (paper[c] / PAPER[c])));

      const alpha = cover + grainAlpha * (1 - cover);
      if (alpha <= 0) continue;
      const o = (py * W + px) * 4;
      for (let c = 0; c < 3; c++) out[o + c] = (ink[c] * cover + paper[c] * grainAlpha * (1 - cover)) / alpha;
      out[o + 3] = alpha * 255;
    }
  }
  return out;
}

self.onmessage = (e: MessageEvent<RisoJob>) => {
  const data = render(e.data);
  (self as unknown as Worker).postMessage({ id: e.data.id, data }, [data.buffer]);
};
