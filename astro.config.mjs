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
      // 404 is not a real content page
      filter: (page) => !page.includes('/404'),
    }),
    pruneAssets(),
  ],
  image: {
    // Sharp is Astro's default image service; generates AVIF/WebP + fallbacks.
    responsiveStyles: true,
  },
});
