// Rehype plugin for Thoughts posts: a hyphenated compound ("real-world") never
// splits across lines, nor does a spaced em dash leave the word before it — the
// same rule the redesign's generator applies to every paragraph on the site
// (keep_compounds in redesign-2026/source/gen_v47.py).
const COMPOUND = /([^\s]+-[^\s]+)/g;
const SKIP = new Set(['code', 'pre', 'script', 'style']);

function transform(node) {
  if (!node.children) return;
  const out = [];
  for (const child of node.children) {
    if (child.type === 'text') {
      const value = child.value.replace(/ — /g, ' — ');
      const parts = value.split(COMPOUND);
      parts.forEach((part, i) => {
        if (!part) return;
        if (i % 2 === 1) {
          out.push({
            type: 'element',
            tagName: 'span',
            properties: { className: ['nw'] },
            children: [{ type: 'text', value: part }],
          });
        } else {
          out.push({ type: 'text', value: part });
        }
      });
    } else {
      if (child.type === 'element' && !SKIP.has(child.tagName)) transform(child);
      out.push(child);
    }
  }
  node.children = out;
}

export default function rehypeKeepCompounds() {
  return (tree) => transform(tree);
}
