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
5. [Turn on analytics](#5-turn-on-analytics)
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
| `title` | The post's own headline — shown as the H1 on the post page, the browser tab title, and in social-share previews. Also what's used as the clickable sentence on the Thoughts list, unless you set `listTitle` (below). Wrap a word in `*asterisks*` to italicise it (e.g. a movie or book title) — that works in `title` and `listTitle`, but nowhere else in the front matter. |
| `listTitle` | *Optional.* A different headline just for the Thoughts list, if you want it to read differently there than on the post itself (like a magazine's contents-page line vs. the article's own head). Leave it out and `title` is used everywhere. |
| `pubDate` | The date, as `YYYY-MM-DD`. Posts are listed newest first by this date. |
| `description` | A short summary. Shown as the subtitle on the post and in link previews. |
| `draft` | `true` = hidden from the site (a private work-in-progress). `false` = live. |

**Drafts:** set `draft: true` while you're still writing. A draft never appears in the Thoughts
list, never gets its own web page, and is invisible to Google. When it's ready, change it to
`draft: false`.

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

**Page wording** lives in the matching files under `src/pages/` — `index.astro` (Home),
`work.astro` (Work), `thoughts/index.astro` (the Thoughts list) and `404.astro`. The text is plain
English inside the file (Home's and Work's words sit in lists near the top); edit between the
quotes or tags. If in doubt, ask a developer or Claude.

### Swapping in your real images

Every image on the site lives in `src/assets/images/`. The file names say where each one shows:

| File | Where it shows |
|---|---|
| `home-*.jpg`, `osc-phone-57.jpg`, `ph-politics-uson.jpg`, `ads-nba.jpg` | the cards on the Home rail (cropped tall, about 5:7) |
| `editorial-magazines.webp` | Home, beside "My editorial background" (a cut-out with a transparent background) |
| `home-age-checks.jpg`, `home-whitewash.jpg`, `home-pulpit.jpg`, `osc-phone-43.jpg` | Work → Highlights (4:3) |
| `ads-*.jpg` | Work → More Advertising Work (4:3) |
| `editorial-*.jpg`, `ph-politics-uson.jpg`, `work-*.jpg` | Work → More Editorial Work (4:3) |

The highlights reel on Home is a video in `public/media/` (a 4:5 cut for desktops, a vertical cut
for phones, each with a poster image). Replace those files keeping the same names.

**You do _not_ need to optimise images yourself.** The site does it at build time — it generates
modern AVIF/WebP versions at several sizes, lazy-loads them, and sets exact dimensions so nothing
jumps around. Just give it a reasonable source file: JPG, about **1200–1600 px on the long edge**,
roughly the right shape (images are cropped to fill their frame).

**To replace one image:** put the new file in `src/assets/images/`, change the matching `import`
line near the top of `src/pages/index.astro` or `src/pages/work.astro` to point at it, and update
its `alt` text (a short description of the picture, for screen readers). Or send the image to
Claude and say which slot it's for.

---

## 5. Turn on analytics

Optional and free. Until you set it up, analytics simply stay off.

**Analytics (GoatCounter — privacy-friendly, no cookie banner needed).**
1. Sign up at <https://www.goatcounter.com> and pick a site code (e.g. `miguelescobar`).
2. Open `src/consts.ts`, find `GOATCOUNTER_CODE`, and put your code there. Save and publish.

There is no contact form — the footer carries your email, phone, LinkedIn and CV as plain links,
which is the whole contact surface of the site.

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
    index.astro              Home (/) — one long scroll: the name, Work, About, Editorial/Branded, Policy
    work.astro               /work/ — Highlights, More Advertising Work, More Editorial Work
    thoughts/
      index.astro            Thoughts list (/thoughts/)
      [...slug].astro        The template every post uses
    404.astro                "Page not found"
  content/thoughts/          YOUR POSTS live here (one .md file each)
  components/                Shared pieces: Nav, Menu, Footer ("Let’s talk"), Frame (images), Typed
  layouts/                   The page shell
  consts.ts                  ← contact details, site description, GoatCounter setting
  styles/global.css          Colours, the typeface, text styles shared by every page
  styles/home.css            Home's layout and all of its scroll motion
  assets/images/             Site images (optimised automatically at build)
  assets/fonts/              Self-hosted Neue Montreal woff2 (licence in /licenses)
public/                      Files served as-is: CV, reel videos, favicon, OG image, robots.txt
redesign-2026/               The approved 2026 design (Claude Design boards) the site is built from
```

The old addresses `/about/`, `/editorial-work/` and `/advertising-work/` redirect to Home and to
the matching sections of Work.

---

## 9. For developers

- **Stack:** Astro 5 (static output, `output: 'static'`), zero client framework. Small vanilla
  scripts only (see Motion). `@astrojs/sitemap` for the sitemap.
- **Design source:** `redesign-2026/` — the approved boards (`boards/*.dc.html`, desktop at
  1440px and phone at 390px) and the generator that wrote them (`source/gen_v47.py`, whose comments
  record why each value is what it is). Phone values apply below 900px, desktop values from 900px;
  desktop display type and margins scale with the viewport below 1440 and stop there, and content
  never runs wider than 1600px. Light theme only.
- **Fonts:** one face at one weight — **PP Neue Montreal** Regular (plus its italic for emphasis in
  posts), self-hosted, `font-display: swap`, the roman preloaded. Pangram Pangram licence in
  `/licenses`. The retail OTFs carry Cyrillic/Greek this site never renders, so `assets:fonts`
  subsets them (~83KB to ~26KB a face).
- **Images:** `astro:assets` `<Picture>` via `src/components/Frame.astro` → responsive AVIF/WebP
  with a JPEG fallback (PNG for cut-outs) + `srcset`, explicit dimensions, lazy below the fold.
- **Motion:** all CSS — scroll-driven animations (`animation-timeline: scroll()` / `view()`) for
  Home's reveals, typed headlines, the nav's colour changes and name, and the Policy stage; the
  boards' pixel ranges are re-expressed as fractions of the screen height (`svh`). Every animation
  has a still end state under `prefers-reduced-motion` and in browsers without scroll timelines.
  Small vanilla scripts only: the menu, the Home rail's buttons, and the reel (plays only while on
  screen, never with reduced motion, pause button).
- **SEO:** per-page title/description, Open Graph + Twitter tags, canonical URLs on
  `www.miguel-escobar.com`, JSON-LD `Person` on the home page, `robots.txt`, generated sitemap,
  and a design-matched OG image (`public/og-image.png`).
- **Config knobs:** `src/consts.ts` (contact info, `GOATCOUNTER_CODE`).
- **Build hook:** `integrations/prune-assets.mjs` deletes the untransformed original images
  Astro emits on import but never references, so `dist/` stays lean.
- **Checks:** `npm run build` then `npm run validate:html` (html-validate). Accessibility was
  verified with axe-core on the previous design; re-run it after big changes.

### One-off asset scripts (already run; outputs are committed)
These regenerate the derived assets. They need the optional tools (`@resvg/resvg-js`, `fontkit`,
`wawoff2`, and `fonttools` on PATH for `assets:fonts`). You normally never need these.

```bash
npm run assets:og            # public/og-image.png (1200×630: the Home hero — statement, name, cyan glow)
npm run assets:icons         # favicon.svg/.png + apple-touch-icon.png: a circle in the glow's cyan (#1AB0E7)
npm run assets:fonts         # PP OTFs → subsetted, self-hosted woff2 (needs `pip install fonttools`)
```

### Note on `npm audit`
`npm audit` may report advisories in Astro/sharp. They concern server-side rendering and
processing of *untrusted* images at runtime. This site is **fully static** (no server) and only
processes Miguel's own images **at build time**, so they don't apply to what's deployed. Update
Astro when convenient (`npm install astro@latest`) to clear them.
