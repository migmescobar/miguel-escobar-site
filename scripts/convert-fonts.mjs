// One-off: turn the site's licensed OTFs (Pangram Pangram, free personal-use —
// EULAs in /licenses) into subsetted woff2 for the web. Sources live in
// scripts/fonts/ so this is reproducible from a clean checkout.
// Run: npm run assets:fonts   (needs fonttools on PATH: `pip install fonttools`)
//
// Two steps per face: pyftsubset trims the glyph set, then wawoff2 compresses.
// The retail OTFs ship huge Cyrillic/Greek coverage this site never renders —
// subsetting takes Neue Montreal from ~83KB to ~26KB. `--layout-features='*'`
// keeps kerning and ligatures intact; don't narrow that flag.
import { compress } from 'wawoff2';
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';

const SRC = 'scripts/fonts';
const OUT = 'src/assets/fonts';

// Latin + the punctuation the site actually uses: curly quotes, en/em dashes,
// the → on the "More …" cards, é in "exposé", and ©.
const UNICODES = [
  'U+0000-00FF', 'U+0131', 'U+0152-0153', 'U+02BB-02BC', 'U+02C6', 'U+02DA',
  'U+02DC', 'U+0304', 'U+0308', 'U+0329', 'U+2000-206F', 'U+2074', 'U+20AC',
  'U+2122', 'U+2190-2193', 'U+2197', 'U+2212', 'U+2215', 'U+FEFF', 'U+FFFD',
].join(',');

// Only the faces the site actually renders — see README "For developers".
// Neue Montreal carries the whole site; there is no display serif.
const jobs = [
  // Semibold maps to 500 and is used only for the current item in the mobile nav.
  ['PPNeueMontreal-Regular.otf', 'neue-montreal-400.woff2'],
  ['PPNeueMontreal-Italic.otf', 'neue-montreal-400-italic.woff2'],
  ['PPNeueMontreal-Semibold.otf', 'neue-montreal-500.woff2'],
];

const tmp = mkdtempSync(path.join(tmpdir(), 'fontsubset-'));
try {
  for (const [inp, out] of jobs) {
    const subset = path.join(tmp, inp);
    execFileSync('pyftsubset', [
      `${SRC}/${inp}`,
      `--unicodes=${UNICODES}`,
      "--layout-features=*",
      `--output-file=${subset}`,
    ]);
    const woff2 = await compress(readFileSync(subset));
    writeFileSync(`${OUT}/${out}`, woff2);
    const before = readFileSync(`${SRC}/${inp}`).length;
    console.log(
      `  ${inp} -> ${out} (${(woff2.length / 1024).toFixed(1)} KB, from ${(before / 1024).toFixed(0)} KB otf)`
    );
  }
} finally {
  rmSync(tmp, { recursive: true, force: true });
}
console.log('done');
