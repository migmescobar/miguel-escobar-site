// Thoughts post titles are plain strings (used verbatim in <title>, OG/Twitter
// meta, and JSON-LD — contexts where HTML tags aren't valid), but the ON-PAGE
// headline sometimes needs a word italicised (e.g. a movie title). Titles may
// mark that with the same *asterisk* syntax as the Markdown body; these two
// helpers are the only two ways that's ever consumed:
//   - parseTitleParts: for rendering the visible headline as mixed text/<em>.
//   - plainTitle: for every metadata surface, where the markers are stripped.
export interface TitlePart {
  text: string;
  em: boolean;
}

export function parseTitleParts(raw: string): TitlePart[] {
  return raw
    .split(/\*([^*]+)\*/g)
    .map((text, i) => ({ text, em: i % 2 === 1 }))
    .filter((part) => part.text.length > 0);
}

export function plainTitle(raw: string): string {
  return raw.replace(/\*([^*]+)\*/g, '$1');
}

/**
 * Line-breaking for headlines, as the redesign sets them: an article never ends a
 * line (it stays with the word after it), and a word stays with an opening quote
 * that follows it ("Nolan’s “Odyssey”").
 */
export function bindWords(text: string): string {
  return text.replace(/(^|[\s“‘])(a|an|the) /gi, '$1$2\u00a0').replace(/(\S) “/g, '$1\u00a0“');
}
