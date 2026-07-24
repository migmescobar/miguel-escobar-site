// Small Astro integration: after the build, delete raster files in dist/_astro
// that no built HTML/CSS/JS/XML actually references. Astro emits the untransformed
// original of every imported image even when only optimized <Picture> variants are
// used; this removes that dead weight. Conservative: only touches _astro image files
// that appear in ZERO output files.
import { readdirSync, readFileSync, statSync, unlinkSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export default function pruneAssets() {
  return {
    name: 'prune-unused-images',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        const root = fileURLToPath(dir);

        const walk = (d, out = []) => {
          for (const e of readdirSync(d, { withFileTypes: true })) {
            const p = path.join(d, e.name);
            if (e.isDirectory()) walk(p, out);
            else out.push(p);
          }
          return out;
        };

        const files = walk(root);
        const haystack = files
          .filter((f) => /\.(html|css|js|xml|json)$/.test(f))
          .map((f) => readFileSync(f, 'utf8'))
          .join('\n');

        let removed = 0;
        let bytes = 0;
        for (const f of files) {
          if (!/_astro[\\/].+\.(png|jpe?g|avif|webp)$/.test(f)) continue;
          const base = path.basename(f);
          if (!haystack.includes(base)) {
            bytes += statSync(f).size;
            unlinkSync(f);
            removed++;
          }
        }
        if (removed > 0) {
          logger.info(`pruned ${removed} unreferenced image(s), ${(bytes / 1048576).toFixed(1)} MB`);
        }
      },
    },
  };
}
