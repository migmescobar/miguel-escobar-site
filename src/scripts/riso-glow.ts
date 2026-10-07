// Risograph halftone glows (RISO_GLOWS in src/consts.ts).
//
// Each element marked data-riso keeps its smooth CSS gradient as the fallback.
// This reads that gradient's stops from the element's computed style (so the
// print always matches the CSS exactly, at every breakpoint), has a worker
// draw the halftone at the element's size, lays it in a canvas over the
// gradient, fades it in, and then drops the gradient. Without JavaScript, or
// if anything fails, the gradient simply stays.
import type { RisoJob } from './riso-worker';

type Stop = RisoJob['stops'][number];

/**
 * Stops of a CSS radial-gradient as the browser computes it: rgb() colours,
 * positions in px or %. Browsers leave out any position that CSS would put
 * there anyway (one exactly halfway between its neighbours), so missing
 * positions are restored by CSS's own rules: the first stop at 0, the last at
 * the end of the ray, the rest spaced evenly between the nearest stops that
 * have one, and none before the stop ahead of it.
 */
function parseStops(bg: string, w: number, h: number): Stop[] | null {
  if (!bg.startsWith('radial-gradient(')) return null;
  const body = bg.slice(bg.indexOf('(') + 1, bg.lastIndexOf(')'));
  // Split on commas outside parentheses.
  const parts: string[] = [];
  let depth = 0;
  let cur = '';
  for (const ch of body) {
    if (ch === '(') depth++;
    if (ch === ')') depth--;
    if (ch === ',' && depth === 0) {
      parts.push(cur.trim());
      cur = '';
    } else cur += ch;
  }
  parts.push(cur.trim());
  if (!/^rgba?\(/.test(parts[0])) parts.shift(); // shape, size, position

  // Percentages run along the gradient ray: closest-side here, else the
  // default farthest-corner.
  const ray = /closest-side/.test(bg) ? Math.min(w, h) / 2 : Math.hypot(w / 2, h / 2);
  const raw: { rgb: [number, number, number]; r: number | null }[] = [];
  for (const part of parts) {
    const m = part.match(/^rgba?\((\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?),\s*(\d+(?:\.\d+)?)(?:,\s*[\d.]+)?\)\s*(.*)$/);
    if (!m) return null;
    const rgb: [number, number, number] = [+m[1], +m[2], +m[3]];
    const positions = m[4].split(/\s+/).filter(Boolean);
    const toPx = (p: string) => (p.endsWith('%') ? (parseFloat(p) / 100) * ray : parseFloat(p));
    if (!positions.length) raw.push({ rgb, r: null });
    // A stop with two positions is two stops of the same colour.
    for (const p of positions) raw.push({ rgb, r: toPx(p) });
  }
  if (raw.length < 2) return null;
  if (raw[0].r === null) raw[0].r = 0;
  if (raw[raw.length - 1].r === null) raw[raw.length - 1].r = ray;
  for (let i = 1; i < raw.length; i++) {
    if (raw[i].r === null) {
      let j = i;
      while (raw[j].r === null) j++;
      const a = raw[i - 1].r!;
      const b = raw[j].r!;
      for (let k = i; k < j; k++) raw[k].r = a + ((b - a) * (k - i + 1)) / (j - i + 1);
    }
    raw[i].r = Math.max(raw[i].r!, raw[i - 1].r!);
  }
  return raw.map((s) => ({ r: s.r!, rgb: s.rgb }));
}

export function initRisoGlows() {
  const els = [...document.querySelectorAll<HTMLElement>('[data-riso]')];
  if (!els.length || !('Worker' in window)) return;
  let worker: Worker;
  try {
    worker = new Worker(new URL('./riso-worker.ts', import.meta.url), { type: 'module' });
  } catch {
    return;
  }
  let nextId = 1;
  const pending = new Map<number, (data: Uint8ClampedArray) => void>();
  worker.onmessage = (e) => {
    const cb = pending.get(e.data.id);
    pending.delete(e.data.id);
    cb?.(e.data.data);
  };

  const drawn = new WeakMap<HTMLElement, string>();
  const draw = (el: HTMLElement) => {
    const w = el.offsetWidth;
    const h = el.offsetHeight;
    if (!w || !h) return;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const key = `${w}x${h}@${dpr}`;
    if (drawn.get(el) === key) return;
    // Read the gradient with it showing (it is hidden once a print is in).
    el.classList.remove('riso-done');
    const stops = parseStops(getComputedStyle(el).backgroundImage, w, h);
    if (!stops) return;
    drawn.set(el, key);
    const id = nextId++;
    pending.set(id, (data) => {
      if (drawn.get(el) !== key) return; // superseded by a newer size
      const canvas = document.createElement('canvas');
      canvas.className = 'me-riso';
      canvas.width = Math.round(w * dpr);
      canvas.height = Math.round(h * dpr);
      canvas.setAttribute('aria-hidden', 'true');
      canvas.getContext('2d')!.putImageData(new ImageData(data, canvas.width, canvas.height), 0, 0);
      el.querySelector('.me-riso')?.remove();
      el.append(canvas);
      // Fade the print in over the gradient, then drop the gradient. (Read a
      // layout value first, so the print's starting opacity is applied before
      // it changes; and don't depend on transitionend alone, which never
      // fires if the transition doesn't run.)
      void canvas.offsetWidth;
      canvas.classList.add('is-in');
      let finished = false;
      const done = () => {
        if (finished) return;
        finished = true;
        el.classList.add('riso-done');
      };
      if (matchMedia('(prefers-reduced-motion: reduce)').matches) done();
      else {
        canvas.addEventListener('transitionend', done, { once: true });
        setTimeout(done, 700);
      }
    });
    worker.postMessage({ id, w, h, dpr, stops } satisfies RisoJob);
  };

  // Draw each glow as it nears the screen (the hero's at once), and again if
  // its size changes (a breakpoint).
  const io = new IntersectionObserver(
    (entries) => {
      for (const en of entries) if (en.isIntersecting) draw(en.target as HTMLElement);
    },
    { rootMargin: '100% 0px' }
  );
  const ro = new ResizeObserver((entries) => {
    for (const en of entries) {
      const el = en.target as HTMLElement;
      if (drawn.has(el)) draw(el);
    }
  });
  els.forEach((el) => {
    io.observe(el);
    ro.observe(el);
  });
}
