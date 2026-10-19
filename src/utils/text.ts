// Markup for the sketch rebuild's moving type. Statements are written as plain
// strings with three marks:
//   *words*  emphasis (Neue York Narrow Extrabold, in the accent where there is one)
//   |        a line break from 900px up (the sketches' breaks; phones wrap freely)
//       a no-break space: the words either side stay together and move as one
// A full stop or comma after the closing * stays outside the emphasis.

const escape = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

interface Token {
  /** A line break comes before this word. */
  br: boolean;
  core: string;
  /** Punctuation after an emphasised core. */
  tail: string;
  em: boolean;
}

function tokens(text: string): Token[] {
  const out: Token[] = [];
  let em = false;
  let br = false;
  for (const raw of text.split(/ +/)) {
    if (raw === '|') {
      br = true;
      continue;
    }
    let w = raw;
    const opens = w.startsWith('*');
    if (opens) {
      em = true;
      w = w.slice(1);
    }
    const close = w.match(/^(.*)\*([.,;:!?]*)$/);
    if (close) {
      out.push({ br, core: close[1], tail: close[2], em: true });
      em = false;
    } else {
      out.push({ br, core: w, tail: '', em });
    }
    br = false;
  }
  return out;
}

const lb = (t: Token) => (t.br ? '<br class="lb">' : '');

/**
 * A line that rises a word at a time, each word inside its own mask. Goes in an
 * element with data-rise (the site script adds .is-in as it comes up the screen).
 */
export function rise(text: string): string {
  return tokens(text)
    .map((t, i) => {
      const inner = t.em ? `<span class="x">${escape(t.core)}</span>${escape(t.tail)}` : escape(t.core);
      return `${lb(t)}<span class="rw"><span style="--i: ${i}">${inner}</span></span>`;
    })
    .join(' ');
}

/**
 * A statement that fills in word by word as it's read. Goes in an element with
 * class "words", data-words and style="--n: <n>" (the count returned here).
 */
export function words(text: string): { html: string; n: number } {
  let i = 0;
  const html = tokens(text)
    .map((t) => {
      if (!t.em) return `${lb(t)}<span class="w lo" style="--i: ${i++}">${escape(t.core)}</span>`;
      const head = `${lb(t)}<span class="w hl" style="--i: ${i++}">${escape(t.core)}</span>`;
      return t.tail ? `${head}<span class="w lo" style="--i: ${i++}">${escape(t.tail)}</span>` : head;
    })
    .join(' ');
  return { html, n: i };
}

/** Hyphenated compounds never split across lines; nor does a spaced dash from the word before it. */
export function keepCompounds(text: string): string {
  return text
    .split(/(<[^>]+>)/)
    .map((part) =>
      part.startsWith('<')
        ? part
        : part.replace(/ — /g, ' — ').replace(/([^\s<>]+-[^\s<>]+)/g, '<span class="nw">$1</span>')
    )
    .join('');
}
