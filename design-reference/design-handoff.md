# Handoff: Miguel Escobar — Personal Portfolio Site

## Overview
A responsive, editorial-style personal portfolio for Miguel Escobar, a Singapore-based
communications professional. Seven pages: a **Home** landing page, two work-index pages
(**Editorial**, **Advertising**), a **Thoughts** blog index, and **four individual Thought
post** pages. Every page shares a common header (with a mobile hamburger menu) and a common
Contact + footer section. The aesthetic is quiet and typographic — warm off-white paper,
near-black ink, a single sans typeface (Geist) with a monospace (Geist Mono) for labels.

## About the Design Files
The files in this bundle are **design references created in HTML** — prototypes showing the
intended look, layout, and behavior. They are **not production code to copy directly**. They
use a small in-house template runtime (`support.js`, custom `<x-dc>` / `{{ }}` / `<sc-if>`
tags) and a drag-and-drop image placeholder web component (`image-slot.js`) that exist only
in the prototyping environment.

Your task is to **recreate these designs in the target codebase's existing environment**
(React, Vue, Svelte, SwiftUI, plain HTML/CSS, etc.), using its established patterns, routing,
and component libraries. If no codebase exists yet, pick the most appropriate framework
(a static site generator such as Astro/Eleventy, or Next.js, suits this content well) and
implement there. Ignore the `<x-dc>`/`support.js` machinery — reproduce the **markup,
styling, and interactions** described below.

## Fidelity
**High-fidelity (hifi).** Final colors, typography, spacing, and interactions. Recreate the
UI pixel-perfectly using the target codebase's conventions. All values in this document are
authoritative.

---

## Global System

### Design Tokens

**Colors**
| Token | Value | Use |
|---|---|---|
| Paper (background) | `#EAE7E1` | Page background |
| Ink (foreground) | `#141414` | Text, rules, buttons |
| Ink 90% | `rgba(20,20,20,.9)` | Body text on post pages |
| Ink 85% | `rgba(20,20,20,.85)` | Body text on work pages |
| Ink 80% | `rgba(20,20,20,.8)` | Secondary body |
| Ink 75% | `rgba(20,20,20,.75)` | Mobile nav inactive |
| Ink 70% | `rgba(20,20,20,.7)` | Post deck/subtitle |
| Ink 60% | `rgba(20,20,20,.6)` | Form field labels |
| Ink 55% | `rgba(20,20,20,.55)` | Footer, back-link, eyebrow |
| Ink 50% | `rgba(20,20,20,.5)` | Thoughts inline dates |
| Ink 40% | `rgba(20,20,20,.4)` | Link underline default, input underline |
| Ink 30% | `rgba(20,20,20,.3)` | Section divider rules, dormant headline links |
| Ink 20% | `rgba(20,20,20,.2)` | Footer top rule |
| Ink 15% | `rgba(20,20,20,.15)` | Mobile nav item dividers |
| Selection | bg `#141414`, text `#EAE7E1` | `::selection` |

**Typography**
- Body / headings: **Geist** (weights 400, 500, 600). Fallback: `Helvetica, Arial, sans-serif`.
- Labels / eyebrows / footer / form labels / dates: **Geist Mono** (weights 400, 500).
- Both loaded from Google Fonts.
- `-webkit-font-smoothing: antialiased` on body.

**Type scale (all headings weight 500 unless noted)**
| Role | size | letter-spacing | line-height |
|---|---|---|---|
| Home hero `h1` | `clamp(40px, 7.2vw, 104px)` | `-.035em` | `1.02` |
| Page title `h1` (work/Thoughts) | `clamp(42px, 6.4vw, 88px)` | `-.035em` | default |
| Post title `h1` | `clamp(34px, 5vw, 60px)` | `-.03em` | `1.08` |
| Contact `h2` "Let's talk" | `clamp(38px, 5vw, 68px)` | `-.03em` | default |
| "Some work" `h2` (Home) | `clamp(38px, 5.4vw, 72px)` | `-.03em` | default |
| Work-item `h2` | `clamp(24px, 2.6vw, 32px)` | `-.015em` | default |
| Thoughts index paragraph | `clamp(30px, 4vw, 48px)` | `-.02em` | `1.38` |
| Home card `h3` | `22px` | `-.01em` | `1.25` |
| Post deck (subtitle) | `22px` | — | `1.5` |
| Post body `p` | `19px` | — | `1.65` |
| Work body `p` | `16px` | — | `1.65` |
| Home intro `p` | `17px` | — | `1.65` |
| Card / contact body `p` | `15–16px` | — | `1.55–1.6` |
| Mono eyebrow / date | `12px` | `.06em` | — |
| Footer / form label mono | `11px` | `.06–.08em` | — |

**Spacing & layout**
- Content max-width: **1360px**, centered (`margin:0 auto`).
- Page horizontal padding: `clamp(20px, 5vw, 64px)` (used on `<main>` and the contact section).
- Header padding: `26px clamp(20px,5vw,64px)`.
- Section vertical rhythm uses `clamp()` throughout — see per-section values below.
- Dividers: `1px solid rgba(20,20,20,.3)` between sections; footer rule `1px solid rgba(20,20,20,.2)`.
- No border-radius anywhere (all corners square, including buttons and inputs).
- No shadows.

**Links (global)**
- Default: color `#141414`, `text-decoration-color: rgba(20,20,20,.4)`, `text-underline-offset:5px`, `text-decoration-thickness:1px`.
- Hover: `text-decoration-color:#141414`.

### Header / Navigation (identical on all pages)
- Layout: outer `<header>`; inner row is `display:flex; justify-content:space-between; align-items:center; gap:14px 28px`.
- Left: wordmark link "Miguel Escobar" → Home, `17px`, weight 400, `letter-spacing:-.01em`, no underline.
- Right (desktop, `.nav-desktop`): four links — **Editorial, Advertising, Thoughts, Contact** — `15px`, no underline, `gap: clamp(18px,3vw,40px)`.
  - Each link has `border-bottom:1px solid transparent; padding-bottom:2px`; on hover the border becomes `#141414`.
  - The link for the **current page** is shown active: `border-bottom:1px solid #141414` and `aria-current="page"` (Contact is never "current"). On Home, none are active.
- **Mobile hamburger** (`.nav-burger`, hidden ≥641px): a 30×30 button, `background:none;border:0`, containing three stacked bars (`height:1.5px; width:24px; background:#141414; gap:5px`). `aria-label="Toggle menu"`, `aria-expanded` bound to open state.
- **Mobile menu** (`.nav-mobile`, hidden by default): a vertical stack shown below the header row when open. Each item: `19px`, `padding:13px 0`, `border-top:1px solid rgba(20,20,20,.15)`. Active item weight 500 / full ink; others weight 400 / `rgba(20,20,20,.75)`. Tapping any item closes the menu.
- **Breakpoint:** at `max-width:640px`, `.nav-desktop` hides, `.nav-burger` shows, and the open `.nav-mobile` displays as a flex column.

### Contact + Footer section (identical on all pages, `id="contact"`)
- Section: `border-top:1px solid rgba(20,20,20,.3)`, padding `clamp(48px,7vw,88px) clamp(20px,5vw,64px) clamp(40px,5vw,64px)`.
- Inner row (max 1360, centered): `display:flex; flex-wrap:wrap; gap:40px 48px`.
- **Left column** (`flex:1 1 320px; min-width:260px`):
  - `h2` "Let's talk".
  - `p` (max-width 400): *"Hiring, briefing, or looking to connect? Reach out to me for anything."*
  - Link stack (`gap:12px`, `16px`): "Download my CV" (weight 500, `download` attr), "+65 9851 7897" (`tel:`), "migmescobar@gmail.com" (`mailto:`), "LinkedIn" (`https://www.linkedin.com/`, new tab).
- **Right column — form** (`flex:1 1 380px; max-width:560px`, toggleable via a `showForm` flag; `gap:22px`):
  - Three fields NAME / EMAIL / MESSAGE. Labels are Geist Mono `11px`, `letter-spacing:.08em`, `rgba(20,20,20,.6)`.
  - Inputs: no box — only a bottom border `1px solid rgba(20,20,20,.4)`, transparent bg, `padding:8px 0`, `17px`, square corners, no outline. On focus: border `#141414` + `box-shadow:0 1px 0 #141414`. Message is a 4-row textarea, `resize:vertical`.
  - Submit button: `padding:14px 28px`, bg `#141414`, text `#EAE7E1`, `1px solid #141414`, `15px`/weight 500, square, `align-self:flex-start`. Hover inverts to transparent bg + ink text. Focus: `outline:2px solid #141414; outline-offset:3px`.
  - On submit: build a `mailto:migmescobar@gmail.com` link with subject "Hello Miguel" and a body of the message plus "— {name} ({email})".
- **Footer bar**: top rule `1px solid rgba(20,20,20,.2)`, `padding-top:20px`, `margin-top: clamp(40px,6vw,72px)`. Single Geist Mono item `11px`, `letter-spacing:.06em`, `rgba(20,20,20,.55)`: "© 2026 MIGUEL ESCOBAR".

---

## Screens / Views

### 1. Home (`Home.dc.html`)
- **Hero section** (max 1360, padding `clamp(40px,8vh,96px) 0 clamp(48px,7vw,96px)`): single `h1` reading
  *"Strategic Communications. Content Governance. Editorial Operations. APAC&nbsp;Markets."*
  - Desktop: left-indented by `margin-left: min(12vw, 240px)`; `text-wrap:balance`.
  - **Responsive:** at `max-width:760px` the indent is removed (`margin-left:0`) and size drops to `clamp(30px, 8.5vw, 104px)` so long words don't clip on small phones.
- **Intro section** (max 1360, `display:flex; flex-wrap:wrap; gap:32px 48px`, padding-bottom `clamp(56px,9vw,120px)`):
  - **Rule column** (`flex:0 1 200px; min-width:120px; padding-top:14px`): a 1px ink horizontal line, `max-width:190px`.
  - **Text column** (`flex:1 1 380px; max-width:640px; 17px/1.65`): three paragraphs (`margin-bottom:1.4em`, last is weight 400). Copy:
    1. "A Singapore-based communications professional with a journalist's instincts. Intellectually curious, plugged into culture and tech, and — for better and worse — AI-pilled." *(Note: the live prototype's first paragraph currently reads "…terminally online and AI-pilled." — treat the two as interchangeable; confirm final wording with Miguel.)*
    2. "At Esquire Philippines, I covered culture, politics, and current affairs, writing, producing, and editing everything from daily articles to investigative features. Over 12+ years I've moved across editorial, content operations, and strategic communications, working with brands like the NBA, Trust Bank, Samsung, and Toyota across the Philippines and Singapore. I've managed high-volume content projects, enforced editorial standards across several publications, and built communications strategies and content governance frameworks for brands."
    3. "In all I do, I find purpose in telling stories that are honest, helpful, and human."
  - **Responsive:** at `max-width:760px` the rule column becomes full-width (`flex:1 1 100%`, `padding-top:4px`) and the rule loses its `max-width` cap, so the line spans the full body-text width instead of orphaning as a short stub above the wrapped text.
- **"Some work" section** (max 1360, padding `clamp(40px,6vw,72px) 0 clamp(64px,9vw,128px)`, preceded by a full-width 1px `.3` rule):
  - `h2` "Some work".
  - Card grid: `display:grid; grid-template-columns:repeat(auto-fill, minmax(min(280px,100%), 1fr)); gap: clamp(40px,4vw,56px) 40px`.
  - Six cards, each `display:flex; flex-direction:column; gap:16px`: a **3:4 portrait** image slot, an `h3` title link, and a 15px description. Cards, in order:
    1. **Age Checks Matter** → `#` — "A film and campaign for the IMDA, launching Age Assurance Measures — age checks on app stores — in Singapore."
    2. **Online Safety Commission Launch** → `#` — "Web copy, service articles, and explainer videos about online harms for the launch of Singapore's Online Safety Commission."
    3. **How to Whitewash a Dictator** → `#` — "An investigative feature on an invisible war for Philippine history, waged by Wikipedia editors on hotly contested pages."
    4. **A Pulpit for Pastors of Porn** → `#` — "An exposé that dug deep into a social media subculture of sexual predators in the Philippines, sparking a nationwide reckoning."
    5. **More Editorial Work →** → `Editorial Work` — "A selection of articles published with my byline, including for Esquire Philippines, Tatler Asia, and Smile Magazine."
    6. **More Advertising Work →** → `Advertising Work` — "A selection of ads and campaigns I've worked on, including for the NBA, Trust Bank, and Alcon."

### 2. Editorial Work (`Editorial Work.dc.html`)
- Page title section (max 1360, padding `clamp(36px,7vh,80px) 0 clamp(40px,5vw,64px)`): `h1` "Editorial Work".
- Four **work articles**, each: `border-top:1px solid rgba(20,20,20,.3)`, padding `clamp(32px,4vw,56px) 0` (last article's bottom padding is `clamp(56px,8vw,104px)`), `display:flex; flex-wrap:wrap-reverse; gap:32px 56px; align-items:center`.
  - **Text block** (`flex:1 1 340px; max-width:560px`): `h2` (`margin:10px 0 14px`) + one or two 16px paragraphs. Inline links use `#` placeholders.
  - **Image block** (`flex:1 1 380px; aspect-ratio:4/3; min-width:min(100%,320px)`): a landscape image slot.
  - `wrap-reverse` means that when the row wraps (narrow screens) the image appears **above** the text.
  - Items: **Politics in Esquire** (2 paragraphs; links: Salvador Panelo, Dick Gordon, Mocha Uson) · **Other Big Esquire Features** (links: big celebrity interviews, film reviews, fashion editorials) · **Tatler Asia's Most Influential** (link: I contributed) · **Smile Magazine Cover Story**. Full copy is in the source file.

### 3. Advertising Work (`Advertising Work.dc.html`)
- Same structure as Editorial. Title "Advertising Work". Four articles:
  **Trust Bank Singapore** (links: launch of its cashback card, a film) · **NBA Asia-Pacific Newsletters** · **Alcon Asia-Pacific Campaigns** · **GoTyme Bank Philippines** (links: campaign film, shorts). Full copy in source.

### 4. Thoughts index (`Thoughts.dc.html`)
- Title section: `h1` "Thoughts".
- **Continuous-paragraph index** (section: `border-top` rule, padding `clamp(32px,4vw,56px) 0 clamp(64px,10vw,140px)`): a single large paragraph (`clamp(30px,4vw,48px)`, weight 500, `line-height:1.38`, `text-wrap:pretty`) where **each post is one sentence rendered as a link**, preceded by a small inline monospace date.
  - Dormant link color `rgba(20,20,20,.3)`; on hover the whole sentence transitions (`.35s ease`) to `#141414`.
  - Inline date span: Geist Mono, `font-size:.3em`, weight 400, `letter-spacing:.1em`, `vertical-align:.62em`, `color:rgba(20,20,20,.5)`, `margin-right:.45em`, `white-space:nowrap`.
  - Entries (date → sentence → target):
    - **JUL 2026** — "Lorem ipsum dolor sit amet, consectetur adipiscing elit." → `Thought - Brand Editor`
    - **JUN 2026** — "Sed do eiusmod tempor incididunt ut labore et dolore." → `Thought - AI-Pilled Playbook`
    - **MAY 2026** — "Ut enim ad minim veniam, quis nostrud exercitation ullamco." → `Thought - Newsroom to Brand`
    - **APR 2026** — "Duis aute irure dolor in reprehenderit in voluptate velit." → `Thought - Writing for Trust`
  - Post titles/sentences are **placeholder Lorem Ipsum** pending final copy.

### 5–8. Thought posts (`Thought - *.dc.html`)
- Centered article column, `max-width:720px`.
- **Back link** (padding `clamp(28px,5vh,56px) 0 0`): Geist Mono `12px`, `letter-spacing:.06em`, `rgba(20,20,20,.55)`, "← ALL THOUGHTS" → `Thoughts`. Hover adds a bottom border.
- **Post header** (padding `clamp(28px,4vw,44px) 0 clamp(24px,3vw,36px)`):
  - **Eyebrow**: Geist Mono `12px`, `letter-spacing:.06em`, `rgba(20,20,20,.55)`, the **post date** — sample values in the prototypes: Newsroom "12 MAY 2026", Brand Editor "24 JULY 2026", AI-Pilled "3 JUNE 2026", Writing for Trust "18 APRIL 2026".
  - `h1` post title (`clamp(34px,5vw,60px)`, `margin-bottom:22px`, `text-wrap:balance`).
  - Deck `p` (`22px`, `line-height:1.5`, `rgba(20,20,20,.7)`).
- **Hero image**: `aspect-ratio:16/9; width:100%`, `margin-bottom: clamp(28px,4vw,44px)`.
- **Body** (`border-top:1px solid rgba(20,20,20,.3)`, `padding-top: clamp(28px,4vw,40px)`, `padding-bottom: clamp(48px,7vw,96px)`): four paragraphs, `19px`/`1.65`, `rgba(20,20,20,.9)`, `margin-bottom:1.3em`.
- Titles and body are **placeholder Lorem Ipsum** pending final copy.

---

## Interactions & Behavior
- **Mobile menu**: hamburger toggles an open/closed boolean; open shows the stacked nav; any nav item click closes it; `aria-expanded` reflects state. Pure client state, no routing dependency.
- **Contact form**: prevents default submit and opens the user's mail client via a composed `mailto:` (see Contact section). No network request.
- **Scroll reveal**: every element marked as a reveal target starts at `opacity:0; translateY(18px)` and animates to `opacity:1; translateY(0)` over `.8s cubic-bezier(.16,1,.3,1)` when it enters the viewport (IntersectionObserver, `threshold:0.1`, unobserve after firing). A 1.5s failsafe forces everything visible in case the observer never fires.
  - **Reduced motion:** if `prefers-reduced-motion: reduce`, the reveal is skipped entirely (content renders visible) and `scroll-behavior` is set to `auto`.
- **Headline links** (Thoughts index): color-only hover transition, `.35s ease`.
- **Nav / body links**: underline-color or bottom-border hover as described in tokens/header.
- **Smooth scrolling**: `html { scroll-behavior: smooth }` (Contact link is an in-page `#contact` anchor).

## Responsive Behavior (summary)
- **≤640px**: desktop nav → hamburger + stacked mobile menu.
- **≤760px** (Home only): hero loses left indent and shrinks its min size; intro rule column goes full-width so the divider matches body-text width.
- All sections use `flex-wrap`/`grid auto-fill` + `clamp()` padding, so they reflow fluidly with no other hard breakpoints. Work articles use `wrap-reverse` so the image leads above the text when stacked.

## State Management
- `menuOpen: boolean` — mobile menu visibility (toggle / close-on-navigate).
- `showForm: boolean` — whether the contact form column renders (defaults true; exposed as a config flag).
- `motion: boolean` — whether scroll-reveal runs (defaults true; also gated by `prefers-reduced-motion`).
- No data fetching. All content is static.

## Assets
- **Fonts**: Geist + Geist Mono (Google Fonts). Load equivalently in the target app.
- **Images**: none supplied. Every image is a **placeholder slot** to be filled with real assets:
  - Home cards: **3:4 portrait**, export ≈700×930px.
  - Editorial/Advertising row images: **4:3 landscape**, export ≈1200×900px.
  - Thought post hero: **16:9**, export ≈1440×810px.
  - Format JPEG/WebP, keep under ~300–400KB; images crop-to-fill so match the ratio.
  - Placeholder captions in source name the intended subject (e.g. "Cashback card OOH, Dhoby Ghaut").
- No icons (hamburger is three CSS bars). No SVG/illustration.

## Files (in this bundle)
- `Home.dc.html`
- `Editorial Work.dc.html`
- `Advertising Work.dc.html`
- `Thoughts.dc.html`
- `Thought - Newsroom to Brand.dc.html`
- `Thought - Brand Editor.dc.html`
- `Thought - AI-Pilled Playbook.dc.html`
- `Thought - Writing for Trust.dc.html`

The `<x-dc>` wrapper, `{{ }}` holes, `<sc-if>`, `support.js`, and `image-slot.js` are
prototype-runtime only — reproduce the rendered markup/behavior, not those constructs.

## Outstanding content (placeholders to replace)
- Real images in every slot.
- Real headlines + body copy for the four Thought posts (currently Lorem Ipsum) and their index sentences/dates.
- Real URLs: CV download, LinkedIn, and the `#` placeholder links on work items and Thought index.
