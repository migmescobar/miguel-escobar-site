// Typed headlines (Home). A port of `type_chars` / `typed` in redesign-2026/source/gen_v47.py.
//
// Each character sits in its own span, numbered in typing order (--i), inside word spans that keep
// words whole. The subject phrase (`emph`) takes the accent: full ink against the quieter lead-in, and
// a full stop after it goes with it. Short emphasised pairs ("branded content") and articles stay on
// the line of the word after them. Screen readers get the plain sentence; the characters are hidden
// from them.

const ARTICLES = new Set(['a', 'an', 'the']);

const escape = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

/** Milliseconds per character: a headline types in about 1.4 s, never faster than 18 ms or slower than 34 ms. */
export function typingDt(n: number): number {
  return Math.max(18, Math.min(34, Math.round(1400 / n)));
}

export interface Typed {
  /** The aria-hidden character markup. */
  html: string;
  /** Characters typed (spaces excluded). */
  n: number;
  /** Milliseconds per character. */
  dt: number;
  /** When the paragraph under the headline starts to fade in: once the headline is 60% typed. */
  fd: number;
}

export function typeChars(text: string, emph = ''): Typed {
  const words = text.split(' ');
  const ew = emph ? emph.replace(/,/g, '').split(' ').filter(Boolean) : [];
  const bare = words.map((w) => w.replace(/[.,]$/, ''));
  let start = -1;
  if (ew.length) {
    for (let i = 0; i <= words.length - ew.length; i++) {
      if (ew.every((w, j) => bare[i + j] === w)) {
        start = i;
        break;
      }
    }
    if (start < 0) throw new Error(`Emphasis "${emph}" not found in "${text}"`);
  }
  const total = words.reduce((s, w) => s + [...w].length, 0);
  let k = 0;
  const spans = (s: string) =>
    [...s]
      .map((ch) => {
        k += 1;
        return `<span class="c${k === total ? ' last' : ''}" style="--i: ${k - 1};">${escape(ch)}</span>`;
      })
      .join('');

  const out = words.map((w, i) => {
    let inner: string;
    if (ew.length && i >= start && i < start + ew.length) {
      let [, core, punct] = w.match(/^(.*?)([.,]?)$/) as RegExpMatchArray;
      // A comma inside the phrase belongs to it; so does the closing full stop.
      if (i < start + ew.length - 1 || punct === '.') {
        core = w;
        punct = '';
      }
      inner = `<span class="me-em">${spans(core)}</span>${spans(punct)}`;
    } else {
      inner = spans(w);
    }
    return `<span class="w">${inner}</span>`;
  });

  // Word i is held to word i + 1.
  const binds = new Set<number>();
  if (ew.length > 1 && ew.length <= 2 && ew.join(' ').length <= 16) {
    for (let i = start; i < start + ew.length - 1; i++) binds.add(i);
  }
  bare.slice(0, -1).forEach((w, i) => {
    if (ARTICLES.has(w.toLowerCase())) binds.add(i);
  });
  const groups: string[][] = [[out[0]]];
  for (let i = 1; i < out.length; i++) {
    if (binds.has(i - 1)) groups[groups.length - 1].push(out[i]);
    else groups.push([out[i]]);
  }
  const html = groups
    .map((g) => (g.length === 1 ? g[0] : `<span style="white-space: nowrap;">${g.join(' ')}</span>`))
    .join(' ');
  const dt = typingDt(total);
  return { html, n: total, dt, fd: Math.round(total * dt * 0.6) };
}

/** Hyphenated compounds never split across lines; nor does a spaced dash from the word before it. */
export function keepCompounds(text: string): string {
  return text
    .split(/(<[^>]+>)/)
    .map((part) =>
      part.startsWith('<')
        ? part
        : part
            .replace(/ — /g, ' — ')
            .replace(/([^\s<>]+-[^\s<>]+)/g, '<span class="nw">$1</span>')
    )
    .join('');
}
