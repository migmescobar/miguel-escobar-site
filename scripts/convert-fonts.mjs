// One-off: convert the Editorial New OTFs (Pangram Pangram, free personal-use) to
// woff2 for the site. Run: node scripts/convert-fonts.mjs
import { compress } from 'wawoff2';
import { readFileSync, writeFileSync } from 'node:fs';
const SRC = '/Users/mig/Downloads/PPEditorialNew-Free for personal use';
const OUT = 'src/assets/fonts';
const jobs = [
  ['PPEditorialNew-Regular.otf', 'editorial-new-400.woff2'],
  ['PPEditorialNew-Italic.otf', 'editorial-new-400-italic.woff2'],
];
for (const [inp, out] of jobs) {
  const woff2 = await compress(readFileSync(`${SRC}/${inp}`));
  writeFileSync(`${OUT}/${out}`, woff2);
  console.log(`  ${inp} -> ${out} (${(woff2.length / 1024).toFixed(1)} KB)`);
}
console.log('done');
