// ─────────────────────────────────────────────────────────────────────────────
// Site-wide settings. If you're not a developer, these are the only values you'll
// normally need to change. Each one is explained in the README.
// ─────────────────────────────────────────────────────────────────────────────

/** Canonical production origin. Must match `site` in astro.config.mjs. */
export const SITE_URL = 'https://www.miguel-escobar.com';

export const SITE_TITLE = 'Miguel Escobar';
export const SITE_DESCRIPTION =
  'Miguel Escobar is a communications and editorial professional in Singapore, working across content governance, online safety, and brand storytelling in APAC markets.';

/** Contact + footer details (used on every page). */
export const CONTACT = {
  email: 'migmescobar@gmail.com',
  // Shown in the footer (rendered with non-breaking spaces so it never wraps mid-digits).
  phoneDisplay: '+65 9851 7897',
  phoneHref: 'tel:+6598517897',
  linkedin: 'https://www.linkedin.com/in/miguel-escobar-6u56u5',
  /** CV lives in /public. Replace the file there to update the download. */
  cv: '/MiguelEscobar_2026_CV_Resume.pdf',
};

// ── Analytics ───────────────────────────────────────────────────────────────
// Create a free site at https://www.goatcounter.com and put your code here
// (the part before ".goatcounter.com"). Leave as-is to disable analytics.
export const GOATCOUNTER_CODE = 'YOUR_GOATCOUNTER_CODE';

/** True once the GoatCounter code has been filled in. */
export const GOATCOUNTER_READY = GOATCOUNTER_CODE !== 'YOUR_GOATCOUNTER_CODE';

/** Primary navigation (shared header). */
export const NAV_LINKS = [
  { href: '/about/', label: 'About' },
  { href: '/work/', label: 'Work' },
  { href: '/thoughts/', label: 'Thoughts' },
];
