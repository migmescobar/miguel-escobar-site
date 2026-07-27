// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import pruneAssets from './integrations/prune-assets.mjs';

// https://astro.build/config
export default defineConfig({
  // Served at the domain root (no `base`). Drives canonical URLs + sitemap.
  site: 'https://www.miguel-escobar.com',
  trailingSlash: 'ignore',
  build: {
    // /editorial-work/ -> editorial-work/index.html (clean directory URLs)
    format: 'directory',
  },
  integrations: [
    sitemap({
      // Exclude the 404 and the generated OG image endpoints.
      filter: (page) => !page.includes('/404') && !page.includes('/og/'),
    }),
    pruneAssets(),
  ],
  image: {
    // Sharp is Astro's default image service; generates AVIF/WebP + fallbacks.
    responsiveStyles: true,
  },
  vite: {
    // Native / font libs used by the per-post OG endpoint — don't bundle them.
    ssr: { external: ['@resvg/resvg-js', 'fontkit'] },
  },
});
