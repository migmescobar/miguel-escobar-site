# miguel-escobar.com

The personal portfolio of Miguel Escobar — Singapore-based communications professional.
Built with [Astro](https://astro.build) as a fully static site (fast, no server, no
database) and deployed free on GitHub Pages with the custom domain **www.miguel-escobar.com**.

This README is written for a **non-developer**. You can run and update the whole site with a
few copy-paste commands. If something here is unclear, hand this file to any developer (or to
Claude) and they'll know exactly what to do.

---

## Table of contents

1. [What you need once](#1-what-you-need-once)
2. [Run it on your Mac (preview)](#2-run-it-on-your-mac-preview)
3. [Add or edit a Thoughts post](#3-add-or-edit-a-thoughts-post) ← the main thing you'll do
4. [Change your details, links, and the CV](#4-change-your-details-links-and-the-cv)
5. [Turn on the contact form and analytics](#5-turn-on-the-contact-form-and-analytics)
6. [Publish changes (it deploys itself)](#6-publish-changes-it-deploys-itself)
7. [First-time setup: GitHub + domain + DNS](#7-first-time-setup-github--domain--dns)
8. [How the site is organised](#8-how-the-site-is-organised)
9. [For developers](#9-for-developers)

---

## 1. What you need once

- A Mac (these notes assume macOS).
- **Node.js 20 or newer.** Check by opening the **Terminal** app and typing `node --version`.
  If it's missing or old, install the "LTS" version from <https://nodejs.org>.
- The first time, in Terminal, go to this folder and install the building blocks:

  ```bash
  cd path/to/this/folder
  npm install
  ```

  (Drag the folder onto the Terminal window to paste its path.)

---

## 2. Run it on your Mac (preview)

To see the site locally before publishing:

```bash
npm run dev
```

Then open the link it prints (usually <http://localhost:4321>). Edits you make to files are
reflected in the browser automatically. Press `Ctrl + C` in Terminal to stop.

To preview the **exact** files that get published (optional):

```bash
npm run build     # creates the finished site in the dist/ folder
npm run preview   # serves that finished site
```

---

## 3. Add or edit a Thoughts post

Every post is **one plain-text file** in the folder `src/content/thoughts/`. To add a post,
create a new file there ending in `.md` — for example `my-first-post.md` — and start it with
this block (the part between the `---` lines is the "front matter"):

```markdown
---
title: The title of the post
pubDate: 2026-08-01
description: One or two sentences that appear as the post's subtitle and preview.
draft: false
---

Write the post here in Markdown. A blank line starts a new paragraph.

## A subheading

- a bullet
- another bullet

**bold**, *italic*, and [a link](https://example.com) all work.
```

Field-by-field:

| Field | What to put |
|---|---|
| `title` | The post title. It's also the clickable sentence on the Thoughts page — so a short, readable sentence works best (keep it under ~55 characters for tidy search-result titles). |
| `pubDate` | The date, as `YYYY-MM-DD`. Posts are listed newest first by this date. |
| `description` | A short summary. Shown as the subtitle on the post and in link previews. |
| `draft` | `true` = hidden from the site (a private work-in-progress). `false` = live. |

**Drafts:** set `draft: true` while you're still writing. A draft never appears in the Thoughts
list, never gets its own web page, and is invisible to Google. When it's ready, change it to
`draft: false`. (The three starter posts in that folder are lorem-ipsum placeholders — edit them
in place or delete them and add your own.)

**Optional header image for a post.** Put an image file in `src/assets/images/`, then add
these two lines to the post's front matter:

```markdown
heroImage: ../../assets/images/your-photo.jpg
heroAlt: A short description of the photo, for screen readers.
```

The image is automatically resized and optimised — just drop in a normal-sized photo.

That's the whole workflow. Save the file, then [publish](#6-publish-changes-it-deploys-itself).
(You can also just ask Claude to "add a post" and paste your text — it will create the file.)

---

## 4. Change your details, links, and the CV

**Contact details, social links, site description** all live in one file:
**`src/consts.ts`**. Open it and edit the values in quotes — email, phone, LinkedIn, etc. It's
commented so you can see what each one is.

**Your CV.** Your CV lives at `public/MiguelEscobar_2026_CV_Resume.pdf`. To update it later,
replace that file with a new PDF, keeping the **same file name** — the "Download my CV" link
then just works.

**Page wording** (home, editorial, advertising) lives in the matching files under
`src/pages/` (e.g. `src/pages/index.astro` is the home page). The text is plain English inside
the file; edit between the tags. If in doubt, ask a developer or Claude.

### Swapping in your real images

The home page and the Editorial Work page use your real art. The Advertising Work page still uses
**on-brand placeholders** (paper-coloured cards labelled with the slot and "PLACEHOLDER IMAGE").
All images live in `src/assets/images/`, and the file names tell you which slot each one is:

| File | Where it shows |
|---|---|
| `home_*.png` (6) | the six "Some work" cards on the home page (real art) |
| `editorial_*.png` (4) | the four rows on the Editorial Work page (real art) |
| `ph_ads_*.png` (4) | the four rows on the Advertising Work page (placeholder) |

**You do _not_ need to optimise images yourself.** The site does it for you at build time — it
generates modern AVIF/WebP versions at several sizes, lazy-loads them, and sets exact dimensions
so nothing jumps around. Just give it a reasonable source file:

- **Format:** JPG or PNG.
- **Size:** roughly **1600 px on the long edge** is plenty; keep it under a few MB. (No need to
  upload 40-megapixel camera originals — they only slow the build.)
- **Shape (important):** home cards are **3:4 portrait**; Editorial/Advertising rows are **4:3
  landscape**. Images are cropped to fill, so crop to roughly the right shape or the edges get
  trimmed.

**To replace one image:**
1. Put your photo in `src/assets/images/` (e.g. `my-photo.jpg`).
2. Open the page it belongs to — `src/pages/index.astro` (home), `editorial-work.astro`, or
   `advertising-work.astro`. Near the top you'll see lines like
   `import whitewash from '../assets/images/home_whitewash.png';` — change that path to your
   file, e.g. `'../assets/images/my-photo.jpg'`.
3. Update the matching `alt="…"` text to describe the real photo (good for accessibility + SEO).
4. Save and [publish](#6-publish-changes-it-deploys-itself).

**Easiest of all:** send the images to Claude, say which slot each one is for, and it'll drop
them in, write the alt text, and publish.

---

## 5. Turn on the contact form and analytics

Both are optional and both are free. Until you set them up, the site still works: the contact
form falls back to opening the visitor's email app, and analytics simply stay off.

**Contact form (Formspree).**
1. Sign up at <https://formspree.io> and create a new form (send submissions to your email).
2. It gives you an endpoint that looks like `https://formspree.io/f/abcdwxyz`.
3. Open `src/consts.ts`, find `FORMSPREE_ENDPOINT`, and paste your endpoint in place of the
   placeholder. Save, then [publish](#6-publish-changes-it-deploys-itself).

**Analytics (GoatCounter — privacy-friendly, no cookie banner needed).**
1. Sign up at <https://www.goatcounter.com> and pick a site code (e.g. `miguelescobar`).
2. Open `src/consts.ts`, find `GOATCOUNTER_CODE`, and put your code there. Save and publish.
   (Analytics only load on the live site, never during local preview.)

---

## 6. Publish changes (it deploys itself)

Once the site is on GitHub (see the next section), **publishing is automatic**: every time you
save your changes to the `main` branch on GitHub, a robot rebuilds the site and puts it live in
a couple of minutes. You can watch it happen under the **Actions** tab of your GitHub repo.

If you're editing on your Mac, the sequence is:

```bash
git add -A
git commit -m "Add a new post"   # describe what you changed
git push
```

(Or use the GitHub Desktop app if you prefer buttons to commands.)

---

## 7. First-time setup: GitHub + domain + DNS

This is a **one-time** setup.

> ✅ **Already done for you:** the repo **`migmescobar/miguel-escobar-site`** is created, `main`
> is pushed, GitHub Pages is set to build from **GitHub Actions**, and the first deploy
> succeeded. Steps **a** and **b** are for reference; what's left is the domain + DNS (steps
> **c–f**), which need your Squarespace login.

### a. Put the code on GitHub _(done)_
The repo lives at <https://github.com/migmescobar/miguel-escobar-site>. Future changes publish
automatically whenever you `git push` (see §6).

### b. Turn on GitHub Pages _(done)_
Source is set to **GitHub Actions** (repo Settings → Pages), using `.github/workflows/deploy.yml`.

### c. Verify your domain (prevents anyone else claiming it)
1. GitHub: click your avatar → **Settings → Pages** (your account-level page settings).
2. Under **Verified domains**, add `miguel-escobar.com`, and add the **TXT record** GitHub
   shows you at your registrar (Squarespace) — see the DNS steps below for where.

### d. Point the domain at GitHub (custom domain)
1. Back in the **repo's** Settings → Pages, set **Custom domain** to `www.miguel-escobar.com`
   and save. (This, not the `public/CNAME` file, is what makes the domain stick — the file is
   just a harmless backup.)
2. Leave **Enforce HTTPS** for now; tick it once the certificate has issued (step f).

### e. Enter DNS records at Squarespace
In Squarespace: **Settings → Domains → miguel-escobar.com → DNS / DNS Settings** (labels vary
slightly; look for "DNS settings" or "Custom records"). Add these records:

**1) One CNAME so `www` points at GitHub:**

| Type | Host / Name | Value / Data |
|---|---|---|
| CNAME | `www` | `migmescobar.github.io` |

**2) Four A records so the bare domain `miguel-escobar.com` reaches GitHub:**

| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |

**3) Four AAAA records (IPv6) for the same bare domain:**

| Type | Host | Value |
|---|---|---|
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |

(If Squarespace uses "Host" you can leave blank or `@` for the bare domain. Also add the
**TXT** verification record from step c here.) With the A/AAAA records in place, the bare
`miguel-escobar.com` will redirect to `www.miguel-escobar.com` automatically.

### f. Finish
- DNS changes can take anywhere from a few minutes to a day to take effect.
- Once GitHub shows the domain as configured and the padlock/certificate is ready, go back to
  **repo Settings → Pages** and tick **Enforce HTTPS**.
- Your Squarespace **domain registration stays with Squarespace** — you're only changing where
  it points. You can do this any time before the old Squarespace site expires.

---

## 8. How the site is organised

```
src/
  pages/                     Each file = one web page
    index.astro              Home (/)
    editorial-work.astro     /editorial-work/
    advertising-work.astro   /advertising-work/
    thoughts/
      index.astro            Thoughts list (/thoughts/)
      [...slug].astro        The template every post uses
    404.astro                "Page not found"
  content/thoughts/          YOUR POSTS live here (one .md file each)
  components/                Shared pieces (header, footer/contact, image)
  layouts/                   Page shells
  consts.ts                  ← contact details, links, Formspree & GoatCounter settings
  styles/global.css          Colours, fonts, and shared styles
  assets/images/             Site images (currently on-brand placeholders; optimised automatically)
  assets/fonts/              Self-hosted Editorial New woff2 (license in /licenses)
public/                      Files served as-is: CV, favicon, OG image, robots.txt
```

---

## 9. For developers

- **Stack:** Astro 5 (static output, `output: 'static'`), zero client framework. Small vanilla
  scripts only (mobile menu, contact form, scroll-reveal). `@astrojs/sitemap` for the sitemap.
- **Fonts:** Geist + Geist Mono (self-hosted via `@fontsource`) for body/UI, plus **PP Editorial
  New** (Pangram Pangram, self-hosted woff2, Regular 400, exposed as `--font-serif`) for the
  display headings. All `font-display: swap`. The free personal-use license is committed in
  `/licenses`.
- **Images:** `astro:assets` `<Picture>` → responsive AVIF/WebP with a JPEG fallback + `srcset`,
  explicit dimensions (no layout shift), lazy below the fold. See `src/components/WorkImage.astro`.
  The home cards and the Editorial page use real art; the Advertising list page still uses
  placeholders (see §4 → "Swapping in your real images").
- **Motion:** scroll-reveal is opt-in via an inline head snippet + IntersectionObserver, fully
  disabled under `prefers-reduced-motion`, with a guaranteed failsafe so content can't get stuck
  hidden.
- **SEO:** per-page title/description, Open Graph + Twitter tags, canonical URLs on
  `www.miguel-escobar.com`, JSON-LD `Person` on the home page, `robots.txt`, generated sitemap,
  and a design-matched OG image (`public/og-image.png`).
- **Config knobs:** `src/consts.ts` (contact info, `FORMSPREE_ENDPOINT`, `GOATCOUNTER_CODE`).
- **Build hook:** `integrations/prune-assets.mjs` deletes the untransformed original images
  Astro emits on import but never references, so `dist/` stays lean.
- **Checks:** `npm run build` then `npm run validate:html` (html-validate). Accessibility was
  verified with axe-core (0 violations) and the home page scores 99/100/100/100 on Lighthouse
  (perf / a11y / best-practices / SEO).

### One-off asset scripts (already run; outputs are committed)
These regenerate the derived assets. They need the optional tools (`@resvg/resvg-js`, `fontkit`,
`wawoff2`). You normally never need these.

```bash
npm run assets:placeholders  # the 4 on-brand placeholder images for the Advertising page
npm run assets:og            # public/og-image.png (1200×630, Editorial New masthead + brand dot)
npm run assets:icons         # public/apple-touch-icon.png (derived from favicon.png)
npm run assets:fonts         # PP Editorial New OTF → self-hosted woff2 (src/assets/fonts)
```

### Note on `npm audit`
`npm audit` may report advisories in Astro/sharp. They concern server-side rendering and
processing of *untrusted* images at runtime. This site is **fully static** (no server) and only
processes Miguel's own images **at build time**, so they don't apply to what's deployed. Update
Astro when convenient (`npm install astro@latest`) to clear them.
