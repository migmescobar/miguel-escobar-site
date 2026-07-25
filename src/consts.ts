// ─────────────────────────────────────────────────────────────────────────────
// Site-wide settings. If you're not a developer, these are the only values you'll
// normally need to change. Each one is explained in the README.
// ─────────────────────────────────────────────────────────────────────────────

/** Canonical production origin. Must match `site` in astro.config.mjs. */
export const SITE_URL = 'https://www.miguel-escobar.com';

export const SITE_TITLE = 'Miguel Escobar';
export const SITE_DESCRIPTION =
  'Miguel Escobar is an experienced communications professional with an editorial background focused in tech and culture. He is based in Singapore, but born and raised in Metro Manila.';

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

// ── Contact form ────────────────────────────────────────────────────────────
// 1. Create a free form at https://formspree.io (send confirmations to the email
//    above). 2. Paste the endpoint it gives you (looks like the example below).
// Until you do, the form falls back to opening the visitor's email app.
export const FORMSPREE_ENDPOINT = 'https://formspree.io/f/YOUR_FORM_ID';

// ── Analytics ───────────────────────────────────────────────────────────────
// Create a free site at https://www.goatcounter.com and put your code here
// (the part before ".goatcounter.com"). Leave as-is to disable analytics.
export const GOATCOUNTER_CODE = 'YOUR_GOATCOUNTER_CODE';

/** True once the Formspree endpoint has been filled in. */
export const FORMSPREE_READY = !FORMSPREE_ENDPOINT.includes('YOUR_FORM_ID');
/** True once the GoatCounter code has been filled in. */
export const GOATCOUNTER_READY = GOATCOUNTER_CODE !== 'YOUR_GOATCOUNTER_CODE';

/** Primary navigation (shared header). */
export const NAV_LINKS = [
  { href: '/editorial-work/', label: 'Editorial' },
  { href: '/advertising-work/', label: 'Advertising' },
  { href: '/thoughts/', label: 'Thoughts' },
  // Contact section lives in the footer of every page, so this is a same-page anchor.
  { href: '#contact', label: 'Contact' },
];
