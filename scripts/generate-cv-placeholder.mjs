// Write a minimal but valid placeholder CV PDF so the "Download my CV" link works
// before the real file is added. Replace public/MiguelEscobar_2026_CV_Resume.pdf
// with the real CV. Run: node scripts/generate-cv-placeholder.mjs
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const root = path.dirname(fileURLToPath(import.meta.url)) + '/..';

const text =
  'BT /F1 22 Tf 72 700 Td (Miguel Escobar) Tj ' +
  '/F1 12 Tf 0 -32 Td (CV placeholder - replace this file with the real CV.) Tj ' +
  '0 -18 Td (File: public/MiguelEscobar_2026_CV_Resume.pdf) Tj ET';

const objects = [
  '<</Type/Catalog/Pages 2 0 R>>',
  '<</Type/Pages/Kids[3 0 R]/Count 1>>',
  '<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Resources<</Font<</F1 4 0 R>>>>/Contents 5 0 R>>',
  '<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>',
  `<</Length ${text.length}>>\nstream\n${text}\nendstream`,
];

let pdf = '%PDF-1.4\n';
const offsets = [];
objects.forEach((body, i) => {
  offsets.push(pdf.length);
  pdf += `${i + 1} 0 obj\n${body}\nendobj\n`;
});
const xrefStart = pdf.length;
pdf += `xref\n0 ${objects.length + 1}\n0000000000 65535 f \n`;
offsets.forEach((o) => (pdf += String(o).padStart(10, '0') + ' 00000 n \n'));
pdf += `trailer\n<</Size ${objects.length + 1}/Root 1 0 R>>\nstartxref\n${xrefStart}\n%%EOF`;

writeFileSync(path.join(root, 'public/MiguelEscobar_2026_CV_Resume.pdf'), pdf, 'latin1');
console.log('Wrote public/MiguelEscobar_2026_CV_Resume.pdf (placeholder)');
