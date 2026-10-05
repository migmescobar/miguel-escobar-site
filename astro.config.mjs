// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import pruneAssets from './integrations/prune-assets.mjs';
import rehypeKeepCompounds from './integrations/rehype-keep-compounds.mjs';

// https://astro.build/config
export default defineConfig({
  // Served at the domain root (no `base`). Drives canonical URLs + sitemap.
  site: 'https://www.miguel-escobar.com',
  trailingSlash: 'ignore',
  build: {
    // /work/ -> work/index.html (clean directory URLs)
    format: 'directory',
  },
  // The 2026 redesign folded About into Home, and Editorial Work and Advertising
  // Work into one Work page. The old addresses send people to the right place.
  redirects: {
    '/about': '/#about',
    '/editorial-work': '/work/#editorial',
    '/advertising-work': '/work/#advertising',
  },
  markdown: {
    rehypePlugins: [rehypeKeepCompounds],
  },
  integrations: [
    sitemap({
      // Exclude the 404, the generated OG image endpoints, and the redirects.
      filter: (page) =>
        !page.includes('/404') &&
        !page.includes('/og/') &&
        !/\/(about|editorial-work|advertising-work)\/?$/.test(page),
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
