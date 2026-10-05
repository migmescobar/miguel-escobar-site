# Handoff: miguel-escobar.com redesign (2026)

This folder is the approved redesign, made on the Claude Design canvas
(https://claude.ai/artifact/K1ihWWgnKJb9zWDwyXXzHP). Mig has signed it off for build. The job is
to implement it in this Astro site, replacing the current design. It supersedes `../design-handoff.md`
and the other files one level up, which describe the previous (Geist) design.

## Ground rules from Mig

- **Copy and content do not change.** Use the current site's words and information; add no text.
  Every string in the boards comes from `source/content_v47.py`, which was taken from the live site.
- **Light theme only.** No dark mode, no theme switch. Some generator code still carries a
  `DARK_MODE` switch; it is off — ignore everything behind it.
- **One typeface, one weight:** PP Neue Montreal Regular (400) everywhere. The fonts are already in
  `src/assets/fonts/`. Mig's Pangram Pangram licence covers this use.
- **Two colours:** paper `#EAE7E1`, ink `#141414`, and alpha tints of ink (tokens in
  `LIGHT` in `source/gen_v47.py`). The only colour beyond these is the cyan/blue glow (see below).
- Desktop frames are 1440 wide; phone frames are 390 wide. Build fluid between them; the boards are the
  two anchor states.

## What is in this folder

| Path | What it is |
|---|---|
| `boards/*.dc.html` | The approved artboards: the complete HTML/CSS of each page, in the canvas's template format. **This is the visual source of truth.** |
| `boards/NewHomePlay`, `NewHomeMobilePlay` | Home as an interactive prototype, with all scroll-driven motion live. The non-Play Home boards are static full-length renders of the same page. |
| `boards/NavBar*`, `LetsTalk*` | Shared components: the nav, and the footer ("Let's talk" + contact list), imported by every page. |
| `boards/NewMenu*` | The open menu overlay. |
| `boards/canvas.json` | Canvas index (frame sizes = intended page heights). |
| `source/gen_v47.py` | The generator that wrote every board. Its comments record **why** each value is what it is, version by version (`V106 (Mig): …`). Read the comment above a constant before changing it. Feature switches like `GLASS_V110 = True` mark the shipped state. |
| `source/content_v47.py` | All copy. |
| `source/fit.json` | Fitted display sizes (hero name 160.85px desktop / 78px phone). |
| `blob-map.json` + `assets/` | Boards reference images and video as `/_blob/<id>`; this maps each id to the file in `assets/`. The highlights reel videos (`highlights-reel-*.mp4` and posters) are new and not yet in the repo. |

### Reading the boards

Each `.dc.html` has a `<helmet>` (styles) and a body under `<x-dc>`. You can ignore the runtime:
`<dc-import name="X">` inlines board `X`, `{{ … }}` are template holes (menu open/closed state,
nav link targets), and the `<script>` blocks only drive the menu toggle and the reel's
pause button. Port the markup and CSS. Inline styles are deliberate and exact.

## Pages

- **Home** (`/`): a continuous scroll. The hero's name, set huge across the page, rises in on load.
  An arrow cue follows. Then the Work chapter (the highlights reel panel, Branded, beside Editorial),
  then the pinned **Policy** section, where the words pull into focus as you scroll and the blue glow
  radiates outward, then Thoughts, then the footer.
- **Work** (one page, e.g. `/work`), replacing Editorial Work and Advertising Work, in three sections:
  Highlights, More Advertising Work, More Editorial Work. Modelled on Monocle and The Economist.
  **Redirect** `/editorial-work` and `/advertising-work` to it. The reel video is Home-only.
- **Thoughts** index and **Thought post**: the existing posts, restyled.
- **404**.

## Behaviour to reproduce

Everything below is CSS, mostly scroll-driven animation (`animation-timeline: scroll()` / `view()`)
with `@supports`/reduced-motion fallbacks. The Play boards' `<style>` hold the exact keyframes and
ranges (`proto_css`, `pol_css`, `glass_v110` in the generator).

1. **Nav.** Mig's name at the left, the menu button (three bars) at the right, over a progressive
   backdrop blur ("glass": stacked `backdrop-filter` layers with smoothstep masks, `GLASS` constant).
   Over the Home reel a smoke band replaces the paper veil. Browsers without scroll timelines keep the
   plain veil.
2. **Nav name.** On every page it links home. On Home it stays hidden until the Work chapter's
   heavy rule reaches the foot of the nav (974px of scroll on desktop, 870px on phone, from
   `NAVNAME_LATE`). Then its two words rise into masks, the way the hero name rose, and they
   drop back out on the way up. Hover dims to 0.6 opacity.
3. **Hero arrow glow.** A soft radial cyan glow behind the arrow (radius 220px desktop / 180px phone,
   softened profile `CUE_GLOW_SOFT`). It overlaps neighbouring elements and recedes into the arrow over
   the first 40% of a screen's scroll.
4. **Policy.** Pinned stage; the text resolves from blur to sharp as you scroll, and the glow radiates
   outward simultaneously (`POL_RADIATE`, starting at 0.45 of the range).
5. **Menu.** Full-screen overlay; list of Home, Work, Thoughts, Contact; no switch.
6. **Cards.** No hover glow (removed in V112). Uniform size and alignment.
7. Respect `prefers-reduced-motion`: every animation has a still end state in the boards' CSS.

## One open item

**Nav name tracking.** The name in the nav is 15px with `letter-spacing: -0.03em`, the hero's
value, so the nav name is an exact scaled copy of the hero name. (Measured: at 2x pixel density the
nav render matches the hero scaled down to within 0.2% ink.) Mig felt it reads slightly tight at that
size. That is expected: tracking chosen for 160px looks tight at 15px. The pairs AR, SC and BA come
within about 1px of touching. Measured closest gaps at 15px:

| letter-spacing | tightest pair (AR) | mean pair gap |
|---|---|---|
| -0.03em (current) | 0.80px | 1.53px |
| -0.01em | 1.10px | 1.83px |
| 0 | 1.25px | 1.98px |
| +0.01em | 1.40px | 2.13px |

Recommendation: **0** (`NAVNAME_CSS` in the generator). It is a loosening of 0.03em, about half a
pixel per letter, consistent with the site's own V101 rule that tracking opens as size falls. Keep the
0.2em word gap. Confirm the value with Mig before shipping.

## Build notes

- Fonts: `font-kerning: normal`, `-webkit-font-smoothing: antialiased`, base `letter-spacing: 0.02em`;
  each text role sets its own tracking by size (`LABEL`, `LEAD`, `BODY`, headline roles in the generator).
- Keep the existing Astro stack, sitemap, OG image scripts, and the downloadable CV.
- Optimise the reel: the boards use a 720p landscape, a vertical, and a 4:5 cut, each with a poster.
- Verify against the boards side by side at 1440 and 390 before merging.
