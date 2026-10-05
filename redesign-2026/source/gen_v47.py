# miguel-escobar.com redesign on the Design canvas, V49.
# One family (Neue Montreal) and two colours (ink and off-white) for everything; light and dark themes; a nav of two
# buttons (theme, menu) over a five-item menu; the home page reordered (work first) with its headlines typed in;
# Branded is the highlights reel with its words over it, beside Editorial on a desktop.
# MEASURE=1 writes roots with height:auto so the preview harness can measure real heights.
import json, math, os, re, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content_v47 import (NAME, STATEMENT, SCROLL, EDITORIAL, ADVERTISING, THOUGHTS_TITLE, THOUGHTS_SUB, ENTRY,
                         POST_PARAS, POST_TITLE, HANG, POST_DECK, FEATURED, MORE)

SCR = '/tmp/claude-0/-home-claude/26df12c1-35a6-5dcc-93b0-3bafd6432f7f/scratchpad'
ROOT = os.path.join(SCR, 'canvas')
P = os.path.join(ROOT, 'project')
MEASURE = os.environ.get('MEASURE') == '1'
HEIGHTS = json.load(open(os.path.join(SCR, 'heights.json'))) if os.path.exists(os.path.join(SCR, 'heights.json')) else {}
FIT = json.load(open(os.path.join(SCR, 'fit.json'))) if os.path.exists(os.path.join(SCR, 'fit.json')) else {}

BLOB = {
    'font': '/_blob/9a4426dde9e70c65ccd45b0c0b192e4e',
    'font-italic': '/_blob/feaee5c532dd527b59acc4386d5ea837',
    'home-osc': '/_blob/8cad5cba46236ddb073c3722d5bf8011',
    'home-age-checks': '/_blob/6431bfbe806ca058f5a805a87865db21',
    'home-whitewash': '/_blob/bc81976e2c9a210b898426eda8c2172e',
    'home-pulpit': '/_blob/334edb3bec8b45ef9fb5855bad5110ba',
    'home-advertising': '/_blob/0a7e63ddf093eada74a8cdd6cff0bb61',
    'home-editorial': '/_blob/bc9a9f557593ad6b2a9370b57f5db877',
    'editorial-politics': '/_blob/155be574c40441acb20003fc6cf160f4',
    'editorial-culture': '/_blob/808681a5040ae1965729bb4b54f0b161',
    'editorial-tatler': '/_blob/e2ee4e9e0673b4f143d1c524840d20da',
    'editorial-smile': '/_blob/b6b51f4aff8c99a8016feb948de73217',
    'ads-trust': '/_blob/85bb848b96b766cd87bef1ccb9236f4c',
    'ads-nba': '/_blob/3d82d1a37dd94f925a82a211c1d80686',
    'ads-alcon': '/_blob/9b7e6af295e9f03a8786046466721053',
    'ads-gotyme': '/_blob/d328fe931c7bbed6bf6463910d1569d3',
    'reel-v': '/_blob/fb28d7924c560483f09861f2cccd52a1',        # the phone's cut of the highlights reel: 9:16 from the 1080p master, reframed shot by shot
    'reel-v-poster': '/_blob/0579d1b2e90ae09ea0bd6c1c880bbd49',
    'reel-45': '/_blob/e38ab1401c9adabcdd72a726b1eafbbc',       # the desktop cut: 4:5 (864x1080), reframed the same way; 13 s, silent
    'reel-45-poster': '/_blob/878e22906607b66f9f6471ce21b95d3c',
    'editorial-konfekt': '/_blob/d9c797abb6508fcec807a6e0e8c34c80',   # the Konfekt placeholder (836 x 1124): out since V59
    'writer': '/_blob/5fb6de3c4bd931078a20b0ec3e2c0205',
    'work-goodmen': '/_blob/35fac2c7d51797f7693c198b9a7d43fa',   # V93: Mig's own 4:3 crop for A Few Good Men (1200 x 900)
    'work-denim': '/_blob/58df362da375ebabde34beeafcefc028',     # V93: Mig's own 4:3 crop for the selvedge denim feature (1200 x 900)
    'ph-politics': '/_blob/ed22d0e82973d2f927b07c708f98623d',   # V91: Mig's portrait of Mocha Uson from the Esquire feature (1000 x 1400, 5:7)   # V78: PP Writer Regular (woff2, from Mig's OTF)
}

# ── Palette and theme ────────────────────────────────────────────────────────────────────────────────────────
# Two colours only, ink and off-white (paper), and tints of each. The accent comes later: `--accent` is the hook
# (the headlines' subject phrases take it) and for now it is the text colour itself.
PAPER, INK = '#EAE7E1', '#141414'
SANS = "'Neue Montreal', Helvetica, Arial, sans-serif"
BASE = (f"font-family: {SANS}; font-size: 16px; letter-spacing: 0.02em; -webkit-font-smoothing: antialiased; "
        "font-kerning: normal; font-variant-ligatures: common-ligatures; text-rendering: optimizeLegibility;")
NOUL = 'color: inherit; text-decoration: none;'

# Everything that changes with the theme is a variable. Light: paper ground, ink text, an ink footer. Dark: the pair
# swaps (ink ground, paper text, a paper footer). Headlines are two-tone: the lead-in in `muted` (the text colour at
# 55%: 3.8:1 on paper, 5.2:1 on ink, both past the 3:1 large text needs), the subject phrase in full. Inline styles
# carry the light value as a fallback, so a component board renders on its own; the variables themselves live in
# each page's helmet.
LIGHT = dict(bg=PAPER, fg=INK, fg85='rgba(20, 20, 20, 0.85)', fg75='rgba(20, 20, 20, 0.75)', fg70='rgba(20, 20, 20, 0.7)',
             muted='rgba(20, 20, 20, 0.55)', grid='rgba(20, 20, 20, 0.16)', rule='rgba(20, 20, 20, 0.25)', ring='rgba(20, 20, 20, 0.3)', ul='rgba(20, 20, 20, 0.4)',
             wash='rgba(20, 20, 20, 0.06)', accent=INK, caret=INK, fbg=INK, ffg=PAPER, f75='rgba(234, 231, 225, 0.75)',
             f70='rgba(234, 231, 225, 0.7)', frule='rgba(234, 231, 225, 0.3)')
DARK = dict(bg=INK, fg=PAPER, fg85='rgba(234, 231, 225, 0.85)', fg75='rgba(234, 231, 225, 0.75)', fg70='rgba(234, 231, 225, 0.7)',
            muted='rgba(234, 231, 225, 0.55)', grid='rgba(234, 231, 225, 0.16)', rule='rgba(234, 231, 225, 0.25)', ring='rgba(234, 231, 225, 0.3)', ul='rgba(234, 231, 225, 0.4)',
            wash='rgba(234, 231, 225, 0.06)', accent=PAPER, caret=PAPER, fbg=PAPER, ffg=INK, f75='rgba(20, 20, 20, 0.75)',
            f70='rgba(20, 20, 20, 0.7)', frule='rgba(20, 20, 20, 0.3)')
C = {k: f'var(--{k}, {v})' for k, v in LIGHT.items()}
# V115 (Mig): no dark theme. The site is paper and ink: no switch in the menu, no theme tweak on the boards, no dark
# rules in any page's CSS or theme state in its script, and the two dark previews leave the canvas. DARK_MODE = True
# puts it all back.
DARK_MODE = False
THEME_CSS = (':root{' + ';'.join(f'--{k}:{v.replace(" ", "")}' for k, v in LIGHT.items()) + '}\n'
             + ('.me-dark{' + ';'.join(f'--{k}:{v.replace(" ", "")}' for k, v in DARK.items()) + '}\n' if DARK_MODE else ''))

# ── Grid, rhythm and text roles ──────────────────────────────────────────────────────────────────────────────
COL, GUT = (1312 - 11 * 24) / 12, 24     # 12 columns at 1440: 64 margins, 24 gutters
GRID12 = 'display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); column-gap: 24px;'


def span(n):
    return round(n * COL + (n - 1) * GUT, 2)


HERO_MAXW = round(span(10))
FOOT_OVERLAP = 4      # the footer is pulled up over the page by this much, so no seam shows between them
HERO_OVERLAP = 4      # home: the chapters are pulled up over the hero's foot by this much (and padded back down), so
                      # the page's dark ground cannot show through the join as a hairline when the canvas scales the page
WIDE_GAP = 2 * GUT    # two gutters: between an element and the one beside it where one is large (the map, the reel
                      # panel); the element on the left stops a gutter short, so the grid's lines stay where they are
FOOT_LIST_TOP = 13    # desktop footer: the contact list's top rule level with the cap height of "Let's talk"
HEAVY = 4             # the heavy rule that opens a section or a list; hairlines (1px) separate the items within it


# V101 type audit: one weight (Regular) stays; tracking is set by size, so the phone's smaller display type is no
# longer as tight as the desktop's (the tracking that suits 152px crowds 64px), and the smallest text opens up a
# little. TYPE_V101 = False puts V100's values back.
TYPE_V101 = True


def LABEL(px, color=None):
    """Labels (dates, eyebrows, the footer's small print): small capitals in the one family."""
    ls = ('0.07em' if px <= 11 else '0.06em') if TYPE_V101 else '0.06em'
    feat = " font-feature-settings: 'case';" if TYPE_V101 else ''
    return (f'font-size: {px}px; line-height: 1.4; letter-spacing: {ls}; text-transform: uppercase;{feat} '
            f'color: {color or C["fg70"]};')


LABEL_PX = {'d': 12, 'm': 11}
LEAD = {'d': 'font-size: 22px; line-height: 1.4; letter-spacing: 0.005em;',
        'm': 'font-size: 19px; line-height: 1.4; letter-spacing: 0.005em;'}
BODY = 'font-size: 17px; line-height: 1.65; letter-spacing: 0.01em;'
BODY_L = 'font-size: 22px; line-height: 1.55; letter-spacing: 0.005em;'    # desktop statements

# ── Headlines in PP Writer (V78) ─────────────────────────────────────────────────────────────────────────────
# Headlines and titles are set in PP Writer (Pangram Pangram's serif, its Regular cut): the page titles, the hero's
# statement, the home chapters' headlines, Policy's, the rail's captions, the Work page's titles, Thoughts' entry and
# the post's title, the footer's "Let's talk". The name, the body, labels, leads, links and the menu stay in Neue
# Montreal. Each headline keeps its size; Writer takes its own tracking (looser than Neue Montreal's at display
# sizes) and, where lines stack, more leading (its ascenders and descenders run to .76 and .23 of the em, against
# Neue Montreal's .715 and .18). Single-line titles keep theirs, so they sit where they did.
# SERIF = False puts every headline back in Neue Montreal (V77 exactly). On the canvas, each page's `headlines`
# tweak (serif / sans) swaps them back on that board alone: every serif headline carries its Neue Montreal tracking
# and leading in custom properties (--ls-sans, --lh-sans), and the class `me-hs`, which the switch keys on.
SERIF = False
THEME_CLS = ' {{ themeCls }}' if DARK_MODE or SERIF else ''   # the class binding a page's root carries (V115: none)
THEME_ATTR = ' class="{{ themeCls }}"' if DARK_MODE or SERIF else ''
WRITER = "'PP Writer', Georgia, 'Times New Roman', serif"


def sf(css, ls, lh=None):
    """A headline role in Writer: the same size, Writer's tracking `ls` and (where given) leading `lh`."""
    if not SERIF:
        return css
    ls0 = re.search(r'letter-spacing: ([^;]+);', css).group(1)
    lh0 = re.search(r'line-height: ([^;]+);', css).group(1)
    out = re.sub(r'letter-spacing: [^;]+;', f'letter-spacing: {ls};', css)
    if lh:
        out = re.sub(r'line-height: [^;]+;', f'line-height: {lh};', out)
    return f'font-family: {WRITER}; {out} --ls-sans: {ls0}; --lh-sans: {lh0};'


H2_SANS = {'d': 'font-size: 84px; font-weight: 400; line-height: 1.02; letter-spacing: -0.026em;',
           'm': 'font-size: 40px; font-weight: 400; line-height: 1.06; letter-spacing: -0.02em;'}
H2 = {'d': sf(H2_SANS['d'], '-0.012em', '1.06'), 'm': sf(H2_SANS['m'], '-0.008em', '1.1')}
# Page titles (Work, Thoughts, the 404's, the footer's "Let's talk"): one line each, their leading as it was; the
# phone's 404 title runs to two lines, so it takes Writer's leading ('m2').
TITLE_XL_SANS = {'d': 'font-size: 152px; font-weight: 400; line-height: 0.9; letter-spacing: -0.035em;',
                 'm': f'font-size: 64px; font-weight: 400; line-height: 0.94; letter-spacing: {"-0.025em" if TYPE_V101 else "-0.035em"};'}
TITLE_XL = {'d': sf(TITLE_XL_SANS['d'], '-0.02em'), 'm': sf(TITLE_XL_SANS['m'], '-0.02em'),
            'm2': sf(TITLE_XL_SANS['m'], '-0.02em', '1')}
# The rail's captions (the samples' titles).
CAPTION = {'d': sf('font-size: 22px; line-height: 1.3; letter-spacing: 0.005em;', '0em'),
           'm': sf(f'font-size: 16px; line-height: 1.3; letter-spacing: {"0.012em" if TYPE_V101 else "0.005em"};', '0.005em')}
if SERIF and HANG:
    HANG = ' text-indent: -0.4em; --ti-sans: -0.3em;'   # the post title's opening quote hangs: Writer's is wider
# Writer's wider set moves some headlines' line breaks, so they are held where a serif page would hold them: an
# article (a, an, the) never ends a line, and a possessive stays with the quoted title it owns ("Nolan's
# “Odyssey”"). Typed headlines hold words together in a no-wrap span (a no-break space cannot: every word there is
# an inline block, and the line may break either side of one); plain ones take a no-break space.
ARTICLES = ('a', 'an', 'the')
HOLD_ARTICLES = True   # V79: in any face


def bind_hl(text):
    """A plain headline's text, its articles and possessive titles held to the words after them (V78, serif only)."""
    if not HOLD_ARTICLES:
        return text
    text = re.sub(r'(?<![\w’])(a|an|the|A|An|The) (?=\S)', '\\1\u00a0', text)
    return re.sub(r'(\w’s) (“)', '\\1\u00a0\\2', text)
# Vertical spacing: one value per relationship, the same wherever the relationship recurs (V52 audit).
SECTION = {'d': 192, 'm': 112}      # a major break, measured from the last line or edge to the next rule (or the
                                    # footer): hero to first chapter, chapter to chapter, last line to footer
PAGE_BOTTOM = SECTION               # inner pages: from the last line or rule to the footer
CH_PAD = {'d': SECTION['d'] // 2, 'm': SECTION['m'] // 2}   # home: half a break above each chapter, half below
FIRST_CH_TOP = {'d': 146, 'm': 82}  # home: over the first chapter, so the name's baseline sits a full break above its rule
RAIL_TAIL = {'d': 0, 'm': 20}       # home: one caption on the rail runs a line longer than the rest (Trust Bank's on a
                                    # desktop, Esquire's on a phone), so the break under the rail is taken from the rest
PAGE_TOP_CAP = {'d': 205, 'm': 135} # every page's first caps (titles, labels, the hero's statement) sit this far down
HERO_TOP = {'d': 121, 'm': 73}      # the hero statement's margin, to put its caps there
ITEM = {'d': 120, 'm': 64}          # between the rows of a list of work
TOP = {'d': 120, 'm': 72}           # under the nav to a page's title; the footer's top to "Let's talk"
TITLE_TO_RULE = {'d': 104, 'm': 48} # a page's title (or the lead under it) to the first rule (baseline to rule: 119 / 56)
BLOCK = {'d': 64, 'm': 32}          # a headline to the block it introduces (the rail)
TEXT = {'d': 40, 'm': 28}           # a page's title to its lead or deck (no divider over it); under a divider, text_gap
ACTION = {'d': 44, 'm': 32}         # text to the link that follows it
LABEL_GAP = {'d': 28, 'm': 22}      # a page's label (a date, "Error 404") to its title
PARA = '1em'                        # paragraph to paragraph, everywhere body text runs
TEXT_TAIL = 4                       # a body line's half-leading, taken off where a page ends on text
HEAD_GAP = {'d': 28, 'm': 22}       # from a rule down to the box of the headline it opens (V61: a pinch more than
                                    # 20 / 16; LABEL_GAP's values); the text under the headline follows it (text_gap)
RAIL_NAV_DROP = 11                  # desktop: the rail's rings sit centred on the headline's last line
# Measured offsets (the alignment checks set these).
LABEL_TOP = {'d': 130, 'm': 76}     # padding over a page that opens on a label, so its caps sit where titles' do
NF_GRID_TOP = TITLE_TO_RULE['d']    # 404, desktop: title box to the list's rule
NF_LEAD_LIFT = 7                    # 404, desktop: the lead's cap height level with the list's rule
LEAD_TO_RULE_M = TITLE_TO_RULE['m'] # phone: a lead's box to the list's rule under it
THOUGHTS_SUB_DROP = 7               # Thoughts, desktop: the lead's last baseline on the title's
MAP_COLS = 7                        # About, desktop: the map sits in seven columns, stopping a gutter short (731 x 357);
                                    # the words take the last five
MAP_W_D = round(span(MAP_COLS) - (WIDE_GAP - GUT), 2)   # 731.33: the desktop map's width; its height follows the projection (2.05:1)
MENU_LS = {'d': '-0.026em', 'm': '-0.02em'} if TYPE_V101 else {'d': '-0.035em', 'm': '-0.035em'}   # V101: as the headlines at each size
MENU_FS = {'d': 84, 'm': 40}        # menu items: the headline size (the phone's is what fits "Advertising Work")
PANEL_H = 780                       # phone: the reel panel Branded's words sit in (a screen, less the nav)
# V60: under a divider, the space from a headline's last baseline to the capitals of the text under it matches the
# space from the divider down to the headline's capitals, everywhere. The gaps between the boxes that do that follow
# from Neue Montreal's vertical metrics, per em (ascent .958, descent .242, capitals .715), laid out as Chrome does:
# ascent and descent each rounded to the pixel, the half-leading over them floored, so a line's baseline sits a whole
# number of pixels below its top.
F_ASC, F_DESC, F_CAP = 0.958, 0.242, 0.715
F_SERIF = (1.05, 0.34, 0.71)    # PP Writer's (V78): ascent, descent, capitals; x-heights .51 (sans) and .49 (serif)
F_X = {'sans': 0.51, 'serif': 0.49}


def fmetrics(css):
    """(ascent, descent, capitals) per em of the family a role's CSS sets."""
    return F_SERIF if 'PP Writer' in css else (F_ASC, F_DESC, F_CAP)


def size_lh(css):
    """(font size, line height in px) from a text role's CSS."""
    fs = float(re.search(r'font-size: ([\d.]+)px', css).group(1))
    return fs, fs * float(re.search(r'line-height: ([\d.]+);', css).group(1))


def baseline(css):
    """From the top of a line box to its baseline."""
    fs, lh = size_lh(css)
    asc, desc, _ = fmetrics(css)
    a, d = int(asc * fs + 0.5), int(desc * fs + 0.5)
    return math.floor((lh - a - d) / 2) + a


def cap_drop(css):
    """From the top of a line box to the tops of its capitals."""
    return baseline(css) - fmetrics(css)[2] * size_lh(css)[0]


def base_foot(css):
    """From a line box's baseline down to its bottom."""
    return size_lh(css)[1] - baseline(css)


def text_gap(head, body, k):
    """The gap between a headline's box and the box of the text under it that puts the text's capitals as far
    below the headline's last baseline as the headline's capitals sit below the divider over it."""
    return round(HEAD_GAP[k] + cap_drop(head) - base_foot(head) - cap_drop(body), 2)


def x_mid(css):
    """From a line box's bottom up to the middle of its x-height."""
    return base_foot(css) + F_X['serif' if 'PP Writer' in css else 'sans'] * size_lh(css)[0] / 2


# V78: what Writer's metrics and leading move, put back where the offsets were measured on Neue Montreal: the hero
# statement's capitals (on the page's line for first capitals), the footer's contact list (its rule level with the
# capitals of "Let's talk"), the rail's rings (centred on the headline's last line), and the phone's 404 title (its
# capitals as far under the label as any page title's).
if SERIF:
    HERO_TOP = {k: round(HERO_TOP[k] - (cap_drop(H2[k]) - cap_drop(H2_SANS[k])), 2) for k in HERO_TOP}
    FOOT_LIST_TOP = round(FOOT_LIST_TOP + cap_drop(TITLE_XL['d']) - cap_drop(TITLE_XL_SANS['d']), 2)
    RAIL_NAV_DROP = round(RAIL_NAV_DROP + x_mid(H2['d']) - x_mid(H2_SANS['d']), 2)
NF_TITLE_TOP_M = round(LABEL_GAP['m'] - (cap_drop(TITLE_XL['m2']) - cap_drop(TITLE_XL_SANS['m'])), 2)
# and the lead under it as far from the title's last baseline as the Work and Thoughts leads are from theirs
NF_LEAD_TOP_M = round(TEXT['m'] - (base_foot(TITLE_XL['m2']) - base_foot(TITLE_XL['m'])), 2)


# Desktop, Editorial and Branded side by side, six columns each: Branded is the phone's reel panel at 4:5, and both
# halves take the panel's type, scaled so its words cover the same share of it as on the phone (about half).
PANEL_W = round(span(6))            # 644, so 805 tall
PAIR = dict(h2=sf('font-size: 56px; font-weight: 400; line-height: 1.04; letter-spacing: -0.024em;', '-0.01em', '1.08'),
            body='font-size: 19px; line-height: 1.6; letter-spacing: 0.008em;', pad=32, p_to_link=ACTION['m'])
PAIR['h_to_p'] = text_gap(PAIR['h2'], PAIR['body'], 'd')   # 12.3
PAIR_TEXT_W = PANEL_W - 2 * PAIR['pad']   # 580: the measure of both halves' words
VEIL = ('linear-gradient(to bottom, rgba(20, 20, 20, 0.18) 0%, rgba(20, 20, 20, 0.72) 42%, rgba(20, 20, 20, 0.84) 100%)')

# ── Page CSS ─────────────────────────────────────────────────────────────────────────────────────────────────
PAGE_CSS = THEME_CSS + """::selection{background:var(--fg);color:var(--bg)}
a:focus-visible,button:focus-visible{outline:2px solid currentColor;outline-offset:4px}
a.ul:hover{text-decoration-color:currentColor !important}
a.entry:hover .entry-title{opacity:1 !important}
a.lrow .lrow-arrow{transition:transform .5s cubic-bezier(0.16,1,0.3,1),opacity .35s ease}
a.lrow:hover .lrow-arrow{opacity:1 !important;transform:translateX(3px)}
a.lrow.ext:hover .lrow-arrow{transform:translate(2px,-2px)}
a.lrow:hover .lrow-label{text-decoration-line:underline;text-decoration-thickness:1px;text-underline-offset:5px}
.me-sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap;border:0}
.me-iconbtn{display:flex;align-items:center;justify-content:center;flex-shrink:0;width:44px;height:44px;padding:0;margin:0;border:0;border-radius:0;background:transparent;color:inherit;font:inherit;cursor:pointer;-webkit-tap-highlight-color:transparent}
.me-themeicon{display:block}
.me-menu{visibility:hidden;opacity:0;transition:opacity .3s ease,visibility 0s linear .3s}
.me-menu.is-open{visibility:visible;opacity:1;transition:opacity .3s ease}
.me-mi{transform:translateY(16px);opacity:0;transition:transform .7s cubic-bezier(0.16,1,0.3,1),opacity .45s ease}
.me-menu.is-open .me-mi{transform:none;opacity:1}
.me-menu.is-open .me-mi:nth-child(2){transition-delay:.05s}
.me-menu.is-open .me-mi:nth-child(3){transition-delay:.1s}
.me-menu.is-open .me-mi:nth-child(4){transition-delay:.15s}
.me-menu.is-open .me-mi:nth-child(5){transition-delay:.2s}
a.me-mi:hover .me-mlabel{text-decoration-line:underline;text-decoration-thickness:2px;text-underline-offset:.12em}
@media (prefers-reduced-motion: reduce){.me-menu,.me-mi{transition:none !important}}
"""

# V67: the nav's buttons are glass (after Petr Knoll's "Glass Button" pen, scaled to a 44px disc): a faint white
# sheen, a shade inside the top and a highlight inside the foot, a hairline rim whose two darker arcs catch the light
# like a lens's edge, a diagonal shine laid on in screen, and a soft shadow under it. On hover the disc gives a
# little, the rim's arcs turn and the shine slides; pressed, it sinks. In the dark theme the glass is clearer and
# its rim's arcs catch the light instead of darkening, as glass does on a dark ground. The frosted band stays
# behind them.
# GLASS_BTNS = False puts back the bare icons (their ink on the page margins).
GLASS_BTNS = False   # V68: back to bare icons (the glass went into the band instead)
GLASS_BTN_CSS = """@property --me-rim{syntax:"<angle>";inherits:false;initial-value:-75deg}
.me-glassbtn{position:relative;border-radius:50%;background:linear-gradient(-75deg,rgba(255,255,255,.04),rgba(255,255,255,.18),rgba(255,255,255,.04));box-shadow:inset 0 2px 2px rgba(0,0,0,.05),inset 0 -2px 2px rgba(255,255,255,.5),0 4px 2px -2px rgba(0,0,0,.16),inset 0 0 1.5px 4px rgba(255,255,255,.15),0 7px 14px -7px rgba(0,0,0,.22);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);transition:transform .4s cubic-bezier(.25,1,.5,1),box-shadow .4s cubic-bezier(.25,1,.5,1)}
.me-glassbtn>*{position:relative;z-index:1}
.me-glassbtn::before{content:"";position:absolute;inset:1px;border-radius:50%;pointer-events:none;background:linear-gradient(-45deg,rgba(255,255,255,0) 0%,rgba(255,255,255,.5) 40% 50%,rgba(255,255,255,0) 55%) 0% 50%/200% 200% no-repeat;mix-blend-mode:screen;transition:background-position .5s cubic-bezier(.25,1,.5,1)}
.me-glassbtn::after{content:"";position:absolute;inset:0;border-radius:50%;padding:1px;box-sizing:border-box;pointer-events:none;background:conic-gradient(from var(--me-rim) at 50% 50%,rgba(0,0,0,.45),rgba(0,0,0,0) 5% 40%,rgba(0,0,0,.45) 50%,rgba(0,0,0,0) 60% 95%,rgba(0,0,0,.45)),linear-gradient(rgba(255,255,255,.5),rgba(255,255,255,.5));-webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);mask-composite:exclude;transition:--me-rim .5s ease}
.me-glassbtn:hover{transform:scale(.975);box-shadow:inset 0 2px 2px rgba(0,0,0,.05),inset 0 -2px 2px rgba(255,255,255,.5),0 3px 1px -2px rgba(0,0,0,.2),inset 0 0 1px 2px rgba(255,255,255,.5),0 5px 10px -6px rgba(0,0,0,.22)}
.me-glassbtn:hover::before{background-position:25% 50%}
.me-glassbtn:hover::after{--me-rim:-125deg}
.me-glassbtn:active{transform:scale(.94)}
.me-glassbtn:active::before{background-position:50% 15%}
.me-dark .me-glassbtn{background:linear-gradient(-75deg,rgba(255,255,255,.02),rgba(255,255,255,.09),rgba(255,255,255,.02));box-shadow:inset 0 2px 2px rgba(0,0,0,.2),inset 0 -2px 2px rgba(255,255,255,.2),0 4px 2px -2px rgba(0,0,0,.35),inset 0 0 1.5px 4px rgba(255,255,255,.06),0 7px 14px -7px rgba(0,0,0,.45)}
.me-dark .me-glassbtn:hover{box-shadow:inset 0 2px 2px rgba(0,0,0,.2),inset 0 -2px 2px rgba(255,255,255,.2),0 3px 1px -2px rgba(0,0,0,.4),inset 0 0 1px 2px rgba(255,255,255,.16),0 5px 10px -6px rgba(0,0,0,.45)}
.me-dark .me-glassbtn::after{background:conic-gradient(from var(--me-rim) at 50% 50%,rgba(255,255,255,.55),rgba(255,255,255,0) 5% 40%,rgba(255,255,255,.55) 50%,rgba(255,255,255,0) 60% 95%,rgba(255,255,255,.55)),linear-gradient(rgba(255,255,255,.14),rgba(255,255,255,.14))}
@media (prefers-reduced-motion: reduce){.me-glassbtn,.me-glassbtn::before,.me-glassbtn::after{transition:none}}
"""
if GLASS_BTNS:
    PAGE_CSS += GLASS_BTN_CSS


def btn_look(side):
    """A nav button's class and margin: glass discs sit with their edge on the page margin; bare icons hang their
    ink there (the button's box overhangs the margin by the icon's inset)."""
    if GLASS_BTNS:
        return ' me-glassbtn', ''
    return '', f' style="margin-{side}: {-15 if side == "right" else -13}px;"'


# Home only (static and prototype alike, so both lay out identically).
HOME_CSS = """.w{display:inline-block}
.me-em{color:var(--accent)}
.me-dot{transform-box:fill-box;transform-origin:center}
a.me-link .me-ring{transition:background-color .35s ease,border-color .35s ease,color .35s ease}
a.me-link .me-arrow{transition:transform .5s cubic-bezier(0.16,1,0.3,1)}
a.me-link:hover .me-ring{background-color:var(--fg);border-color:var(--fg);color:var(--bg)}
a.me-link:hover .me-arrow{transform:translateX(3px)}
a.me-link:hover .me-link-label{text-decoration-line:underline;text-decoration-thickness:1px;text-underline-offset:5px}
a.me-card:hover .me-card-desc{text-decoration-line:underline;text-decoration-thickness:1px;text-underline-offset:5px}
.me-rail{display:flex;overflow-x:auto;overflow-y:hidden;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scrollbar-width:none}
.me-rail::-webkit-scrollbar{display:none}
.me-rail>.me-card{position:relative;flex:0 0 auto;scroll-snap-align:start}
.me-rail>.me-card:not(:last-child)::after{content:"";position:absolute;top:0;bottom:0;right:-12.5px;width:1px;background:var(--fg)}
.me-rail-m>.me-card:not(:last-child)::after{right:-8.5px}
.me-railbtn{display:flex;align-items:center;justify-content:center;width:48px;height:48px;padding:0;box-sizing:border-box;border:1px solid var(--ring);border-radius:50%;background:transparent;color:var(--fg);cursor:pointer;transition:background-color .35s ease,border-color .35s ease,color .35s ease,opacity .35s ease}
.me-railbtn:hover:not(:disabled){background:var(--fg);border-color:var(--fg);color:var(--bg)}
.me-railbtn:disabled{opacity:.28;cursor:default}
.me-reelbtn{position:absolute;right:16px;top:16px;z-index:1;display:flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;box-sizing:border-box;border:1px solid rgba(234,231,225,.6);border-radius:50%;background:rgba(20,20,20,.3);color:#EAE7E1;cursor:pointer;transition:background-color .3s ease}
.me-reelbtn:hover{background:rgba(20,20,20,.6)}
.me-ico-play{display:none}
.me-reel.is-paused .me-ico-play{display:block}
.me-reel.is-paused .me-ico-pause{display:none}
.me-onvideo{--fg:#EAE7E1;--bg:#141414;--muted:rgba(234,231,225,.6);--accent:#EAE7E1;--caret:#EAE7E1;--ring:rgba(234,231,225,.55)}
"""
# About's map: rings pulse out from Singapore across Southeast Asia without end, one setting out every PULSE / RIPPLES
# seconds (negative delays, so the pulse is already running when the page opens). Each ring widens fast and slows
# (ease-out) while it holds its strength and fades late (ease-in), so it is still visible as it reaches the region's
# edge. With reduced motion, one still ring marks that edge instead.
RIPPLES, PULSE = 3, 4.2
HOME_CSS += ('@keyframes me-pulse{0%{r:var(--dot);opacity:0;animation-timing-function:cubic-bezier(0.22,0.61,0.36,1)}'
             '7%{opacity:.9;animation-timing-function:ease-in}100%{r:var(--rip);opacity:0}}\n'
             '@media (prefers-reduced-motion: no-preference){\n'
             f'.me-ripple{{animation:me-pulse {PULSE}s infinite}}\n'
             + ''.join(f'.me-ripple:nth-child({i + 1}){{animation-delay:-{round(PULSE * i / RIPPLES, 2)}s}}\n' for i in range(1, RIPPLES))
             + '}\n@media (prefers-reduced-motion: reduce){.me-ripple:first-child{r:var(--rip);opacity:.3}}\n')

# ── Policy: solid blue, the words come into focus (V65; V62–V63's spray and V64's pivot are out) ───────────────
# POLICY_FX = False puts V61's Policy back (the rest of the page as it now stands).
# Policy is a stage a screen tall, solid in the site's blue from its top edge, its words centred on it in paper. In
# the prototype the stage pins for a beat. The words arrive out of focus, a soft glassy haze of themselves, and as
# the stage settles they sharpen: the headline first, the paragraph a moment after (a timed transition, like the
# other headlines' typing, set off as the stage nears the top of the screen; it stays sharp once it has resolved).
# On the full-page boards, with reduced motion, or without scroll timelines, the words are simply sharp.
POLICY_FX = True
POL = dict(pin=0.5,            # the stage stays pinned for this share of a screen's scrolling
           focus_at=0.82,      # the words start to sharpen once the stage's top is this share of a screen up
           blur='0.26em',      # how far out of focus they start (in em, so headline and paragraph look alike)
           haze=0.5,           # and how strongly the haze shows
           dur=1.6,            # seconds to sharpen
           lag=0.35)           # the paragraph follows the headline by this much
POL_BLUE = '#0047BB'    # the site's blue, in both themes
POL_TEXT = ('#EAE7E1', 'rgba(234, 231, 225, 0.92)', 'rgba(234, 231, 225, 0.66)')   # emphasis; words; lead-in
# V102: Policy on the zine's blue (Mig's reference): a soft sphere of cyan, deep azure at its heart, cyan through its
# body, paling out to paper at its edge. The stops are measured from the reference's sphere, each moved (in OKLab) by
# the difference between the reference's cool ground and our warm paper, in proportion to how much ground shows
# through it: the sphere keeps the reference's colour where it is solid and meets our paper as it fades, with no
# halo where cool would meet warm. The stage is paper in both themes (in the dark one it already was), so the words
# are ink in both, the nav goes ink over it, and the hairline that parted it from the footer stays only where the
# two would otherwise run together (the dark theme's paper footer). The sphere fades out inside the stage's height,
# so no edge of it shows where the stage meets the sections either side. The lead-in takes 58% ink, which keeps 3:1
# at the sphere's deepest point. POL_GLOW = False puts V101's ink stage back.
POL_GLOW = True
POL_GLOW_R = {'d': 430, 'm': 200}   # px: where the sphere has faded out to paper
POL_GLOW_STOPS = [(0.0, '#00A1DF'), (0.081, '#00A8E4'), (0.161, '#00AEE6'), (0.242, '#00B4E7'), (0.323, '#00B9E7'),
                  (0.363, '#10BEE7'), (0.403, '#24BFE8'), (0.444, '#44C2E7'), (0.484, '#59C6E6'), (0.524, '#6EC7E6'),
                  (0.565, '#7DCBE4'), (0.605, '#8DCEE4'), (0.645, '#98D0E5'), (0.685, '#A6D4E4'), (0.726, '#B0D8E4'),
                  (0.766, '#BCD9E4'), (0.806, '#C5DBE4'), (0.847, '#D0DFE4'), (0.887, '#D6E2E2'), (0.927, '#E2E4E3'),
                  (0.968, '#E8E6E1'), (1.0, PAPER)]


def pol_glow(mobile):
    r = POL_GLOW_R['m' if mobile else 'd']
    stops = ', '.join(f'{c} {round(f * r, 1):g}px' for f, c in POL_GLOW_STOPS)
    at = '50% 390px' if (mobile and BOXES) else '50% 50%'   # V103: on a phone, its heart where the note meets the headline
    return f'radial-gradient(circle at {at}, {stops}) {PAPER}'


# V112 (Mig): the sphere radiates outward as the words come into focus. It lies on its own layer under the words, drawn
# as before (the same stops about the same heart), and in the prototype it waits at POL_RADIATE_FROM of its size until
# the focus pull sets off, then opens to its full size on the same trigger, clock and curve as the headline's focus, so
# the light and the focus arrive as one movement; like the focus it stays open, however the page is scrolled after. On
# the full-page boards, with reduced motion, or without scroll timelines, it is simply full. POL_RADIATE = False puts
# the sphere back in the stage's ground, still.
POL_RADIATE = True
POL_RADIATE_FROM = 0.45


def pol_glow_layer(mobile):
    r = POL_GLOW_R['m' if mobile else 'd']
    stops = ', '.join(f'{c} {round(f * r, 1):g}px' for f, c in POL_GLOW_STOPS)
    top = '390px' if (mobile and BOXES) else '50%'
    return (f'<div class="me-pol-glow" aria-hidden="true" style="position: absolute; left: 50%; top: {top}; width: {2 * r}px; '
            f'height: {2 * r}px; margin: -{r}px 0 0 -{r}px; pointer-events: none; '
            f'background: radial-gradient(circle at 50% 50%, {stops});"></div>\n')


def pol_vh(mobile):
    return 844 if mobile else 900


def pol_pin(mobile):
    return round(POL['pin'] * pol_vh(mobile))


def pol_css(mobile):
    """The prototype's focus pull (appended to its scroll CSS). The section's own view timeline sets --in once the
    stage is most of the way up; the words hold their haze until then (and keep their focus after, however the page
    is scrolled)."""
    trig = round(POL['focus_at'] * pol_vh(mobile))
    ease = 'cubic-bezier(0.33,1,0.68,1)'
    rad0 = rad1 = ''
    if POL_GLOW and POL_RADIATE:   # V112: the sphere waits small, then opens with the headline's focus
        rad0 = f'.me-pol-glow{{transform:scale({POL_RADIATE_FROM:g});transition:transform 0s linear 99999s}}'
        rad1 = f'.me-pol-glow{{transition:transform {POL["dur"]}s {ease}}}'
    return ('@supports (animation-timeline: view()){\n'
            f'.me-pol{{--in:0;animation:me-in linear forwards;animation-timeline:--ch-pol;animation-range:cover {trig}px cover 100%}}\n'
            '@media (prefers-reduced-motion: no-preference){\n'
            f'@container style(--in: 0){{.me-pol-focus{{filter:blur({POL["blur"]});opacity:{POL["haze"]:g};transform:scale(1.035);'
            f'transition:filter 0s linear 99999s,opacity 0s linear 99999s,transform 0s linear 99999s}}{rad0}}}\n'
            f'@container style(--in: 1){{.me-pol-focus{{transition:filter {POL["dur"]}s {ease},opacity {POL["dur"] * 0.6:g}s ease-out,transform {POL["dur"]}s {ease}}}'
            f'.me-pol-focus-2{{transition-delay:{POL["lag"]}s}}{rad1}}}\n'
            '}\n}\n')


if POLICY_FX and POL_GLOW:
    HOME_CSS += ('.me-pol{--accent:#141414;--caret:#141414;--pol-text:rgba(20,20,20,0.85);--pol-muted:rgba(20,20,20,0.58);color:#141414}\n'
                 '.me-pol-focus{transform-origin:50% 50%}\n'
                 '.me-footseam{display:none}' + ('.me-dark .me-footseam{display:block}' if DARK_MODE else '') + '\n')
elif POLICY_FX:
    HOME_CSS += ('.me-pol{--pol-blue:var(--fbg);--accent:var(--ffg);--pol-text:color-mix(in srgb,var(--ffg) 85%,transparent);'
                 '--pol-muted:color-mix(in srgb,var(--ffg) 58%,transparent)}\n'
                 '.me-pol-focus{transform-origin:50% 50%}\n')


def policy_stage(mobile):
    """Policy on its stage: a screen tall (the prototype lengthens the section by the pin, and the stage sticks), solid
    blue, the words centred on it in the site's headline and statement type."""
    sc = {x[0]: x for x in SCROLL}
    _, head, body, _ = sc['policy']
    k = 'm' if mobile else 'd'
    vh = pol_vh(mobile)
    h_css, b_css = H2[k], (BODY if mobile else BODY_L)
    hw, pw, pad = (350, 350, 20) if mobile else (round(span(9)), round(span(7)), 64)   # the statement in three balanced lines
    hl, _ = typed('h2', head, EMPH['policy'], f'margin: 0; max-width: {hw}px; {h_css} color: var(--pol-muted); text-wrap: balance;', cls='me-pol-hl me-pol-focus')
    if BOXES:   # V103: the paragraph in a paper box over the sphere, as the zine's quotes sit in boxes over its type
        bw, bpx, bpy, gap = (320, 16, 14, 28) if mobile else (round(span(6)), 32, 24, 40)
        para = (f'<div class="me-pol-focus me-pol-focus-2" style="margin-top: {gap}px; width: {bw}px; max-width: 100%; padding: {bpy}px {bpx}px {bpy - TEXT_TAIL}px; {box_css(fixed=True)}">'
                f'<p style="margin: 0; {b_css} color: var(--pol-text); text-wrap: balance;">{keep_compounds(body)}</p></div>')
    else:
        para = (f'<p class="me-pol-focus me-pol-focus-2" style="margin: {text_gap(h_css, b_css, k)}px 0 0; max-width: {pw}px; {b_css} color: var(--pol-text); text-wrap: balance;">'
                f'{keep_compounds(body)}</p>')
    radiate = POL_GLOW and POL_RADIATE
    ground = PAPER if radiate else (pol_glow(mobile) if POL_GLOW else 'var(--pol-blue)')
    return f"""<section id="policy" class="me-pol" style="position: relative; height: var(--pol-h, {vh}px);">
<div class="me-pol-stage" style="position: sticky; top: 0; height: {vh}px; overflow: clip; display: flex; align-items: center; justify-content: center; background: {ground};">
{pol_glow_layer(mobile) if radiate else ''}<div style="position: relative; box-sizing: border-box; width: 100%; padding: 0 {pad}px; display: flex; flex-direction: column; align-items: center; text-align: center;">
{hl}
{para}
</div>
</div>
</section>"""



# Scroll behaviour and the typing, in the prototype artboards only (their scroller is the timeline source).
# Typing: each character of a headline fades in (0.14 s) at its turn, --i x --dt after the headline arrives, and a
# thin caret in the text colour stands after the newest character; when the last one lands the caret blinks twice and
# goes. Paragraphs follow once the headline is most of the way through. Nothing is hidden without scroll timelines
# and style queries, and reduced-motion users get everything as is.
PROTO_CSS_T = """@keyframes me-rise{from{transform:translateY(104%)}to{transform:none}}
@keyframes me-bob{0%,100%{transform:translateY(-3px)}50%{transform:translateY(5px)}}
@keyframes me-drift{to{transform:translateY(-160px)}}
@keyframes me-fg-body{to{color:var(--fg)}}
@keyframes me-fg-paper{to{color:#EAE7E1}}
@keyframes me-fg-foot{to{color:var(--ffg)}}
@keyframes me-in{from,to{--in:1}}
@keyframes me-par{from{transform:translateY(__PAR__px)}50%,to{transform:none}}
@keyframes me-exit{to{transform:translateY(-__EXIT__px)}}
@keyframes me-type{from{opacity:0}to{opacity:1}}
@keyframes me-caret{from,to{opacity:1}}
@keyframes me-caret-end{0%,24%{opacity:1}25%,49%{opacity:0}50%,74%{opacity:1}75%,100%{opacity:0}}
.me-scroller{scroll-behavior:smooth;overscroll-behavior:contain}
.me-rise>span{display:inline-block;animation:me-rise 1.2s cubic-bezier(0.16,1,0.3,1) both}
.me-rise>span:nth-child(2){animation-delay:0.09s}
.me-cue svg{animation:me-bob 2.6s ease-in-out infinite}
.me-type .c{position:relative}
.me-type .c::after{content:"";position:absolute;top:.12em;bottom:-.04em;right:-.05em;width:max(2px,.034em);background:var(--caret);opacity:0;pointer-events:none}
@media (prefers-reduced-motion: no-preference){
.me-typeload .c{animation:me-type .14s ease-out both;animation-delay:calc(var(--t0,0ms) + var(--i) * var(--dt))}
.me-typeload .c::after{animation:me-caret linear;animation-duration:var(--dt);animation-delay:calc(var(--t0,0ms) + var(--i) * var(--dt))}
.me-typeload .c.last::after{animation-name:me-caret-end;animation-duration:2.4s}
}
@supports (animation-timeline: view()){
.me-root{timeline-scope:--ch-reel,--ch-foot}
.me-ch-reel{view-timeline-name:--ch-reel}
.me-ch-foot{view-timeline-name:--ch-foot}
.me-drift{animation:me-drift linear both;animation-timeline:scroll(nearest);animation-range:0px __VH__px}
__NAVANIM__
.me-rv{--in:0;animation:me-in linear forwards;animation-timeline:view();animation-range:cover __TRIG__px cover 100%}
.me-rv.me-plate{animation-range:cover __MAPTRIG__px cover 100%}
.me-rv.me-gal{animation-range:cover __GALTRIG__px cover 100%}
.me-par{animation:me-par linear both;animation-timeline:view();animation-range:cover 0% cover 100%}
.me-exit{animation:me-exit linear both;animation-timeline:view();animation-range:cover __EXITFROM__px cover 100%}
@media (prefers-reduced-motion: no-preference){
@container style(--in: 0){
.me-hl .c{opacity:0}
.me-fade{opacity:0;transform:translateY(16px);transition:opacity 0s linear 99999s,transform 0s linear 99999s}
.me-plate .me-ink,.me-ripples{opacity:0;transition:opacity 0s linear 99999s}
.me-dot{transform:scale(0);transition:transform 0s linear 99999s}
}
@container style(--in: 1){
.me-hl .c{animation:me-type .14s ease-out both;animation-delay:calc(var(--t0,0ms) + var(--i) * var(--dt))}
.me-hl .c::after{animation:me-caret linear;animation-duration:var(--dt);animation-delay:calc(var(--t0,0ms) + var(--i) * var(--dt))}
.me-hl .c.last::after{animation-name:me-caret-end;animation-duration:2.4s}
.me-fade{transition:opacity 1s cubic-bezier(0.16,1,0.3,1) var(--fd,.45s),transform 1s cubic-bezier(0.16,1,0.3,1) var(--fd,.45s)}
.me-plate .me-ink{transition:opacity 1s ease .05s}
.me-dot{transition:transform .7s cubic-bezier(0.34,1.56,0.64,1) .65s}
.me-ripples{transition:opacity .9s ease 1s}
}
}
}
@media (prefers-reduced-motion: reduce){
.me-rise>span,.me-cue svg,.me-drift,.me-par,.me-exit{animation:none !important}
}
"""


def proto_css(vh, navh):
    """The nav's two buttons take the colour that reads on what is under them: the text colour, paper over the reel
    panel and over Policy's blue, the footer's text colour over the footer. Each flip happens while an edge crosses
    the nav's own height. On a desktop the panel is the right half, so only the theme switch (at the right) flips
    over it. The nav has no fill, only its glass."""
    mobile = vh < 880
    nav = (NAV_ANIM_M_P if mobile else NAV_ANIM_D_P) if POLICY_FX else (NAV_ANIM_M if mobile else NAV_ANIM_D)   # V80: transparent again, so it takes the colour that reads on what is under it
    css = (PROTO_CSS_T.replace('__R__', f'cover {vh - navh}px cover {vh}px').replace('__RX__', f'cover calc(100% - {navh}px) cover 100%')
            .replace('__MAPTRIG__', str(round(vh * 0.06)))
            .replace('__GALTRIG__', str(round(vh * 0.3)))
            .replace('__SNAP__', 'linear(0,0 44%,1 56%,1)').replace('__TRIG__', str(round(vh * 0.16)))
            .replace('__PAR__', '18' if mobile else '40').replace('__EXIT__', '32' if mobile else '56')
            .replace('__EXITFROM__', str(round(vh * 0.8))).replace('__VH__', str(vh))
            .replace('__NAVANIM__', nav)
            .replace('__R__', f'cover {vh - navh}px cover {vh}px').replace('__RX__', f'cover calc(100% - {navh}px) cover 100%')
            .replace('__SNAP__', 'linear(0,0 44%,1 56%,1)'))
    tl = '--ch-pol' if POLICY_FX else '--ch-foot'
    if POLICY_FX and POL_GLOW:
        css = '@keyframes me-fg-ink{to{color:#141414}}\n' + css
    if GLASS_V110:   # V110: and the veil's colour band rides on the reel panel's edges (see glass_v110)
      gh = GLASS['m' if mobile else 'd']['h']
      pos = (lambda y: f'0 {y}px') if mobile else (lambda y: f'0 0,0 {y}px')
      css += ('@keyframes me-veil-out{to{opacity:0}}\n'
            f'@keyframes me-smoke-in{{to{{background-position:{pos(-gh)}}}}}\n@keyframes me-smoke-out{{to{{background-position:{pos(-2 * gh)}}}}}\n'
            '@supports (animation-timeline: view()){\n'
            '.me-nav .me-veil{animation-name:me-veil-out,me-smoke-in,me-smoke-out;animation-duration:auto;animation-fill-mode:both;'
            f'animation-timing-function:linear;animation-timeline:{tl},--ch-reel,--ch-reel;'
            f'animation-range:cover {vh - GLASS["m" if mobile else "d"]["veil"][2]}px cover {vh - navh // 3}px,'
            f'cover {vh - gh}px cover {vh}px,cover calc(100% - {gh}px) cover 100%}}\n}}\n')
    else:   # V98: the glass and its veil are back (V79 took them out)
      css += ('@keyframes me-veil-out{to{opacity:0}}\n@supports (animation-timeline: view()){\n'
            f'.me-nav .me-veil{{animation-name:me-veil-out;animation-duration:auto;animation-fill-mode:both;animation-timing-function:linear;'
            f'animation-timeline:{tl};animation-range:cover {vh - GLASS["m" if mobile else "d"]["veil"][2]}px cover {vh - navh // 3}px}}\n}}\n')
    if POLICY_FX:
        css = (f'.me-pol{{--pol-h:{vh + pol_pin(mobile)}px}}\n'
               + css.replace('__RP__', '__R__').replace('__R__', f'cover {vh - navh}px cover {vh}px')
                    .replace('.me-root{timeline-scope:--ch-reel,--ch-foot}',
                             '.me-root{timeline-scope:--ch-reel,--ch-foot,--ch-pol}\n.me-pol{view-timeline-name:--ch-pol}')
               + pol_css(mobile))
    if NAV_V106:
        css += navname_proto(mobile, vh, navh)
    if CUE_GLOW:   # V112: the arrow's glow recedes into it as the page leaves the hero
        css += ('@keyframes me-cue-recede{0%{transform:none;opacity:1;animation-timing-function:cubic-bezier(.45,0,.55,1)}'
                '100%{transform:scale(.15);opacity:0}}\n'
                '@supports (animation-timeline: scroll()){\n'
                f'.me-cueglow{{animation:me-cue-recede linear both;animation-timeline:scroll(nearest);animation-range:0px {round(vh * CUE_RECEDE)}px}}\n}}\n'
                '@media (prefers-reduced-motion: reduce){.me-cueglow{animation:none !important}}\n')
    return css


def navname_proto(mobile, vh=None, navh=None):
    """V106, Home's prototype: the nav's name is hidden while the hero's name is on screen. Once the hero's name has
    passed under the nav (the scroller past NAVNAME_AT), its two words rise into their masks, as the hero's rose when
    the page opened (0.9 s, the second word 0.06 s behind); scrolling back, they drop away (0.3 s) and the link goes
    out of reach. With reduced motion it simply appears and goes; without scroll timelines it stays. V111: not until
    the Work chapter's rule reaches the nav's foot (see NAVNAME_LATE)."""
    k = 'm' if mobile else 'd'
    at = vh + FIRST_CH_TOP[k] - navh if NAVNAME_LATE else NAVNAME_AT[k]
    # V107: the hero's own rise (its duration, easing and lag; the masks are a line deep, so 104% clears them)
    down, rise, lag = ('104%', '1.2s cubic-bezier(0.16,1,0.3,1)', '.09s') if WORDMARK else ('150%', '.9s cubic-bezier(0.16,1,0.3,1)', '.06s')
    return ('@supports (animation-timeline: scroll()){\n'
            f'.me-navhome{{--in:0;animation:me-in linear forwards;animation-timeline:scroll(nearest);animation-range:{at}px {at + 1}px}}\n'
            '@container style(--in: 0){.me-navhome .me-navname{visibility:hidden;transition:visibility 0s linear .3s}'
            f'.me-navhome .me-nw{{transform:translateY({down});transition:transform .3s cubic-bezier(.4,0,1,1)}}}}\n'
            '@container style(--in: 1){.me-navhome .me-navname{visibility:visible}'
            f'.me-navhome .me-nw{{transform:none;transition:transform {rise}}}'
            f'.me-navhome .me-nmask+.me-nmask .me-nw{{transition-delay:{lag}}}}}\n'
            '}\n'
            '@supports not (animation-timeline: scroll()){.me-navhome .me-navname{visibility:visible}}\n'
            '@media (prefers-reduced-motion: reduce){.me-navhome .me-nw{transition:none !important;transform:none !important}}\n')


_FLIPS = ('animation-duration:auto;animation-fill-mode:both;animation-name:me-fg-paper,me-fg-body,me-fg-foot;animation-timing-function:__SNAP__;'
          'animation-timeline:--ch-reel,--ch-reel,--ch-foot;animation-range:__R__,__RX__,__R__')
_FOOT = ('animation-duration:auto;animation-fill-mode:both;animation-name:me-fg-foot;animation-timing-function:__SNAP__;'
         'animation-timeline:--ch-foot;animation-range:__R__')
NAV_ANIM_D = '.me-nav{' + _FOOT + '}\n.me-nav .me-navr{' + _FLIPS + '}'


NAV_ANIM_M = '.me-nav{' + _FLIPS + '}'
# With Policy's stage, both buttons also go over to paper (the words' colour) once the blue lies under them; the
# footer's own flip follows.
_FLIPS_P = ('animation-duration:auto;animation-fill-mode:both;animation-name:me-fg-paper,me-fg-body,me-fg-foot,me-fg-foot;'
            'animation-timing-function:__SNAP__;animation-timeline:--ch-reel,--ch-reel,--ch-pol,--ch-foot;animation-range:__R__,__RX__,__RP__,__R__')
_FOOT_P = ('animation-duration:auto;animation-fill-mode:both;animation-name:me-fg-foot,me-fg-foot;animation-timing-function:__SNAP__;'
           'animation-timeline:--ch-pol,--ch-foot;animation-range:__RP__,__R__')
if POL_GLOW:   # V102: over the stage the nav goes ink (it is paper in both themes), then the footer's flip
    _FLIPS_P = _FLIPS_P.replace('me-fg-body,me-fg-foot,me-fg-foot', 'me-fg-body,me-fg-ink,me-fg-foot')
    _FOOT_P = _FOOT_P.replace('animation-name:me-fg-foot,me-fg-foot', 'animation-name:me-fg-ink,me-fg-foot')
NAV_ANIM_D_P = '.me-nav{' + _FOOT_P + '}\n.me-nav .me-navr{' + _FLIPS_P + '}'
NAV_ANIM_M_P = '.me-nav{' + _FLIPS_P + '}'


FONT_FACES = (
    "@font-face{font-family:'Neue Montreal';src:url('%s') format('woff2');font-weight:400;font-style:normal;font-display:swap}\n"
    "@font-face{font-family:'Neue Montreal';src:url('%s') format('woff2');font-weight:400;font-style:italic;font-display:swap}\n"
) % (BLOB['font'], BLOB['font-italic'])
# V78: Writer, and the `headlines` switch (in every board's helmet, components too, so an imported footer follows
# its page): under `.me-sans` each serif headline takes back Neue Montreal and its own tracking, leading and indent.
# The typing caret spans the same height in either face (its box is the face's ascent and descent).
SERIF_CSS = ''
if SERIF:
    FONT_FACES += ("@font-face{font-family:'PP Writer';src:url('%s') format('woff2');font-weight:400;font-style:normal;font-display:swap}\n"
                   % BLOB['writer'])
    SERIF_CSS = (".me-sans .me-hs{font-family:'Neue Montreal',Helvetica,Arial,sans-serif !important;letter-spacing:var(--ls-sans) !important;"
                 "line-height:var(--lh-sans) !important;text-indent:var(--ti-sans,0) !important}\n"
                 ".me-type.me-hs .c::after{top:.21em;bottom:.06em}\n"
                 ".me-sans .me-type.me-hs .c::after{top:.12em;bottom:-.04em}\n")


def mark_serif(t):
    """Every element whose style sets a serif headline role (it carries --ls-sans) takes the class `me-hs`."""
    def rep(m):
        tag = m.group(0)
        return tag.replace(' class="', ' class="me-hs ', 1) if ' class="' in tag else tag.replace(' style="', ' class="me-hs" style="', 1)
    return re.sub(r'<[a-z][a-z0-9]*\s[^>]*style="[^"]*--ls-sans[^"]*"[^>]*>', rep, t)


def helmet(imported=False, proto=None, extra_css=''):
    css = FONT_FACES + 'body{margin:0}\n' + SERIF_CSS
    if not imported:
        css += PAGE_CSS + extra_css
    elif extra_css:
        css += extra_css
    if proto:
        css += proto_css(*proto)
    return f"<helmet>\n<style>\n{css}</style>\n</helmet>"


def dc(title, body, w, h, props=None, script=None, imported=False, proto=None, extra_css=''):
    props = dict(props or {})
    props['$preview'] = {'width': w, 'height': h}
    pj = json.dumps(props, ensure_ascii=False).replace('&', '&amp;').replace("'", '&#39;')
    script = script or "class Component extends DCLogic {\nrenderVals() {\nreturn {};\n}\n}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{helmet(imported, proto, extra_css)}
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{pj}'>
{script}
</script>
</body>
</html>
"""


FILES = {}


def write(name, text):
    if SERIF:
        text = mark_serif(text)
    FILES[name] = text
    with open(os.path.join(P, name), 'w', encoding='utf-8') as f:
        f.write(text)


def hcss(name, default):
    return 'height: auto;' if MEASURE else f'height: {HEIGHTS.get(name, default)}px;'


def hval(name, default):
    return HEIGHTS.get(name, default)


# ── Page logic ───────────────────────────────────────────────────────────────────────────────────────────────
# Every page keeps its theme and whether its menu is open. The theme starts from the `theme` tweak (light unless set)
# and the switch flips it; handlers are made once, so children see stable props.
def page_script(rail=False, reel=False):
    parts = ["""class Component extends DCLogic {
renderVals() {
const s = this.state || {};
const dark = s.dark ?? (this.props.theme === 'dark');
if (!this._h) {
const isDark = () => { const t = this.state || {}; return t.dark ?? (this.props.theme === 'dark'); };
this._h = {
toggleTheme: () => this.setState({ dark: !isDark() }),
openMenu: () => this.setState({ menu: true }),
closeMenu: () => this.setState({ menu: false }),
};""" if DARK_MODE else """class Component extends DCLogic {
renderVals() {
const s = this.state || {};
if (!this._h) {
this._h = {
openMenu: () => this.setState({ menu: true }),
closeMenu: () => this.setState({ menu: false }),
};"""]
    if rail:
        parts.append("""const rail = (e) => e.currentTarget.closest('section').querySelector('.me-rail');
const page = (e, dir) => { const el = rail(e); if (el) el.scrollBy({ left: dir * (el.clientWidth + 24), behavior: 'smooth' }); };
this._h.railPrev = (e) => page(e, -1);
this._h.railNext = (e) => page(e, 1);
this._h.railScroll = (e) => {
const el = e.currentTarget, cur = this.state || {};
const atStart = el.scrollLeft < 8, atEnd = el.scrollLeft > el.scrollWidth - el.clientWidth - 8;
if (atStart !== (cur.atStart ?? true) || atEnd !== (cur.atEnd ?? false)) this.setState({ atStart, atEnd });
};""")
    if reel:
        # The reel plays muted and looped while it is on screen; the ring over it pauses it (and a reduced-motion
        # setting leaves it paused on its first frame until played).
        parts.append("""const play = (v) => { const q = v.play(); if (q && q.catch) q.catch(() => {}); };
this._h.reelRef = (el) => {
if (!el || el === this._reel) return;
this._reel = el;
el.muted = true;
const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if (reduce) { el.pause(); this._userPaused = true; if (!(this.state || {}).reelPaused) this.setState({ reelPaused: true }); return; }
play(el);
if ('IntersectionObserver' in window) {
this._io = new IntersectionObserver((entries) => { for (const en of entries) { if (this._userPaused) continue; if (en.isIntersecting) play(el); else el.pause(); } }, { threshold: 0.1 });
this._io.observe(el);
}
};
this._h.toggleReel = () => {
const v = this._reel; if (!v) return;
if (v.paused) { this._userPaused = false; play(v); this.setState({ reelPaused: false }); }
else { this._userPaused = true; v.pause(); this.setState({ reelPaused: true }); }
};""")
    parts.append("""}""")
    if DARK_MODE:
        parts.append("""return {
dark, themeCls: (dark ? 'me-dark' : '') + (this.props.headlines === 'sans' ? ' me-sans' : ''),""" if SERIF else """return {
dark, themeCls: dark ? 'me-dark' : '',""")
        parts.append("""menuOpen: !!s.menu, menuCls: s.menu ? 'is-open' : '',
toggleTheme: this._h.toggleTheme, openMenu: this._h.openMenu, closeMenu: this._h.closeMenu,""")
    else:   # V115
        parts.append("""return {
themeCls: this.props.headlines === 'sans' ? 'me-sans' : '',""" if SERIF else """return {""")
        parts.append("""menuOpen: !!s.menu, menuCls: s.menu ? 'is-open' : '',
openMenu: this._h.openMenu, closeMenu: this._h.closeMenu,""")
    if rail:
        parts.append("""atStart: s.atStart ?? true, atEnd: s.atEnd ?? false,
railPrev: this._h.railPrev, railNext: this._h.railNext, railScroll: this._h.railScroll,""")
    if reel:
        parts.append("""reelRef: this._h.reelRef, toggleReel: this._h.toggleReel,
reelCls: s.reelPaused ? 'is-paused' : '', reelLabel: s.reelPaused ? 'Play the reel' : 'Pause the reel',""")
    parts.append("""};
}""")
    parts.append("""componentWillUnmount() { if (this._io) this._io.disconnect(); }
}""")
    return '\n'.join(parts)


THEME_PROP = {'theme': {'editor': 'enum', 'options': ['light', 'dark'], 'default': 'light'}} if DARK_MODE else {}
MENU_PROP = dict(THEME_PROP)       # the open menu has no headlines (its items stay in Neue Montreal)
HL_PROP = {'headlines': {'editor': 'enum', 'options': ['serif', 'sans'], 'default': 'serif'}} if SERIF else {}
THEME_PROP = {**THEME_PROP, **HL_PROP}
# Boards that only show another (the dark previews) or stand alone (the footer): the tweak's value, and the class.
HL_SCRIPT = """class Component extends DCLogic {
renderVals() {
const sans = this.props.headlines === 'sans';
return { headlines: sans ? 'sans' : 'serif', hlCls: sans ? 'me-sans' : '' };
}
}"""

# ── Icons and buttons ────────────────────────────────────────────────────────────────────────────────────────
THEME_ICON = ('<svg class="me-themeicon" width="14" height="14" viewBox="0 0 14 14" aria-hidden="true">'
              '<circle cx="7" cy="7" r="7" fill="currentColor"></circle></svg>')
BAR = '<span style="display: block; height: 1.5px; width: 100%; background: currentColor;"></span>'
BARS = f'<span style="display: flex; flex-direction: column; justify-content: space-between; width: 18px; height: 11px;">{BAR}{BAR}{BAR}</span>'
CLOSE_X = ('<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" '
           'aria-hidden="true"><path d="M5 5l14 14"></path><path d="M19 5 5 19"></path></svg>')
ARROW_DOWN = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v16"></path><path d="M5.5 13.5 12 20l6.5-6.5"></path></svg>')
ARROW_RIGHT = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
               'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12h16"></path><path d="M13.5 5.5 20 12l-6.5 6.5"></path></svg>')
ARROW_LEFT = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
              'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 12H4"></path><path d="M10.5 5.5 4 12l6.5 6.5"></path></svg>')
ARROW_UPRIGHT = ('<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
                 'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7"></path><path d="M8.5 7H17v8.5"></path></svg>')
ICON_PAUSE = ('<svg class="me-ico-pause" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">'
              '<rect x="4" y="3" width="2.25" height="10" fill="currentColor"></rect><rect x="9.75" y="3" width="2.25" height="10" fill="currentColor"></rect></svg>')
ICON_PLAY = ('<svg class="me-ico-play" width="16" height="16" viewBox="0 0 16 16" aria-hidden="true">'
             '<path d="M5 3.2v9.6L12.6 8z" fill="currentColor"></path></svg>')


# The nav: the menu at the left, the theme switch (a solid disc in the text colour) at the right, each on a glass
# disc whose edge meets the page margin (V67; bare, each icon's ink met it); the menu's close takes the menu button's
# place.
def theme_btn(handler='toggleTheme'):
    cls, st = btn_look('right')
    return (f'<button type="button" class="me-iconbtn me-navr{cls}" data-act="theme" aria-label="Dark mode" aria-pressed="{{{{ dark }}}}" '
            f'onClick="{{{{ {handler} }}}}"{st}>{THEME_ICON}</button>')


def menu_btn(handler='openMenu'):
    cls, st = btn_look('left')
    return (f'<button type="button" class="me-iconbtn{cls}" data-act="menu" aria-label="Menu" aria-controls="menu" aria-expanded="{{{{ menuOpen }}}}" '
            f'onClick="{{{{ {handler} }}}}"{st}>{BARS}</button>')


def close_btn():
    cls, st = btn_look('left')
    if NAV_V106:   # where the menu button now is, at the right
        st = ' style="margin-right: -13px;"'
    return (f'<button type="button" class="me-iconbtn{cls}" data-act="close" aria-label="Close menu" onClick="{{{{ closeMenu }}}}"{st}>{CLOSE_X}</button>')


# V106 (Mig): the nav is his name at the left and the menu at the right; the theme switch leaves the nav for the menu.
# The name is the way home: on every page and in the open menu it stands at the left in small capitals (15px, so its
# capitals stand as tall as the menu's three bars, 11px, and centre on the same line); on Home it is hidden while the
# hero's own name is on screen, and rises into place, as the hero's name rose when the page opened, once that name
# has passed under the nav (it drops away again on the way back up); there it leads to the hero. The menu button's
# bars (and the close cross that replaces them) meet the right margin. In the menu, under its list, a row holds the
# switch: "Dark mode" and a track whose knob crosses to the right and lights up cyan when the dark theme is on.
# NAV_V106 = False puts V105's nav back (the menu at the left, the disc at the right).
NAV_V106 = True
NAVNAME_CSS = "font-size: 15px; line-height: 1; letter-spacing: 0.05em; text-transform: uppercase; font-feature-settings: 'case';"
NAVNAME_AT = {'d': 712, 'm': 666}   # Home's prototype: the scroll offset (px) at which the hero's name is all but under the nav (its foot 24px from the top)
# V111 (Mig): the name comes in only well after the hero's name has gone, not while it is still frosting over under
# the glass: when the Work chapter's heavy rule reaches the foot of the nav (the hero is a screen tall and the rule
# lies FIRST_CH_TOP below it), so 974px on a desktop and 870px on a phone, by which time the hero's name is some 270px
# (200px) off the top of the screen. NAVNAME_LATE = False puts NAVNAME_AT back.
NAVNAME_LATE = True
# V107 (Mig): the nav's name is the hero's name in small, set as a wordmark: the same capitals, tracking (-0.03em),
# space between the words (0.2em) and leading (0.86); on one line on a desktop and stacked on a phone, as the hero
# sets it. It stays 15px, its capitals as tall as the menu's bars and centred on them. On hover it dims, as a mark
# does, rather than taking an underline. It rises as the hero's name rose when the page opened (1.2 s, the second word
# 0.09 s behind). WORDMARK = False puts V106's setting back (open tracking, a word space, one line everywhere).
WORDMARK = True
if WORDMARK:
    NAVNAME_CSS = 'font-size: 15px; line-height: 0.86; letter-spacing: -0.03em;'
# V108 (Mig): one line everywhere, phones included; only the hero's spacing carries over (WORDMARK_STACK = True puts
# V107's stacked phone mark back).
WORDMARK_STACK = False


def nav_name(href, close=False, hidden_on_hero=False, mobile=False):
    """The name, a link home. Each word sits in its own mask so it can rise into place (on Home)."""
    shut = ' onClick="{{ closeMenu }}"' if close else ''
    if WORDMARK:   # V107: the hero's words and setting (its capitals as written, its name for screen readers)
        words = ''.join(f'<span class="me-nmask"><span class="me-nw">{w}</span></span>' for w in NAME)
        flow = 'flex-direction: column;' if (mobile and WORDMARK_STACK) else 'gap: 0.2em;'
        # centred on the bars by eye: with its box centred, the capitals' ink sits a pixel above the bars' middle (the
        # face's ascent outweighs its descent at this leading), so the mark drops a pixel
        a = (f'<a class="me-navname" href="{href}" aria-label="Miguel Escobar"{shut} style="position: relative; top: 1px; display: flex; {flow} {NAVNAME_CSS} '
             f'white-space: nowrap; {NOUL}">{words}</a>')
        return f'<div class="me-navhome">{a}</div>' if hidden_on_hero else a
    words = ' '.join(f'<span class="me-nmask"><span class="me-nw">{w}</span></span>' for w in ('Miguel', 'Escobar'))
    a = (f'<a class="me-navname" href="{href}"{shut} style="display: block; {NAVNAME_CSS} white-space: nowrap; {NOUL}">{words}</a>')
    return f'<div class="me-navhome">{a}</div>' if hidden_on_hero else a


def menu_btn_right(handler='openMenu'):
    """The menu button at the right: its bars' ink on the margin; it takes the right-hand button's colour turns."""
    return (f'<button type="button" class="me-iconbtn me-navr" data-act="menu" aria-label="Menu" aria-controls="menu" aria-expanded="{{{{ menuOpen }}}}" '
            f'onClick="{{{{ {handler} }}}}" style="margin-right: -13px;">{BARS}</button>')


# V109 (Mig): the switch alone, no words, at the right just above the list's heavy rule: its track stands as far above
# the rule as an item's words stand below it (20px; 14px on a phone). Its name, for screen readers, is "Dark mode";
# its hit area is the 44px square the other buttons have. MENU_SWITCH_TOP = False puts V108's last row back.
MENU_SWITCH_TOP = True


def theme_switch_top(mobile):
    gap = 14 if mobile else 20
    return (f'<div style="display: flex; justify-content: flex-end; margin-bottom: {gap}px;">'
            f'<button type="button" class="me-switch" role="switch" data-act="theme" aria-label="Dark mode" aria-checked="{{{{ dark }}}}" '
            f'onClick="{{{{ toggleTheme }}}}" style="width: auto; padding: 10px 0; margin: -10px 0;">'
            f'<span class="me-switch-track" aria-hidden="true"><span class="me-switch-knob"></span></span></button></div>')


def theme_switch(mobile):
    """The menu's last row: the theme as a switch (role switch, its state the theme's)."""
    fs, pad = (19, 16) if mobile else (22, 20)
    return (f'<button type="button" class="me-switch" role="switch" data-act="theme" aria-checked="{{{{ dark }}}}" onClick="{{{{ toggleTheme }}}}" '
            f'style="padding: {pad}px 0; font-size: {fs}px; line-height: 1.3; letter-spacing: 0.005em;">'
            f'<span>Dark mode</span><span class="me-switch-track" aria-hidden="true"><span class="me-switch-knob"></span></span></button>')


NAVNAME_RULES = (
    # the name: its words underlined on hover (each word is its own box, so each takes its own line); the masks run
    # deep enough below the words to show it
    '.me-nmask{display:inline-block;vertical-align:top;overflow:clip;padding-bottom:6px;margin-bottom:-6px}\n'
    '.me-nw{display:inline-block}\n'
    'a.me-navname:hover .me-nw{text-decoration-line:underline;text-decoration-thickness:1px;text-underline-offset:4px}\n')
SWITCH_RULES = (
    # the switch: a 44 x 24 track on a hairline in the text colour, its knob in the text colour; in the dark theme the
    # knob crosses to the right and the track fills with the accent (ink knob on it)
    '.me-switch{display:flex;align-items:center;justify-content:space-between;gap:24px;width:100%;margin:0;border:0;background:transparent;'
    'color:inherit;font-family:inherit;text-align:left;cursor:pointer;-webkit-tap-highlight-color:transparent}\n'
    '.me-switch-track{position:relative;flex-shrink:0;width:44px;height:24px;box-sizing:border-box;border:1px solid currentColor;border-radius:12px;'
    'transition:background-color .3s ease,border-color .3s ease}\n'
    '.me-switch-knob{position:absolute;left:3px;top:3px;width:16px;height:16px;border-radius:50%;background:currentColor;'
    'transition:transform .45s cubic-bezier(0.16,1,0.3,1),background-color .3s ease}\n'
    '.me-dark .me-switch-track{background:__CYAN__;border-color:__CYAN__}\n'
    '.me-dark .me-switch-knob{transform:translateX(20px);background:#141414}\n'
    '@media (prefers-reduced-motion: reduce){.me-switch-track,.me-switch-knob{transition:none}}\n')
if WORDMARK:   # V107
    NAVNAME_RULES = ('.me-nmask{display:block;overflow-x:visible;overflow-y:clip}\n'
                     '.me-nw{display:block}\n'
                     'a.me-navname{transition:opacity .25s ease}\n'
                     'a.me-navname:hover{opacity:.6}\n')
NAV_V106_CSS = NAVNAME_RULES + (SWITCH_RULES if DARK_MODE else '')


# ── Links ────────────────────────────────────────────────────────────────────────────────────────────────────
# V69: Editorial Work and Advertising Work are one page, Work; the old keys (home's links, the rail's cards) lead to it.
D_LINKS = dict(home='NewHomePlay.dc.html', Work='NewWork.dc.html', AdvertisingWork='NewWork.dc.html', EditorialWork='NewWork.dc.html',
               Thoughts='NewThoughts.dc.html', ThoughtPost='NewThoughtPost.dc.html')
M_LINKS = dict(home='NewHomeMobilePlay.dc.html', Work='NewWorkMobile.dc.html', AdvertisingWork='NewWorkMobile.dc.html', EditorialWork='NewWorkMobile.dc.html',
               Thoughts='NewThoughtsMobile.dc.html', ThoughtPost='NewThoughtPostMobile.dc.html')
MENU_ITEMS = [('Home', 'home'), ('Work', 'Work'), ('Thoughts', 'Thoughts'), ('Contact', '#contact')]


def nbdash(text):
    """A spaced em dash stays on the line of the word before it, so no line starts with a dash."""
    return text.replace(' — ', ' — ')


def keep_compounds(text):
    """Hyphenated compounds never split across lines; nor does a dash from its word. Only text between tags is touched."""
    wrap = lambda t: re.sub(r'([^\s<>]+-[^\s<>]+)', r'<span style="white-space: nowrap;">\1</span>', nbdash(t))
    return ''.join(part if part.startswith('<') else wrap(part) for part in re.split(r'(<[^>]+>)', text))


def link_list(items, footer, size, pad, label, arrow_px):
    """Every group of links is the same component: rows on hairlines under a heavy rule, label left, arrow at the right
    edge (up-right for links that leave the site, right for pages on it)."""
    rule, heavy = (C['frule'], C['ffg']) if footer else (C['rule'], C['fg'])
    rows = []
    for href, text in items:
        ext = not href.endswith('.dc.html') and not href.startswith('#')
        attrs = f'href="{href}"' + (' target="_blank" rel="noopener"' if href.startswith('http') else '')
        arrow = (ARROW_UPRIGHT if ext else ARROW_RIGHT).format(s=arrow_px)
        rows.append(f'<a class="lrow{" ext" if ext else ""}" {attrs} style="display: flex; align-items: center; justify-content: space-between; gap: 24px; '
                    f'padding: {pad}px 0; border-bottom: 1px solid {rule}; font-size: {size}px; line-height: 1.3; letter-spacing: 0.005em; {NOUL}">'
                    f'<span class="lrow-label">{text}</span><span class="lrow-arrow" style="display: flex; flex-shrink: 0; opacity: 0.6;">{arrow}</span></a>')
    return f'<nav aria-label="{label}" style="display: flex; flex-direction: column; border-top: {HEAVY}px solid {heavy};">\n' + '\n'.join(rows) + '\n</nav>'


def more_link(href, label, size, circle):
    """Work link: label plus the arrow in a ring."""
    return (f'<a class="me-link" href="{href}" style="display: inline-flex; align-items: center; gap: {circle // 3}px; '
            f'font-size: {size}px; line-height: 1.3; letter-spacing: 0.005em; {NOUL}">'
            f'<span class="me-link-label">{label}</span>'
            f'<span class="me-ring" style="display: flex; flex-shrink: 0; align-items: center; justify-content: center; width: {circle}px; height: {circle}px; '
            f'box-sizing: border-box; border: 1px solid {C["ring"]}; border-radius: 50%;">'
            f'<span class="me-arrow" style="display: flex;">{ARROW_RIGHT.format(s=round(circle * 0.38))}</span></span></a>')


def heavy_rule(mobile, extra=''):
    return f'<div aria-hidden="true" style="{extra}border-top: {HEAVY}px solid {C["fg"]}; margin-bottom: {HEAD_GAP["m" if mobile else "d"]}px;"></div>'


# ── Typing ───────────────────────────────────────────────────────────────────────────────────────────────────
EMPH = {'about': 'Singapore', 'editorial': 'editorial background', 'branded': 'branded content',
        'policy': 'content policy and online safety', 'work': 'honest helpful human storytelling'}
EM_TAKES_STOP = True   # tonal emphasis (see type_chars); set False when the accent is a colour again


def typing_dt(n):
    """Milliseconds per character: a headline types in about 1.4 s, never faster than 18 ms or slower than 34 ms a
    character."""
    return max(18, min(34, round(1400 / n)))


def type_chars(text, emph=''):
    """Each character in its own span, numbered in typing order (--i), inside word spans that keep words whole. The
    subject phrase takes the accent (for now, the full text colour against a quieter lead-in), and the full stop
    after it goes with it: a pale stop after full-strength words would read as a gap. (With a colour accent, the
    stop would keep the text colour instead.)"""
    words = text.split(' ')
    ew = [w for w in re.sub(r'[,]', '', emph).split(' ') if w] if emph else []
    bare = [re.sub(r'[.,]$', '', w) for w in words]
    start = next((i for i in range(len(words) - len(ew) + 1) if bare[i:i + len(ew)] == ew), -1) if ew else -1
    assert not ew or start >= 0, (text, emph)
    total = sum(len(w) for w in words)
    k = [0]

    def spans(s):
        out = ''
        for ch in s:
            k[0] += 1
            out += f'<span class="c{" last" if k[0] == total else ""}" style="--i: {k[0] - 1};">{html.escape(ch, quote=False)}</span>'
        return out
    out = []
    for i, w in enumerate(words):
        if ew and start <= i < start + len(ew):
            core, punct = re.match(r'^(.*?)([.,]?)$', w).groups()
            if i < start + len(ew) - 1 or (EM_TAKES_STOP and punct == '.'):   # a comma inside the phrase belongs to it
                core, punct = w, ''
            inner = f'<span class="me-em">{spans(core)}</span>' + spans(punct)
        else:
            inner = spans(w)
        out.append(f'<span class="w">{inner}</span>')
    binds = set()    # word i is held to word i + 1
    if 1 < len(ew) <= 2 and len(' '.join(ew)) <= 16:   # a short pair stays on one line ("branded content"); a long
        # one ("editorial background") may break, or a phone's column strands the words either side of it
        binds |= set(range(start, start + len(ew) - 1))
    if HOLD_ARTICLES:   # an article never ends a headline's line
        binds |= {i for i, w in enumerate(bare[:-1]) if w.lower() in ARTICLES}
    groups = [[out[0]]]
    for i in range(1, len(out)):
        if i - 1 in binds:
            groups[-1].append(out[i])
        else:
            groups.append([out[i]])
    out = [g[0] if len(g) == 1 else '<span style="white-space: nowrap;">' + ' '.join(g) + '</span>' for g in groups]
    return ' '.join(out), total


def typed(tag, text, emph, style, cls='me-hl', t0=0):
    """A typed line: the characters for sighted readers, the plain text for screen readers. A line with a subject
    phrase is two-tone: the rest of it in the quieter text colour."""
    if emph and 'color:' not in style:
        style += f' color: {C["muted"]};'
    chars, n = type_chars(text, emph)
    dt = typing_dt(n)
    t0s = f' --t0: {t0}ms;' if t0 else ''
    return (f'<{tag} class="me-type {cls}" style="{style} --dt: {dt}ms;{t0s}"><span class="me-sr">{html.escape(text, quote=False)}</span>'
            f'<span aria-hidden="true">{chars}</span></{tag}>'), n * dt


def fade_delay(ms):
    """A paragraph starts to fade in once its headline is 60% typed."""
    return f' --fd: {round(ms * 0.6)}ms;'


# ── Map ──────────────────────────────────────────────────────────────────────────────────────────────────────
MAP = {'d': json.load(open(os.path.join(SCR, 'map', 'map_ee_d.json'))),      # 731 x 357, the desktop map
       'm': json.load(open(os.path.join(SCR, 'map', 'map_ee_m.json')))}      # 350 x 171, the phone's


def sg_map(m, mobile):
    """The world in the Equal Earth projection, centred on the Pacific (150°E) so Southeast Asia sits near the
    middle: a 15° graticule in hairlines, the land's coasts in the quieter text colour, the sphere's outline, and
    Singapore, from which rings pulse out without end across Southeast Asia (to about 3,300 km, the region's far
    ends), fading as they spread. Each size has its own drawing, made at 1 unit = 1 px. The rings' reach (--rip) and
    start (--dot) ride on their group, so one set of keyframes serves both sizes."""
    W, H, (sx, sy) = m['W'], m['H'], m['sg']
    coast, dot_r = (0.75, 2.8) if mobile else (1, 3.2)
    rings = ''.join(f'<circle class="me-ripple" cx="{sx}" cy="{sy}" r="0"></circle>' for _ in range(RIPPLES))
    # V105: the ping in the accent (its rings half a pixel heavier, as a light colour on paper needs)
    ping, ping_w = (CYAN, '1.5') if MAP_PING else (C['fg'], '1')
    return f"""<svg class="me-map" viewBox="0 0 {W} {H}" role="img" aria-label="World map with Singapore marked and a ripple spreading from it across Southeast Asia" style="display: block; width: 100%; height: 100%; overflow: visible;">
<g class="me-ink" fill="none" stroke-linejoin="round" stroke-linecap="round">
<path d="{m['graticule']}" stroke-width="0.75" style="stroke: {C['grid']};"></path>
<path d="{m['land']}" stroke-width="{coast}" style="stroke: {C['muted']};"></path>
<path d="{m['outline']}" stroke-width="1" style="stroke: {C['ring']};"></path>
</g>
<g class="me-ripples" fill="none" stroke-width="{ping_w}" style="stroke: {ping}; --rip: {m['ripple']}px; --dot: {dot_r}px;">{rings}</g>
<circle class="me-dot me-map-sg" cx="{sx}" cy="{sy}" r="{dot_r}" style="fill: {ping};"></circle>
</svg>"""


def plate(mobile, extra_style=''):
    """The map, unframed: the sphere's outline is its edge."""
    k = 'm' if mobile else 'd'
    return (f'<div class="me-rv me-plate" style="{extra_style}aspect-ratio: {MAP[k]["W"]} / {MAP[k]["H"]};">'
            f'{sg_map(MAP[k], mobile)}</div>')


# ── Work samples (the rail) ──────────────────────────────────────────────────────────────────────────────────
def _alts():
    alt = {key: a_ for (_, _, _, key, a_) in FEATURED + MORE}
    for entry in EDITORIAL + ADVERTISING:
        alt[entry[2]] = entry[3]
    return alt


ALT = _alts()
ALT['work-goodmen'] = 'A man in a blue shirt holds a stack of books in front of library shelves.'
ALT['work-denim'] = 'Folded raw selvedge denim stacked in front of bolts of fabric.'
ALT['ph-politics'] = 'Mocha Uson in a black coat, her mouth covered with a strip of grey tape.'
GALLERY = [('home-advertising', 50), ('home-age-checks', 50), ('home-editorial', 50), ('home-whitewash', 50),
           ('work-osc', 50), ('ads-nba', 50), ('home-pulpit', 50), ('ph-politics', 50)]   # V95: Mig's order; V96: AAM and OSC swapped
CAPTIONS = {   # V87: Mig's copy sheet
    'home-whitewash': ('Investigative Feature', 'The Wikipedians at War Over Truth'),
    'home-pulpit': ('Investigative Feature', 'Exposing Intimate Image Abuse Groups'),
    'home-editorial': ('Cover Story', 'Eddie Garcia for Esquire Philippines'),
    'ph-politics': ('Politics', 'Interviews With Controversial Figures'),   # V91: Mig's Uson portrait
    'home-advertising': ('Fintech Campaign', 'Trust Bank Singapore: Cashback Launch'),
    'ads-nba': ('Branded Newsletter', 'NBA Asia-Pacific Weeklies'),
    'work-osc': ('Public Service', 'Online Safety Commission Launch'),
    'home-age-checks': ('Public Service', 'Age Assurance Measures in App Stores'),
}
WORK_HEAD = 'My work has been about honest, helpful, human storytelling.'   # V60, Mig's revision
CARD_LINKS = {
    'home-whitewash': FEATURED[2][1],
    'home-pulpit': FEATURED[3][1],
    'home-editorial': 'https://www.youtube.com/watch?v=yY4LLYrMHt8',   # V87: the same link as the Work page's entry
    'ads-nba': None,
    'work-osc': 'https://www.osc.gov.sg/',
    'ph-politics': None,   # V88: the Work page's entry, which links the interviews themselves
    'home-advertising': 'https://www.marketing-interactive.com/trust-bank-million-dollars-campaign',
    'ads-alcon': None,
    'ads-gotyme': 'https://www.youtube.com/watch?v=MCDe-yLaxYE',
    'home-age-checks': 'https://www.youtube.com/watch?v=HXkZmhEBnBQ',
}
RAIL = {'d': dict(card=round(span(3)), gap=24, label=12, title=22, top=16, between=6, head_gap=64),
        'm': dict(card=150, gap=16, label=11, title=16, top=12, between=4, head_gap=32)}
# V103 (Mig): boxes, after the zine's boxed quotes: the page's own ground inside a 1px line in the text colour (paper
# and ink in the light theme, ink and paper in the dark), with BOX['pad'] inside. They hold the cards on Home and Work
# and Policy's paragraph (paper and ink in both themes there, as its stage is). A picture that heads a card runs to
# the box's edges (BOX['flush']); a picture beside words sits inside the padding. Cards in a row are boxes of one
# height (the rail's flex row and the grids stretch them), a gutter apart, so the hairlines that parted them go. A
# phone's rail card widens so its words have room inside the padding (one card and half the next on screen, not two
# and the edge of a third). BOXES = False puts V102 back.
BOXES = True
BOX = dict(line=1, pad={'d': 20, 'm': 12}, flush=True, gap={'d': 24, 'm': 12})
if BOXES:
    RAIL['m']['card'] = 220
    HOME_CSS += '.me-rail>.me-card.me-box::after{display:none}\n'   # no hairlines between boxed cards


# V104 (Mig): cyan is the site's accent, the zine's (its boxes, and Policy's sphere). Its first job: a box that can be
# followed lights up while the pointer is on it, as the zine's boxed quotes are lit: a band of cyan inside the line
# along the right and lower edges, fading inwards (over a picture too), and a faint halo outside them. A box whose
# links are in its words only (Trust Bank's, the political interviews, the profiles) lights while one of those is
# under the pointer; a box with no link (NBA, Alcon) never does, so the light means "this goes somewhere". Keyboard
# focus lights a box as the pointer does (the focus outline stays); on a touch screen a press does. The halo needs
# room the rail would clip, under its cards and right of its fourth on a desktop: the rail is padded there and pulled
# back by as much, so nothing moves and its pages scroll as before. GLOW = False puts V103 back.
CYAN = '#00B9E7'          # the zine's (Mig's reference samples at rgb(0, 185, 230)); a stop of Policy's sphere
CYAN_RGB = '0, 185, 231'
GLOW = False              # V112 (Mig): the hover's glow is out (True puts it back)
GLOW_ROOM = 16            # px: the rail's padding for the halo
HALO = {'light': 0.5, 'dark': 0.5}   # the halo's strength on paper and on ink


# Colour mixing in OKLab (Björn Ottosson's), so a step toward a colour is an even step to the eye.
def _s2l(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _l2s(c):
    c = max(0.0, min(1.0, c))
    return round(255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055))


def _oklab(hexc):
    r, g, b = (_s2l(int(hexc[i:i + 2], 16)) for i in (1, 3, 5))
    l, m, s = ((0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3),
               (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3),
               (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s, 1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def _hex(L, a, b):
    l, m, s = ((L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3,
               (L - 0.0894841775 * a - 1.2914855480 * b) ** 3)
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return '#' + ''.join('%02X' % _l2s(v) for v in rgb)


def ok_mix(c1, c2, t):
    """c1 moved toward c2 by t (0 to 1), in OKLab."""
    return _hex(*(x + (y - x) * t for x, y in zip(_oklab(c1), _oklab(c2))))


# V105 (Mig): the cyan moves toward his #32C7F3 across the site. That cyan has the zine's hue and nearly its chroma;
# it is lighter (OKLab L .77 to the zine's .73). The accent goes two-thirds of the way (#27C2EF), so the hover's band,
# the map's ping and selected text all take it. Policy's sphere follows a little: each stop of its core moves 40% of
# the way toward the same cyan, tapering to nothing by half the radius, so the heart lifts and loses a little of its
# blue while staying the deepest part, and the fade to paper keeps its course. A lighter cyan stands out less from
# paper and more from ink, so the hover's halo is a touch stronger on paper and a touch weaker on ink, to read as it
# did. CYAN_V105 = False puts V104's colours back (MAP_PING and SELECT_CYAN switch the two new uses).
CYAN_V105 = True
CYAN_MIG = '#32C7F3'
MAP_PING = True       # V105 (Mig's pick, 1): the map's Singapore dot and its rings in the accent, in both themes
SELECT_CYAN = True    # V105 (Mig's pick, 4): selected text is ink on the accent (Policy's stage keeps the inversion)
if CYAN_V105:
    CYAN = ok_mix(CYAN, CYAN_MIG, 2 / 3)
    CYAN_RGB = ', '.join(str(int(CYAN[i:i + 2], 16)) for i in (1, 3, 5))
    HALO = {'light': 0.57, 'dark': 0.45}
    _sm = lambda x: (lambda y: y * y * (3 - 2 * y))(max(0.0, min(1.0, x)))
    POL_GLOW_STOPS[:] = [(f, ok_mix(c, CYAN_MIG, 0.4 * (1 - _sm((f - 0.323) / (0.484 - 0.323))))
                          if f < 0.484 else c) for f, c in POL_GLOW_STOPS]


def _lit(states, pseudo=''):
    return ','.join(f'a.me-box:{s}{pseudo},.me-box:has(a:{s}){pseudo}' for s in states)


def _halo():
    rgba = lambda a: f'rgba({CYAN_RGB.replace(" ", "")},{a:g})'.replace(',0.', ',.')
    if HALO['light'] == HALO['dark']:
        return rgba(HALO['light'])
    return f'var(--me-halo,{rgba(HALO["light"])})'


GLOW_CSS = ('.me-box{position:relative;transition:box-shadow .3s ease}\n'
            f'.me-box::before{{content:"";position:absolute;inset:0;z-index:1;pointer-events:none;'
            f'box-shadow:inset -5px -5px 4px -1px {CYAN};opacity:0;transition:opacity .3s ease}}\n'
            + (f'.me-dark{{--me-halo:rgba({CYAN_RGB.replace(" ", "")},{HALO["dark"]:g})}}\n'.replace(',0.', ',.')
               if HALO['light'] != HALO['dark'] else '') +
            f'@media (hover: hover){{{_lit(["hover"])}{{box-shadow:5px 5px 12px -3px {_halo()}}}'
            f'{_lit(["hover"], "::before")}{{opacity:1}}}}\n'
            f'{_lit(["focus-visible", "active"])}{{box-shadow:5px 5px 12px -3px {_halo()}}}\n'
            f'{_lit(["focus-visible", "active"], "::before")}{{opacity:1}}\n'
            # the focus outline lies on the box's own line (thickening it), not 4px out, where the rail clipped it
            'a.me-box:focus-visible{outline-offset:-2px}\n') if BOXES and GLOW else ''
HOME_CSS += GLOW_CSS
if SELECT_CYAN:   # V105: sitewide, both themes; on Policy's stage (cyan itself) it stays the inversion, ink and paper
    PAGE_CSS = PAGE_CSS.replace('::selection{background:var(--fg);color:var(--bg)}', f'::selection{{background:{CYAN};color:{INK}}}', 1)
    if POLICY_FX and POL_GLOW:
        HOME_CSS += f'.me-pol ::selection{{background:{INK};color:{PAPER}}}\n'
if NAV_V106:   # V106
    PAGE_CSS += NAV_V106_CSS.replace('__CYAN__', CYAN)
    HOME_CSS += '.me-navhome .me-navname{visibility:hidden}\n'   # over the hero (the prototype shows it once past)

# V112 (Mig): Policy's sphere, small, lights the hero's arrow: its own stops, drawn to the glow's edge (a disc twice
# CUE_GLOW_R across, centred on the arrow's ring, behind the ring and the name). On paper it fades to paper as the
# sphere does; on the dark ground the same cyan fades to nothing instead, held to 70% at its heart so the paper arrow
# keeps 3:1 there (the ink arrow has 7:1 on paper). In the prototype it recedes into the arrow as the page leaves the
# hero: it shrinks to a seventh and fades out over the first CUE_RECEDE of a screen's scrolling. CUE_GLOW = False takes
# it out.
CUE_GLOW = True
CUE_GLOW_R = {'d': 100, 'm': 82}   # px: where the glow has faded out
# V113 (Mig): a little over twice as wide (2.2x), so it runs under the name and the statement's foot. It lies under
# everything in the hero now (the hero's content is isolated and the glow sits at z-index -1 in it), so the words
# keep their ink over it; at the screen's edge it simply runs off. CUE_GLOW_BIG = False puts V112's size back.
CUE_GLOW_BIG = True
if CUE_GLOW_BIG:
    CUE_GLOW_R = {'d': 220, 'm': 180}
CUE_GLOW_DARK = 0.7                # the dark ground's glow at its heart
CUE_RECEDE = 0.4                   # gone by this share of a screen's scrolling


# V114 (Mig: "the Policy glow seems softer and more gradual" -- it is). The two are one gradient, but Policy's is
# drawn about twice as large on a desktop (430px to the arrow's 220) and a little larger on a phone (200 to 180), so its
# fade from cyan to paper runs over more of the page: 282px between 90% and 10% of its colour on a desktop and 131 on a
# phone, to the arrow's 144 and 118 (its steepest step twice Policy's on a desktop, 11% more on a phone). At the size
# Mig set, the arrow's glow keeps Policy's colours but draws its heart and body tighter about the arrow (to 10% of its
# radius on a desktop, 22% on a phone; Policy's take 32%) and spreads the fade over the rest: a phone's now fades as
# Policy's does (129px), a desktop's as gently as its size allows (174px; Policy's softness there would take Policy's
# size). Its reach is unchanged within 4%. CUE_GLOW_SOFT = False puts V113's profile back.
CUE_GLOW_SOFT = True
CUE_GLOW_BODY = {'d': 0.10, 'm': 0.22}   # the share of the radius the heart and body take (Policy's: 0.323)


def _cue_stops(dark=False, body_to=None):
    """Policy's sphere as percentage stops, to paper; or (dark) its body's cyan over transparent, each stop at the
    strength that gives its colour on paper. body_to (V114): the heart and body drawn to that share of the radius,
    the fade spread over the rest."""
    rgb = lambda h: [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    body = [c for f, c in POL_GLOW_STOPS if f >= 0.323][0]
    at = ((lambda f: f * body_to / 0.323 if f <= 0.323 else body_to + (f - 0.323) * (1 - body_to) / (1 - 0.323))
          if body_to else (lambda f: f))
    pct = lambda f: f'{round(at(f) * 100, 2 if body_to else 1):g}%'
    out = []
    for f, c in POL_GLOW_STOPS:
        if not dark:
            out.append(f'{c} {pct(f)}')
            continue
        if f <= 0.323:
            a, col = 1.0, rgb(c)
        else:
            v = [x - y for x, y in zip(rgb(c), rgb(PAPER))]
            k = [x - y for x, y in zip(rgb(body), rgb(PAPER))]
            a, col = max(0.0, min(1.0, sum(x * y for x, y in zip(v, k)) / sum(y * y for y in k))), rgb(body)
        out.append(f'rgba({col[0]},{col[1]},{col[2]},{round(a * CUE_GLOW_DARK, 3):g}) {pct(f)}')
    return 'radial-gradient(circle closest-side, ' + ', '.join(out) + ')'


if CUE_GLOW and CUE_GLOW_SOFT:   # V114: each board's own profile, set on the glow (--cg, --cg-dark)
    HOME_CSS += (f'.me-cueglow{{position:absolute;{"z-index:-1;" if CUE_GLOW_BIG else ""}pointer-events:none;background:var(--cg)}}\n'
                 + ('.me-dark .me-cueglow{background:var(--cg-dark)}\n' if DARK_MODE else ''))
elif CUE_GLOW:
    HOME_CSS += (f'.me-cueglow{{position:absolute;{"z-index:-1;" if CUE_GLOW_BIG else ""}pointer-events:none;background:{_cue_stops()}}}\n'
                 f'.me-dark .me-cueglow{{background:{_cue_stops(dark=True)}}}\n')


CUE_POS = 'position: relative; ' if CUE_GLOW else ''
DRIFT_ISO = 'isolation: isolate; ' if CUE_GLOW and CUE_GLOW_BIG else ''   # V113: the glow's floor


def cue_glow(mobile):
    """The glow's disc, centred on the arrow's ring (the ring is the row's last item, flush right, a row tall)."""
    if not CUE_GLOW:
        return ''
    r, ring = CUE_GLOW_R['m' if mobile else 'd'], (52 if mobile else 64) // 2
    soft = ''
    if CUE_GLOW_SOFT:
        b = CUE_GLOW_BODY['m' if mobile else 'd']
        soft = f' --cg: {_cue_stops(body_to=b)};' + (f' --cg-dark: {_cue_stops(dark=True, body_to=b)};' if DARK_MODE else '')
    return (f'<span class="me-cueglow" aria-hidden="true" style="right: {ring - r}px; top: {ring - r}px; '
            f'width: {2 * r}px; height: {2 * r}px;{soft}"></span>\n')


def box_css(fixed=False):
    """A box's line and ground (fixed: paper and ink in both themes)."""
    line, ground = ('#141414', PAPER) if fixed else (C['fg'], C['bg'])
    return f'box-sizing: border-box; border: {BOX["line"]}px solid {line}; background: {ground};'


def work_card(key, x, links, mobile):
    r = RAIL['m' if mobile else 'd']
    href = CARD_LINKS[key] or links['AdvertisingWork']
    attrs = f'href="{href}"' + (' target="_blank" rel="noopener"' if href.startswith('http') else '')
    label, text = CAPTIONS[key]
    esc = lambda t: keep_compounds(html.escape(t, quote=False))
    pic = (f'<div style="aspect-ratio: 1 / 1.4; overflow: clip; background: {C["wash"]};">'
           + (f'<img src="{BLOB[key]}" alt="{html.escape(ALT[key], quote=True)}" draggable="false" style="display: block; width: 100%; height: 100%; object-fit: cover; object-position: {x}% 50%;">'
              if key in BLOB else '') + '</div>')
    words = (f'<p class="me-fade" style="margin: {r["top"]}px 0 0; {LABEL(r["label"])}">{esc(label)}</p>'
             f'<p class="me-fade me-card-desc" style="margin: {r["between"]}px 0 0; {CAPTION["m" if mobile else "d"]} '
             f'text-wrap: balance;">{esc(bind_hl(text))}</p>')
    if BOXES:   # V103: the card is a box, the picture to its edges, the words inside its padding
        bp = BOX['pad']['m' if mobile else 'd']
        inset = '' if BOX['flush'] else f'padding: {bp}px {bp}px 0;'
        return (f'<a class="me-card me-box" {attrs} style="display: block; width: {r["card"]}px; {box_css()} {NOUL}">'
                f'<div style="{inset}">{pic}</div><div style="padding: 0 {bp}px {bp}px;">{words}</div></a>')
    return (f'<a class="me-card" {attrs} style="display: block; width: {r["card"]}px; {NOUL}">'
            f'{pic}{words}</a>')


# ── Home: nav, hero and chapters ─────────────────────────────────────────────────────────────────────────────
# V65: the nav's ground is glass. Layers under the buttons blur whatever passes beneath them, with no tint, edge or
# shadow, so over a plain ground (a blur of one colour is that colour) they cannot be seen at all; only type,
# pictures and edges scrolling under the nav frost over.
# V66: no hard line where the frost ends. The glass runs on below the nav and its blur thins out down its length:
# four layers, each lighter than the last and reaching further down, each fading out at its foot. Blurs laid on
# blurs add up, so the frost is full behind the buttons and tapers smoothly to nothing (a mix of one sharp and one
# blurred picture would show a ghost of the sharp one instead).
# V68: and it is milkier, like frosted glass: over the blur lies a veil in the page's own ground colour, strongest
# behind the buttons and thinning out with the blur. A veil of the ground's colour cannot be seen over the ground,
# but it pales whatever else passes under it towards the ground (milky in the light theme, smoked in the dark).
# Over a field of solid colour it would lay a pale strip across it, so in the prototype it thins out as Policy's
# blue (or, without it, the footer) comes up under the nav, and stays out over the footer that follows.
GLASS = {'d': dict(h=108, layers=[(12, 40, 70), (6, 56, 86), (3, 70, 100), (1.5, 84, 108)],   # (blur px, solid to, gone by)
                   veil=(0.3, 30, 96)),                                                          # (strength, solid to, gone by)
         'm': dict(h=84, layers=[(10, 32, 55), (5, 44, 66), (2.5, 55, 77), (1.2, 66, 84)],
                   veil=(0.3, 24, 74))}
# V110: the glass refined. (1) A finer, longer blur: six layers, each half the last, every mask eased (smoothstep) so
# no layer ends on a line, and the frost tapers over twice the distance it did. (2) The veil holds at full strength
# behind the name and the burger (to just below them), then eases out, and is a little stronger (0.4): what passes
# under the items is quieter. (3) Over the reel the veil is smoke, not milk: on Home its colour is a band three glass-
# heights tall (paper, ink, paper) that the prototype slides up with the scroll, so the paper/ink boundaries ride on
# the panel's own top and bottom edges as they cross the glass (on a desktop only within the panel's columns, its
# sides feathered). A paper veil over the dark footage had lifted it to a grey under the paper items; smoke deepens
# it. No saturate(): it would show the glass over a field of flat colour (Policy's blue). GLASS_V110 = False puts
# back V68's glass.
GLASS_V110 = True
if GLASS_V110:
    GLASS = {'d': dict(h=128, layers=[(16, 36, 66), (8, 46, 82), (4, 58, 98), (2, 70, 110), (1, 82, 120), (0.5, 92, 128)],
                       veil=(0.4, 48, 112)),
             'm': dict(h=100, layers=[(12, 26, 50), (6, 34, 64), (3, 44, 76), (1.5, 54, 86), (0.75, 62, 94), (0.4, 70, 100)],
                       veil=(0.4, 40, 90))}
SMOKE_SOFT, SMOKE_FEATHER = 8, 20   # the half-width of the band's paper/ink boundaries; of the panel's sides (desktop)


def ease_mask(s, e, n=8):
    """A mask on from the top to s, off by e, along a smoothstep (no line where it ends)."""
    stops = ['#000 ' + f'{s:g}px']
    for i in range(1, n):
        t = i / n
        stops.append(f'rgba(0,0,0,{round(1 - t * t * (3 - 2 * t), 3):g}) {round(s + (e - s) * t, 1):g}px')
    stops.append(f'transparent {e:g}px')
    return 'linear-gradient(to bottom, ' + ', '.join(stops) + ')'


def smoke_cols():
    """Desktop: the reel panel's columns (grid columns 7 to 12)."""
    left = round(64 + span(6) + GUT)
    return left, left + PANEL_W


def glass_v110(mobile, home):
    g = GLASS['m' if mobile else 'd']
    h = g['h']
    layers = ''.join(
        f'<div style="position: absolute; inset: 0; -webkit-backdrop-filter: blur({b:g}px); backdrop-filter: blur({b:g}px); '
        f'-webkit-mask-image: {ease_mask(s, e)}; mask-image: {ease_mask(s, e)};"></div>'
        for b, s, e in g['layers'])
    a, s, e = g['veil']
    if home:
        P, k = C['bg'], SMOKE_SOFT
        band = f'linear-gradient(to bottom, {P} {h - k}px, {INK} {h + k}px, {INK} {2 * h - k}px, {P} {2 * h + k}px)'
        if mobile:
            ground = f'background-color: {P}; background-image: {band}; background-size: 100% {3 * h}px; background-repeat: no-repeat;'
        else:
            l, r = smoke_cols()
            f = SMOKE_FEATHER
            cols = f'linear-gradient(to right, {P} {l - f}px, transparent {l + f}px, transparent {r - f}px, {P} {r + f}px)'
            ground = (f'background-color: {P}; background-image: {cols}, {band}; background-size: 100% 100%, 100% {3 * h}px; '
                      f'background-repeat: no-repeat;')
    else:
        ground = f'background: {C["bg"]};'
    layers += (f'<div class="me-veil" style="position: absolute; inset: 0; {ground} opacity: {a:g}; '
               f'-webkit-mask-image: {ease_mask(s, e)}; mask-image: {ease_mask(s, e)};"></div>')
    return (f'<div class="me-glass" aria-hidden="true" style="position: absolute; left: 0; right: 0; top: 0; height: {h}px; z-index: -1; '
            f'pointer-events: none;">{layers}</div>')


def glass(mobile, home=False):
    if GLASS_V110:
        return glass_v110(mobile, home)
    g = GLASS['m' if mobile else 'd']
    layers = ''.join(
        f'<div style="position: absolute; inset: 0; -webkit-backdrop-filter: blur({b:g}px); backdrop-filter: blur({b:g}px); '
        f'-webkit-mask-image: linear-gradient(to bottom, #000 {s}px, transparent {e}px); mask-image: linear-gradient(to bottom, #000 {s}px, transparent {e}px);"></div>'
        for b, s, e in g['layers'])
    a, s, e = g['veil']
    layers += (f'<div class="me-veil" style="position: absolute; inset: 0; background: {C["bg"]}; opacity: {a:g}; '
               f'-webkit-mask-image: linear-gradient(to bottom, #000 {s}px, transparent {e}px); mask-image: linear-gradient(to bottom, #000 {s}px, transparent {e}px);"></div>')
    return (f'<div class="me-glass" aria-hidden="true" style="position: absolute; left: 0; right: 0; top: 0; height: {g["h"]}px; z-index: -1; '
            f'pointer-events: none;">{layers}</div>')


def home_nav(mobile):
    """On home the nav lies over the hero (negative bottom margin), pinned, on its glass; in the prototype its colour
    follows the ground beneath it."""
    h, pad = (56, 20) if mobile else (72, 64)
    buttons = f'{nav_name("#top", hidden_on_hero=True, mobile=mobile)}\n{menu_btn_right()}' if NAV_V106 else f'{menu_btn()}\n{theme_btn()}'
    return (f'<header class="me-nav" style="position: sticky; top: 0; z-index: 20; flex-shrink: 0; height: {h}px; margin-bottom: -{h}px; '
            f'box-sizing: border-box; display: flex; align-items: center; justify-content: space-between; padding: 0 {pad}px; '
            f'background-color: transparent; color: {C["fg"]};">\n{glass(mobile, home=True)}\n'   # V98: the glass is back, the rule under it gone
            f'{buttons}\n</header>')


def hero(mobile):
    if not mobile:
        stmt, _ = typed('p', STATEMENT, '', f'margin: {HERO_TOP["d"]}px 0 0; max-width: {HERO_MAXW}px; {H2["d"]} text-wrap: balance;', 'me-typeload', 350)
        return home_nav(False) + f"""
<section id="top" style="flex-shrink: 0; height: 900px; box-sizing: border-box; display: flex; flex-direction: column; padding: 72px 64px 34px; background-color: {C['bg']}; color: {C['fg']};">
<div class="me-drift" style="{DRIFT_ISO}flex-grow: 1; display: flex; flex-direction: column;">
{stmt}
<div style="flex-grow: 1;"></div>
<div style="{CUE_POS}display: flex; justify-content: flex-end; margin-bottom: 30px;">
{cue_glow(False)}<a class="me-cue" href="#work" aria-label="Scroll to work" style="{CUE_POS}display: flex; align-items: center; justify-content: center; width: 64px; height: 64px; border: 1px solid {C['ring']}; border-radius: 50%; color: inherit;">{ARROW_DOWN.format(s=22)}</a>
</div>
<h1 class="me-rise" aria-label="Miguel Escobar" data-fit="name_d" style="{CUE_POS}margin: 0; display: flex; gap: 0.2em; font-size: {FIT.get('name_d', 160.93)}px; font-weight: 400; line-height: 0.86; letter-spacing: -0.03em; white-space: nowrap; overflow: clip;"><span>{NAME[0]}</span><span>{NAME[1]}</span></h1>
</div>
</section>"""
    stmt, _ = typed('p', STATEMENT, '', f'margin: {HERO_TOP["m"]}px 0 0; {H2["m"]} text-wrap: balance;', 'me-typeload', 350)
    return home_nav(True) + f"""
<section id="top" style="flex-shrink: 0; height: 844px; box-sizing: border-box; display: flex; flex-direction: column; padding: 56px 20px 24px; background-color: {C['bg']}; color: {C['fg']};">
<div class="me-drift" style="{DRIFT_ISO}flex-grow: 1; display: flex; flex-direction: column;">
{stmt}
<div style="flex-grow: 1;"></div>
<div style="{CUE_POS}display: flex; justify-content: flex-end; margin-bottom: 22px;">
{cue_glow(True)}<a class="me-cue" href="#work" aria-label="Scroll to work" style="{CUE_POS}display: flex; align-items: center; justify-content: center; width: 52px; height: 52px; border: 1px solid {C['ring']}; border-radius: 50%; color: inherit;">{ARROW_DOWN.format(s=20)}</a>
</div>
<h1 class="me-rise" aria-label="Miguel Escobar" data-fit="name_m" style="{CUE_POS}margin: 0; display: flex; flex-direction: column; font-size: {FIT.get('name_m', 77)}px; font-weight: 400; line-height: 0.86; letter-spacing: -0.03em; white-space: nowrap; overflow: clip;"><span>{NAME[0]}</span><span>{NAME[1]}</span></h1>
</div>
</section>"""


def work_section(links, mobile):
    """The first chapter: the samples on one rail (after Monocle's rails). Desktop shows four at a time and the rings
    beside the headline page it; a phone shows two and the edge of a third, runs to the screen's edges, and is
    swiped."""
    r = RAIL['m' if mobile else 'd']
    cards = ''.join(work_card(k, x, links, mobile) for k, x in GALLERY)
    hl, _ = typed('h2', WORK_HEAD, EMPH['work'], f'margin: 0; {H2["m" if mobile else "d"]} text-wrap: balance;')
    lit = BOXES and GLOW   # V104: room for the cards' halo, padded in and pulled back out
    if mobile:
        head = f'<div class="me-rv">{hl}</div>'
        edges = (f'margin: {r["head_gap"]}px -20px -{GLOW_ROOM}px; padding: 0 20px {GLOW_ROOM}px;' if lit else
                 f'margin: {r["head_gap"]}px -20px 0; padding: 0 20px;')
        rail = (f'<div class="me-rv me-gal me-rail me-rail-m" style="{edges} scroll-padding-inline: 20px; gap: {r["gap"]}px;">'
                f'{cards}</div>')
        pad = f'{FIRST_CH_TOP["m"]}px 20px {CH_PAD["m"] - RAIL_TAIL["m"]}px'
    else:
        ring = 'class="me-railbtn" type="button"'
        head = f"""<div style="{GRID12} align-items: end;">
<div class="me-rv" style="grid-column: 1 / span 10;">{hl}</div>
<div style="grid-column: 11 / span 2; justify-self: end; display: flex; gap: 12px; margin-bottom: {RAIL_NAV_DROP}px;">
<button {ring} aria-label="Previous work" onClick="{{{{ railPrev }}}}" disabled="{{{{ atStart }}}}">{ARROW_LEFT.format(s=18)}</button>
<button {ring} aria-label="More work" onClick="{{{{ railNext }}}}" disabled="{{{{ atEnd }}}}">{ARROW_RIGHT.format(s=18)}</button>
</div>
</div>"""
        edges = (f'margin: {r["head_gap"]}px -{GLOW_ROOM}px -{GLOW_ROOM}px 0; padding: 0 {GLOW_ROOM}px {GLOW_ROOM}px 0;' if lit else
                 f'margin-top: {r["head_gap"]}px;')
        rail = (f'<div class="me-rv me-gal me-rail" onScroll="{{{{ railScroll }}}}" style="{edges} gap: {r["gap"]}px;">'
                f'{cards}</div>')
        pad = f'{FIRST_CH_TOP["d"]}px 64px {CH_PAD["d"] - RAIL_TAIL["d"]}px'
    return f"""<section id="work" style="position: relative; box-sizing: border-box; padding: {pad};">
{heavy_rule(mobile)}
{head}
{rail}
</section>"""


def chapter_text_d(key, head, body, more, links, extra=''):
    hl, ms = typed('h2', head, EMPH[key], f'margin: 0; {H2["d"]} text-wrap: balance;')
    link = (f'\n<div class="me-rv" style="margin-top: {ACTION["d"]}px;"><div class="me-fade" style="{fade_delay(ms).strip()}">'
            f'{more_link(links[more[0]], more[1], 22, 48)}</div></div>') if more else ''
    return (f'<div style="grid-column: 1 / span 6; grid-row: 2; {extra}">\n<div class="me-rv">{hl}</div>\n'
            f'<div class="me-rv" style="margin-top: {TEXT["d"]}px; max-width: {span(5)}px;"><p class="me-fade" style="margin: 0; {BODY_L} color: {C["fg85"]}; '
            f'text-wrap: pretty;{fade_delay(ms)}">{keep_compounds(body)}</p></div>{link}\n</div>')


def chapter_rule_d():
    return f'<div aria-hidden="true" style="grid-column: 1 / -1; grid-row: 1; border-top: {HEAVY}px solid {C["fg"]}; margin-bottom: {HEAD_GAP["d"]}px;"></div>'


def branded_panel(links, head, body, more, mobile):
    """Branded is the reel: reframed for the frame it fills (9:16 edge to edge on a phone, a screen tall; 4:5 in the
    right half on a desktop, stretched as tall as Editorial's column where that runs longer), it is the chapter's
    ground. The footage simply plays, under a veil that darkens it most at the foot, where the words sit (V63: no
    unmasking, zoom or darkening on arrival); the headline types and the body and link follow over it, in paper. A
    ring at the top right pauses it. (The panel clips rather than hides its overflow: a hidden overflow would make
    it a scroll container, and the words' view timeline would then run against the panel, not the page.)"""
    if mobile:
        h2, body_s, pad, foot, h_to_p, p_to_link = H2['m'], BODY, 20, 28, text_gap(H2['m'], BODY, 'm'), ACTION['m']
        size, src = f'height: {PANEL_H}px;', 'reel-v'
        # V86: no paper under the panel on a phone; the reel runs straight into Policy's ink
        sec = f'<section id="branded" style="position: relative; box-sizing: border-box; padding: {CH_PAD["m"]}px 0 {0 if POLICY_FX else CH_PAD["m"]}px;">'
    else:
        h2, body_s, pad, foot, h_to_p, p_to_link = PAIR['h2'], PAIR['body'], PAIR['pad'], PAIR['pad'], PAIR['h_to_p'], PAIR['p_to_link']
        size, src = f'flex: 1 1 auto; min-height: {round(PANEL_W * 5 / 4)}px;', 'reel-45'
        sec = '<section id="branded" style="grid-column: 7 / span 6; min-width: 0; align-self: stretch; display: flex; flex-direction: column;">'
    hl, ms = typed('h2', head, EMPH['branded'], f'margin: 0; {h2} color: {C["muted"]}; text-wrap: balance;')
    return f"""{sec}
<div class="me-ch-reel me-onvideo me-reel {{{{ reelCls }}}}" style="position: relative; {size} overflow: clip; display: flex; flex-direction: column; justify-content: flex-end; background: {INK}; color: {PAPER};">
<div style="position: absolute; inset: 0;">
<video src="{BLOB[src]}" poster="{BLOB[src + '-poster']}" autoplay="" muted="" loop="" playsinline="" preload="auto" aria-hidden="true" ref="{{{{ reelRef }}}}" style="display: block; width: 100%; height: 100%; object-fit: cover;"></video>
</div>
<div class="me-rv" style="padding: 0 {pad}px {foot}px;">
<div aria-hidden="true" style="position: absolute; inset: 0; background: {VEIL}; pointer-events: none;"></div>
<div style="position: relative;">
<div aria-hidden="true" style="border-top: {HEAVY}px solid {PAPER}; margin-bottom: {HEAD_GAP['m' if mobile else 'd']}px;"></div>
{hl}
<p class="me-fade" style="margin: {h_to_p}px 0 0; {body_s} color: rgba(234, 231, 225, 0.9); text-wrap: pretty;{fade_delay(ms)}">{keep_compounds(body)}</p>
<div class="me-fade" style="margin-top: {p_to_link}px;{fade_delay(ms)}">{more_link(links[more[0]], more[1], 19, 44)}</div>
</div>
</div>
<button type="button" class="me-reelbtn" data-act="reel" aria-label="{{{{ reelLabel }}}}" onClick="{{{{ toggleReel }}}}">{ICON_PAUSE}{ICON_PLAY}</button>
</div>
</section>"""


# Editorial's picture: none for now (the Konfekt placeholder is out). When one arrives, set its blob key, alt text,
# aspect ratio (as 'w / h') and desktop width, e.g. dict(key='editorial-pic', alt='...', ratio='3 / 2', width=PAIR_TEXT_W).
EDITORIAL_PIC = None
# V99: Mig's photograph of his magazines (Esquire on top), cut out, on a transparent ground with a soft shadow, at the
# column's full width (the heavy rule's), 5:3 (620 x 372: the Branded panel keeps its height).
BLOB['editorial-magazines'] = '/_blob/d4665e209c4aa0839459334bf6ff0d18'   # 1240 x 744 WebP with alpha
EDITORIAL_PIC = dict(key='editorial-magazines', ratio='5 / 3', width=None,
                     alt='A pile of magazines, Esquire Philippines on top and Smile beneath it.')


def editorial_pic(mobile):
    """Editorial's picture at its own aspect ratio, still (V63: no unmasking on arrival): the column's full width on
    a phone, EDITORIAL_PIC['width'] on a desktop."""
    img = (f'<img src="{BLOB[EDITORIAL_PIC["key"]]}" alt="{html.escape(EDITORIAL_PIC["alt"], quote=True)}" '
           f'style="display: block; width: 100%; height: 100%; object-fit: cover;">')
    width = '' if mobile or not EDITORIAL_PIC['width'] else f' width: {EDITORIAL_PIC["width"]}px; max-width: 100%;'
    gap = BLOCK['m'] if mobile else PAIR['p_to_link']
    return (f'<div style="margin-top: {gap}px;{width}"><div style="aspect-ratio: {EDITORIAL_PIC["ratio"]}; '
            f'overflow: clip;">{img}</div></div>')   # V99: no wash: the picture is a cut-out on a transparent ground


def pair_d(links, sc):
    """Desktop: Editorial and Branded side by side, six columns each (they follow one another on a phone). Editorial
    opens on a heavy rule level with the top of Branded's reel panel and reads down from it: headline, paragraph
    (and its picture, when there is one), and its link at the column's foot. Its column stops a gutter short of the
    panel, so two gutters part them and the panel keeps its grid line. The panel runs as tall as the column (never
    shorter than 4:5), so the two end together and the links sit level. Both halves' words share one size and one
    measure."""
    _, head, body, more = sc['editorial']
    hl, ms = typed('h2', head, EMPH['editorial'], f'margin: 0; {PAIR["h2"]} text-wrap: balance;')
    pic = ('\n' + editorial_pic(False)) if EDITORIAL_PIC else ''
    left = f"""<section id="editorial" style="grid-column: 1 / span 6; min-width: 0; align-self: stretch; box-sizing: border-box; display: flex; flex-direction: column; padding: 0 {WIDE_GAP - GUT}px {PAIR['pad']}px 0;">
<div aria-hidden="true" style="border-top: {HEAVY}px solid {C['fg']}; margin-bottom: {HEAD_GAP['d']}px;"></div>
<div style="max-width: {PAIR_TEXT_W}px;">
<div class="me-rv">{hl}</div>
<div class="me-rv" style="margin-top: {PAIR['h_to_p']}px;"><p class="me-fade" style="margin: 0; {PAIR['body']} color: {C['fg85']}; text-wrap: pretty;{fade_delay(ms)}">{keep_compounds(body)}</p></div>
</div>{pic}
<div aria-hidden="true" style="flex: 1 1 auto; min-height: {PAIR['p_to_link']}px;"></div>
<div class="me-rv"><div class="me-fade" style="{fade_delay(ms).strip()}">{more_link(links[more[0]], more[1], 19, 44)}</div></div>
</section>"""
    _, head, body, more = sc['branded']
    # No exit drift here (the other chapters have one): the nav's colour follows the panel's layout box, and a drift
    # would carry the panel 50-odd pixels above it by the time its foot reaches the nav.
    return f"""<div style="position: relative; box-sizing: border-box; padding: {CH_PAD['d']}px 64px;">
<div style="{GRID12} align-items: start;">
{left}
{branded_panel(links, head, body, more, False)}
</div>
</div>"""


def chapters_d(links):
    """About (the map in seven columns, stopping a gutter short of the words so two gutters part them, its top level
    with the top of the rule over the words in the last five: the rule, headline and paragraph set as Editorial's
    are); Editorial and Branded side by side, six columns each; then the last chapter, its headline across ten
    columns and its paragraph from the half line."""
    sc = {s[0]: s for s in SCROLL}
    _, head, body, _ = sc['about']
    hl, ms = typed('h2', head, EMPH['about'], f'margin: 0; {PAIR["h2"]} text-wrap: balance;')
    about = f"""<section id="about" style="position: relative; box-sizing: border-box; padding: {CH_PAD['d']}px 64px;">
<div class="me-exit" style="{GRID12} align-items: start;">
{plate(False, f'grid-column: 1 / span {MAP_COLS}; grid-row: 1; justify-self: start; width: {MAP_W_D}px; ')}
<div style="grid-column: {MAP_COLS + 1} / span {12 - MAP_COLS}; grid-row: 1; min-width: 0;">
<div aria-hidden="true" style="border-top: {HEAVY}px solid {C['fg']}; margin-bottom: {HEAD_GAP['d']}px;"></div>
<div style="max-width: {PAIR_TEXT_W}px;">
<div class="me-rv">{hl}</div>
<div class="me-rv" style="margin-top: {PAIR['h_to_p']}px;"><p class="me-fade" style="margin: 0; {PAIR['body']} color: {C['fg85']}; text-wrap: pretty;{fade_delay(ms)}">{keep_compounds(body)}</p></div>
</div>
</div>
</div>
</section>"""
    _, head, body, _ = sc['policy']
    hl, ms = typed('h2', head, EMPH['policy'], f'margin: 0; {H2["d"]} text-wrap: balance;')
    policy = f"""<section id="policy" style="position: relative; box-sizing: border-box; padding: {CH_PAD['d']}px 64px {PAGE_BOTTOM['d'] - TEXT_TAIL + FOOT_OVERLAP}px;">
<div class="me-exit" style="position: relative; {GRID12} align-items: start;">
{chapter_rule_d()}
<div class="me-rv" style="grid-column: 1 / span 10; grid-row: 2;">{hl}</div>
<div class="me-rv" style="grid-column: 7 / span 5; grid-row: 3; margin-top: {text_gap(H2['d'], BODY_L, 'd')}px;"><p class="me-fade" style="margin: 0; {BODY_L} color: {C['fg85']}; text-wrap: pretty;{fade_delay(ms)}">{keep_compounds(body)}</p></div>
</div>
</section>"""
    return '\n'.join([about, pair_d(links, sc), policy_stage(False) if POLICY_FX else policy])


def chapters_m(links):
    """The same on a phone, one after another: About ends on the map (it drifts with the paragraph above it, so the
    gap between them holds); Branded is the reel panel, edge to edge. In the prototype the paragraph (and the map)
    rise into place as the chapter comes up the screen and hold from mid-screen on, so the space under the headline
    is exact while it is read and as it leaves."""
    sc = {s[0]: s for s in SCROLL}
    out = []
    for key in ('about', 'editorial', 'branded', 'policy'):
        _, head, body, more = sc[key]
        if key == 'policy' and POLICY_FX:
            out.append(policy_stage(True))
            continue
        if key == 'branded':
            out.append(branded_panel(links, head, body, more, True))
            continue
        hl, ms = typed('h2', head, EMPH[key], f'margin: 0; {H2["m"]} text-wrap: balance;')
        art = ('\n' + plate(True, f'margin-top: {BLOCK["m"]}px; ') if key == 'about' else
               '\n' + editorial_pic(True) if key == 'editorial' and EDITORIAL_PIC else '')
        link = (f'\n<div class="me-rv" style="margin-top: {ACTION["m"]}px;"><div class="me-fade" style="{fade_delay(ms).strip()}">'
                f'{more_link(links[more[0]], more[1], 19, 44)}</div></div>') if more else ''
        bottom = PAGE_BOTTOM['m'] - TEXT_TAIL + FOOT_OVERLAP if key == 'policy' else CH_PAD['m']
        out.append(f"""<section id="{key}" style="position: relative; box-sizing: border-box; padding: {CH_PAD['m']}px 20px {bottom}px;">
<div class="me-exit" style="position: relative;">
{heavy_rule(True)}
<div class="me-rv">{hl}</div>
<div class="me-par" style="margin-top: {text_gap(H2['m'], BODY, 'm')}px;">
<div class="me-rv"><p class="me-fade" style="margin: 0; {BODY} color: {C['fg85']}; text-wrap: pretty;{fade_delay(ms)}">{keep_compounds(body)}</p></div>{art}
</div>{link}
</div>
</section>""")
    return '\n'.join(out)


def home_sections(links, mobile):
    run = work_section(links, mobile) + '\n' + (chapters_m(links) if mobile else chapters_d(links))
    return hero(mobile) + '\n' + (f'<div style="flex-shrink: 0; margin-top: -{HERO_OVERLAP}px; padding-top: {HERO_OVERLAP}px; '
                                  f'background: {C["bg"]};">\n{run}\n</div>')


def footer_import(mobile=False):
    name = 'LetsTalkMobile' if mobile else 'LetsTalkDesktop'
    w = 390 if mobile else 1440
    return f'<dc-import name="{name}" hint-size="{w}px,{hval(name + ".dc.html", 700 if mobile else 780)}px"></dc-import>'


def home_footer(mobile=False):
    """On home the footer overlaps the last chapter by 4px (no seam at any zoom) and carries the view timeline the
    nav follows."""
    pad = 20 if mobile else 64   # V79: Policy and the footer share the ink, so a hairline parts them
    seam_cls = ' class="me-footseam"' if POLICY_FX and POL_GLOW else ''   # V102: the dark theme's alone
    return (f'<div class="me-ch-foot" style="position: relative; z-index: 1; flex-shrink: 0; margin-top: -{FOOT_OVERLAP}px;">{footer_import(mobile)}'
            f'<div aria-hidden="true"{seam_cls} style="position: absolute; left: {pad}px; right: {pad}px; top: {FOOT_OVERLAP}px; border-top: 1px solid {C["frule"]};"></div></div>')


# ── Menu ─────────────────────────────────────────────────────────────────────────────────────────────────────
def menu_overlay(links, current, mobile, height, doc=False):
    """The menu: a sheet of the page's own ground, the nav's two buttons (close, where the menu button was; theme), and five items on hairlines
    under a heavy rule. Contact is the one anchor: it closes the menu and scrolls to the footer. The current page's
    item is quieter and takes you to its top."""
    pad, navh, fs = (20, 56, MENU_FS['m']) if mobile else (64, 72, MENU_FS['d'])
    pt, pb = (14, 18) if mobile else (20, 26)
    rows = []
    for i, (label, key) in enumerate(MENU_ITEMS):
        cur = key == current
        href = '#top' if cur else (key if key.startswith('#') else links[key])
        close = ' onClick="{{ closeMenu }}"' if (href.startswith('#') and not doc) else ''
        edge = f'{HEAVY}px solid {C["fg"]}' if i == 0 else f'1px solid {C["rule"]}'
        tone = f' color: {C["muted"]};' if cur else ''
        aria = ' aria-current="page"' if cur else ''
        rows.append(f'<a class="me-mi" href="{href}"{close}{aria} style="display: block; padding: {pt}px 0 {pb}px; '
                    f'border-top: {edge}; font-size: {fs}px; line-height: 1; letter-spacing: {MENU_LS["m" if mobile else "d"]}; {NOUL}{tone}"><span class="me-mlabel">{label}</span></a>')
    cls = 'me-menu is-open' if doc else 'me-menu {{ menuCls }}'
    bcls, bst = btn_look('left')
    if NAV_V106:   # V106: the name at the left (home; on Home, its hero, closing the menu), the close where the menu button was
        bst = ' style="margin-right: -13px;"'
    closer = (f'<a href="{links["home"]}" class="me-iconbtn{bcls}" aria-label="Close menu"{bst}>{CLOSE_X}</a>' if doc else close_btn())
    if NAV_V106:
        at_home = current == 'home'
        top = f'{nav_name("#top" if at_home else links["home"], close=at_home and not doc, mobile=mobile)}\n{closer}'
        foot = f'\n{theme_switch(mobile)}'
        head = ''
        if MENU_SWITCH_TOP:   # V109
            head, foot = f'\n{theme_switch_top(mobile)}', ''
        if not DARK_MODE:     # V115: no switch
            head = foot = ''
    else:
        top, foot, head = f'{closer}\n{theme_btn()}', '', ''
    return f"""<div id="menu" class="{cls}" style="position: absolute; left: 0; top: 0; width: 100%; height: {height}px; z-index: 50; box-sizing: border-box; display: flex; flex-direction: column; padding: 0 {pad}px {28 if mobile else 64}px; background: {C['bg']}; color: {C['fg']};">
<div style="display: flex; align-items: center; justify-content: space-between; flex-shrink: 0; height: {navh}px;">
{top}
</div>
<div style="flex-grow: 1;"></div>{head}
<nav aria-label="Menu" style="display: flex; flex-direction: column; border-bottom: 1px solid {C['rule']};">
{chr(10).join(rows)}
</nav>{foot}
</div>"""


# ── Boards: home ─────────────────────────────────────────────────────────────────────────────────────────────
def home_boards():
    for mobile in (False, True):
        w, vh, links = (390, 844, M_LINKS) if mobile else (1440, 900, D_LINKS)
        name = 'NewHomeMobile.dc.html' if mobile else 'NewHome.dc.html'
        script = page_script(rail=True, reel=True)
        props = THEME_PROP
        # the whole page, for the canvas
        body = f"""<div id="page" class="me-root{THEME_CLS}" style="position: relative; width: {w}px; {hcss(name, 6000)} display: flex; flex-direction: column; overflow: clip; background: {C['fbg']}; color: {C['fg']}; {BASE}">
{home_sections(links, mobile)}
{home_footer(mobile)}
{menu_overlay(links, 'home', mobile, vh)}
</div>"""
        write(name, dc('Home, full scroll' + (', mobile' if mobile else ''), body, w, hval(name, 6000), props, script, extra_css=HOME_CSS))
        # the prototype: one screen, scrolled
        pname = 'NewHomeMobilePlay.dc.html' if mobile else 'NewHomePlay.dc.html'
        body = f"""<div{THEME_ATTR} style="position: relative; width: {w}px; height: {vh}px; overflow: hidden; background: {C['bg']}; {BASE}">
<div class="me-scroller" style="width: {w}px; height: {vh}px; overflow-x: hidden; overflow-y: auto;">
<div class="me-root" style="width: {w}px; display: flex; flex-direction: column; background: {C['fbg']}; color: {C['fg']};">
{home_sections(links, mobile)}
{home_footer(mobile)}
</div>
</div>
{menu_overlay(links, 'home', mobile, vh)}
</div>"""
        write(pname, dc('Home, scroll prototype' + (', mobile' if mobile else ''), body, w, vh, props, script,
                        proto=(vh, 56 if mobile else 72), extra_css=HOME_CSS))


def dark_previews():
    """The home page again, in the dark theme, for the canvas (V115: gone, and their old files with them)."""
    if not DARK_MODE:
        for f in ('NewHomeDark.dc.html', 'NewHomeMobileDark.dc.html'):
            if os.path.exists(os.path.join(P, f)):
                os.remove(os.path.join(P, f))
        return
    for mobile in (False, True):
        src = 'NewHomeMobile' if mobile else 'NewHome'
        w, h = (390, hval(src + '.dc.html', 6000)) if mobile else (1440, hval(src + '.dc.html', 6000))
        if SERIF:   # the board's own `headlines` tweak, passed on to the page it shows
            body = (f'<div style="width: {w}px; height: {h}px;"><dc-import name="{src}" theme="dark" headlines="{{{{ headlines }}}}" '
                    f'hint-size="{w}px,{h}px"></dc-import></div>')
            write(src + 'Dark.dc.html', dc('Home, dark' + (', mobile' if mobile else ''), body, w, h, HL_PROP, HL_SCRIPT))
            continue
        body = f'<div style="width: {w}px; height: {h}px;"><dc-import name="{src}" theme="dark" hint-size="{w}px,{h}px"></dc-import></div>'
        write(src + 'Dark.dc.html', dc('Home, dark' + (', mobile' if mobile else ''), body, w, h))


# ── Boards: shared nav, footer, menu ─────────────────────────────────────────────────────────────────────────
NAV_SCRIPT = """class Component extends DCLogic {
renderVals() {
const p = this.props;
return {
dark: !!p.dark,
menuOpen: !!p.menuOpen,
onTheme: () => { if (typeof p.toggleTheme === 'function') p.toggleTheme(); },
onMenu: () => { if (typeof p.openMenu === 'function') p.openMenu(); },
};
}
}"""
NAV_PROPS = {'dark': {'editor': None}, 'menuOpen': {'editor': None}, 'toggleTheme': {'editor': None}, 'openMenu': {'editor': None}}
if NAV_V106:   # no theme switch in the nav now
    NAV_SCRIPT = NAV_SCRIPT.replace("onTheme: () => { if (typeof p.toggleTheme === 'function') p.toggleTheme(); },\n", '')
    NAV_PROPS = {k: v for k, v in NAV_PROPS.items() if k != 'toggleTheme'}
if not DARK_MODE:   # V115: nor any theme at all
    NAV_SCRIPT = NAV_SCRIPT.replace('dark: !!p.dark,\n', '')
    NAV_PROPS = {k: v for k, v in NAV_PROPS.items() if k != 'dark'}


def nav_boards():
    for mobile in (False, True):
        w, h, pad = (390, 56, 20) if mobile else (1440, 72, 64)
        links = M_LINKS if mobile else D_LINKS
        buttons = f'{nav_name(links["home"], mobile=mobile)}\n{menu_btn_right("onMenu")}' if NAV_V106 else f"{menu_btn('onMenu')}\n{theme_btn('onTheme')}"
        body = f"""<header style="position: relative; z-index: 1; width: {w}px; height: {h}px; box-sizing: border-box; display: flex; align-items: center; justify-content: space-between; padding: 0 {pad}px; background: transparent; color: {C['fg']}; {BASE}">
{glass(mobile)}
{buttons}
</header>"""
        name = 'NavBarMobile.dc.html' if mobile else 'NavBarDesktop.dc.html'
        # the buttons' own rule, so the board also draws them right on its own (a page that imports it has it already)
        own = '.me-iconbtn{display:flex;align-items:center;justify-content:center;flex-shrink:0;width:44px;height:44px;padding:0;margin:0;border:0;border-radius:0;background:transparent;color:inherit;font:inherit;cursor:pointer}\n.me-themeicon{display:block}\n' + (GLASS_BTN_CSS if GLASS_BTNS else '')
        if NAV_V106:   # V106: and the name's
            own = own.replace('.me-themeicon{display:block}\n', '') + NAVNAME_RULES
        write(name, dc('Navigation bar, ' + ('mobile' if mobile else 'desktop'), body, w, h, NAV_PROPS, NAV_SCRIPT, imported=True, extra_css=own))


def nav_import(mobile):
    name, w, h = ('NavBarMobile', 390, 56) if mobile else ('NavBarDesktop', 1440, 72)
    theme = '' if NAV_V106 else ' toggle-theme="{{ toggleTheme }}"'
    dark = ' dark="{{ dark }}"' if DARK_MODE else ''   # V115
    return (f'<dc-import name="{name}"{dark} menu-open="{{{{ menuOpen }}}}"{theme} '
            f'open-menu="{{{{ openMenu }}}}" hint-size="{w}px,{h}px"></dc-import>')


def footer_boards():
    contacts = [
        ('mailto:migmescobar@gmail.com', 'migmescobar@gmail.com'),
        ('tel:+6598517897', '+65&nbsp;9851&nbsp;7897'),
        ('https://www.linkedin.com/in/miguel-escobar-6u56u5', 'LinkedIn'),
        ('https://www.miguel-escobar.com/MiguelEscobar_2026_CV_Resume.pdf', 'Download my CV'),
    ]
    for mobile in (False, True):
        name = 'LetsTalkMobile.dc.html' if mobile else 'LetsTalkDesktop.dc.html'
        w = 390 if mobile else 1440
        h = hval(name, 700 if mobile else 780)
        height = 'height: auto;' if MEASURE else f'height: {h}px;'
        lower = (f'<div style="display: flex; flex-wrap: wrap; justify-content: space-between; gap: 8px 24px; border-top: 1px solid {C["frule"]}; '
                 f'padding-top: {14 if mobile else 18}px; {LABEL(LABEL_PX["m" if mobile else "d"], C["f70"])}">'
                 f'<span>© 2026 Miguel Escobar</span><span>Ownself vibe code</span></div>')
        hl = ' class="{{ hlCls }}"' if SERIF else ''   # the board's own `headlines` tweak (a page that imports it has its own)
        if not mobile:
            body = f"""<footer id="contact"{hl} style="width: 1440px; {height} box-sizing: border-box; display: flex; flex-direction: column; padding: {TOP['d']}px 64px 28px; background: {C['fbg']}; color: {C['ffg']}; {BASE}">
<div style="{GRID12} align-items: start;">
<div style="grid-column: 1 / span 6;">
<h2 style="margin: 0; {TITLE_XL['d']} white-space: nowrap;">Let’s talk</h2>
<p style="margin: 56px 0 0; max-width: {span(4)}px; {LEAD['d']} color: {C['f75']}; text-wrap: balance;">Hiring, briefing, or looking to connect?</p>
</div>
<div style="grid-column: 7 / span 6; margin-top: {FOOT_LIST_TOP}px;">
{link_list(contacts, True, 22, 20, 'Contact', 20)}
</div>
</div>
<div style="flex-grow: 1; min-height: 96px;"></div>
{lower}
</footer>"""
        else:
            body = f"""<footer id="contact"{hl} style="width: 390px; {height} box-sizing: border-box; display: flex; flex-direction: column; padding: {TOP['m']}px 20px 20px; background: {C['fbg']}; color: {C['ffg']}; {BASE}">
<h2 style="margin: 0; {TITLE_XL['m']} white-space: nowrap;">Let’s talk</h2>
<p style="margin: {TEXT['m']}px 0 0; {LEAD['m']} color: {C['f75']};">Hiring, briefing, or looking to connect?</p>
<div style="margin-top: {TITLE_TO_RULE['m']}px;">
{link_list(contacts, True, 19, 16, 'Contact', 18)}
</div>
<div style="flex-grow: 1; min-height: 72px;"></div>
{lower}
</footer>"""
        write(name, dc('Let’s talk footer, ' + ('mobile' if mobile else 'desktop'), body, w, h,
                       HL_PROP or None, HL_SCRIPT if SERIF else None, imported=True))


def menu_boards():
    """The open menu on its own, for the canvas."""
    for mobile in (False, True):
        w, h, links = (390, 844, M_LINKS) if mobile else (1440, 900, D_LINKS)
        body = f"""<div{THEME_ATTR} style="position: relative; width: {w}px; height: {h}px; overflow: hidden; background: {C['bg']}; {BASE}">
{menu_overlay(links, None, mobile, h, doc=True)}
</div>"""
        name = 'NewMenuMobile.dc.html' if mobile else 'NewMenuDesktop.dc.html'
        write(name, dc('Menu open, ' + ('mobile' if mobile else 'desktop'), body, w, h, MENU_PROP, page_script()))


# ── Boards: inner pages ──────────────────────────────────────────────────────────────────────────────────────
def page(name, w, default_h, current, main, mobile=False):
    vh = 844 if mobile else 900
    links = M_LINKS if mobile else D_LINKS
    body = f"""<div id="top" class="me-root{THEME_CLS}" style="position: relative; width: {w}px; {hcss(name, default_h)} display: flex; flex-direction: column; overflow: clip; background: {C['fbg']}; color: {C['fg']}; {BASE}">
<main style="flex-grow: 1; display: flex; flex-direction: column; background: {C['bg']};">
{nav_import(mobile)}
{main}
</main>
{footer_import(mobile)}
{menu_overlay(links, current, mobile, vh)}
</div>"""
    return hval(name, default_h), body


def band(title, mobile=False):
    if not mobile:
        return (f'<div style="padding: {TOP["d"]}px 64px 0;">'
                f'<h1 style="margin: 0; {TITLE_XL["d"]}">{title}</h1></div>')
    return (f'<div style="padding: {TOP["m"]}px 20px 0;">'
            f'<h1 style="margin: 0; {TITLE_XL["m"]}">{title}</h1></div>')


def img(key, alt, ratio):
    return (f'<div style="width: 100%; aspect-ratio: {ratio}; overflow: hidden; background: {C["wash"]};">'
            f'<img src="{BLOB[key]}" alt="{html.escape(alt, quote=True)}" style="display: block; width: 100%; height: 100%; object-fit: cover;"></div>')


ROW_H2 = {'d': sf('font-size: 36px; font-weight: 400; line-height: 1.12; letter-spacing: -0.014em;', '-0.006em', '1.12'),
          'm': sf('font-size: 28px; font-weight: 400; line-height: 1.14; letter-spacing: -0.012em;', '-0.004em', '1.16')}


def rows_d(items):
    """Work pages, desktop: each row opens on a rule. The picture (seven columns) and the title's capitals start level
    with each other, as far below the rule as a headline's capitals sit below its rule on home, and the text starts
    as far again below the title's last baseline (V61: the home spacing, applied everywhere)."""
    lift = round(cap_drop(ROW_H2['d']), 2)          # the title's box starts this far above its capitals
    top = round(HEAD_GAP['d'] + lift, 2)            # rule to picture = rule to the title's capitals
    gap = text_gap(ROW_H2['d'], BODY, 'd')
    out = []
    for i, (title, paras, key, alt) in enumerate(items):
        ps = '\n'.join(f'<p style="margin: {f"{gap}px" if j == 0 else PARA} 0 0; {BODY} color: {C["fg85"]}; text-wrap: pretty;">{keep_compounds(t)}</p>'
                       for j, t in enumerate(paras))
        edge = f'{HEAVY}px solid {C["fg"]}' if i == 0 else f'1px solid {C["rule"]}'
        out.append(f"""<article style="{GRID12} align-items: start; padding-top: {top}px; border-top: {edge};">
<div style="grid-column: 1 / span 7;">{img(key, alt, '1.4 / 1')}</div>
<div style="grid-column: 9 / span 4; margin-top: -{lift}px;">
<h2 style="margin: 0; {ROW_H2['d']} text-wrap: balance;">{title}</h2>
{ps}
</div>
</article>""")
    return '\n'.join(out)


def rows_m(items):
    """Work pages, phone: rule, picture, title and text one space apart. The picture sits as far below the rule, and
    the title's capitals as far below the picture, as the text's capitals sit below the title's last baseline: a
    headline's space on home."""
    space = HEAD_GAP['m'] + cap_drop(ROW_H2['m'])   # the one space, measured to capitals
    gap = text_gap(ROW_H2['m'], BODY, 'm')
    out = []
    for i, (title, paras, key, alt) in enumerate(items):
        ps = '\n'.join(f'<p style="margin: {f"{gap}px" if j == 0 else PARA} 0 0; {BODY} color: {C["fg85"]}; text-wrap: pretty;">{keep_compounds(t)}</p>'
                       for j, t in enumerate(paras))
        edge = f'{HEAVY}px solid {C["fg"]}' if i == 0 else f'1px solid {C["rule"]}'
        out.append(f"""<article style="display: flex; flex-direction: column; gap: {HEAD_GAP['m']}px; padding-top: {round(space, 2)}px; border-top: {edge};">
{img(key, alt, '1.4 / 1')}
<div>
<h2 style="margin: 0; {ROW_H2['m']} text-wrap: balance;">{title}</h2>
{ps}
</div>
</article>""")
    return '\n'.join(out)


# ── Work (V76): three sections, set in type alone ───────────────────────────────────────────────────────────
# Mig's outline (30 Sep 2026) gives the order and the words: Highlights, More Advertising Work, More Editorial Work;
# his titles as written; his links. The page takes Monocle's home page for its model, with The Economist's and
# Wired's habits, in the home page's language (one family, ink and paper, a heavy rule over each section, hairlines
# within), and is built to show the range at once.
# V76 (Mig): no pictures on this page, and a layout no longer bound to their sizes. It reads as a front page and its
# contents. V77 (Mig): placeholder pictures sized to that layout (see WK_PIC), and no section counts:
#   Highlights: the ink band (Wired's), four columns of type abreast, straight under the title, so all four pieces,
#     words and all, are on the first screen;
#   More Advertising Work and More Editorial Work: one index for both, so neither outranks the other: a row a piece,
#     its format, its title and its subhead side by side (a contents page's table), on the band's column lines.
# No piece leads its section. Every subhead is set on the same three-column measure and runs three lines; in the band
# the titles and subheads of the four columns start level (CSS subgrid), and in the rows the format, title and
# subhead share a first baseline. Each label is the piece's format. A piece with one link is that link; one with
# several (Trust Bank's film and cash chamber, the political interviews, the profiles) links the names in its text
# instead. The pictures' keys stay in the data (and Mig's OSC illustration stays uploaded) should pictures return.
from content_v47 import a as ul_link, UL

# V94: Mig's photograph for the OSC launch replaces his V75 illustration ('/_blob/6cbcfbd0bfce08dfced9e5a9c97bf018'), cut
# twice: 5:7 for the home rail, 4:3 for the Work page.
BLOB['work-osc'] = '/_blob/8e47adac2bba0e50734317ebc0d6a01e'      # 1000 x 1400
BLOB['work-osc-43'] = '/_blob/57b09d7b71ce6edc27932743926fa6dd'   # 1200 x 900
ALT['work-osc'] = ALT['work-osc-43'] = 'A hand in the dark, lit by the glow of a phone screen.'

YT = 'https://www.youtube.com/watch?v='
ESQ = 'https://www.esquiremag.ph/'
# fmt: the label over the title (the piece's format). dek: one sentence, no full stop, about three lines on the
# shared measure; {name} marks a link from `links`.
WK = {
    'aam': dict(title='Age Assurance Measures', fmt='Public Service',
                dek='A film, explainers, and ads for the Singapore IMDA, launching age verification in app stores',
                pic='home-age-checks', href=YT + 'HXkZmhEBnBQ'),
    'wiki': dict(title='How to Whitewash a Dictator on Wikipedia', fmt='Investigative Feature',
                 dek='A feature on an invisible war for Philippine history, waged by Wikipedia editors through back-and-forth revisions',
                 pic='home-whitewash', href=ESQ + 'politics/opinion/fighting-for-history-on-the-wikipedia-battlefield-a00207-20170817-lfrm2'),
    'ncii': dict(title='Uncovering Intimate Image Abuse Networks', fmt='Investigative Feature',
                 dek='An exposé that sparked a nationwide reckoning, with a subculture of men sharing NCII across a network of Facebook groups',
                 pic='home-pulpit', href=ESQ + 'long-reads/notes-and-essays/the-rise-of-pastor-culture-and-why-it-must-end-a1513-20170629-lfrm'),
    'osc': dict(title='Online Safety Commission Launch', fmt='Public Service',
                dek='Web copy, service articles, and explainer videos about online harms, for Singapore’s new commission',
                pic='work-osc-43', href='https://www.osc.gov.sg/'),
    'trust': dict(title='Trust Bank Cashback Card Launch', fmt='Integrated Campaign',
                  dek='An award-winning campaign for the iconic Singapore digital bank: {film}, islandwide out-of-home, and {chamber}',
                  links=dict(film=(YT + 'nhxvOzenBR4', 'film'),
                             chamber=('https://advocate.com.sg/portfolio/catch-the-cash/', 'a mobile cash chamber')),
                  pic='ads-trust'),
    'nba': dict(title='NBA Asia-Pacific Weeklies', fmt='Branded Newsletter',
                dek='I wrote the league’s weekly newsletter copy for Australia and New Zealand, Japan, and the Philippines, tuned by market',
                pic='ads-nba'),                                  # no link
    'gotyme': dict(title='GoTyme Bank Philippines Launch', fmt='Integrated Campaign',
                   dek='Copy and concept for a film and three shorts on the human quality of the digital bank’s service',
                   pic='ads-gotyme', href=YT + 'yBnokrkGRbM'),
    'alcon': dict(title='Alcon Contact Lenses', fmt='Brand Campaign',
                  dek='Film and visuals for PRECISION1™ and TOTAL1® developed for markets across the globe',
                  pic='ads-alcon'),                              # link to come
    'politics': dict(title='Politics in Esquire', fmt='Interview Feature',
                     dek='Controversial features on {panelo}, {gordon}, and {uson}, published amid the dawn of online culture wars',
                     links=dict(panelo=(ESQ + 'long-reads/esqa/salvador-panelo-a1513-a1521-20160919-lfrm3', 'Salvador Panelo'),
                                gordon=(ESQ + 'long-reads/what-ive-learned/richard-gordon-what-i-ve-learned-a00207-20170717-lfrm', 'Dick Gordon'),
                                uson=(ESQ + 'long-reads/profiles/mocha-uson-full-text-a1521-20161202-lfrm4', 'Mocha Uson')),
                     pic='ph-politics'),   # V91: Mig's Uson portrait (the Robredo one stays out)
    'eddie': dict(title='Eddie Garcia for Esquire Philippines', fmt='Interview Feature',
                  dek='I wrote and produced Esquire’s biggest and most-viewed celebrity feature ever, on an icon of Filipino cinema’s golden age',
                  pic='editorial-culture', href=YT + 'yY4LLYrMHt8'),
    'tatler': dict(title='Tatler Asia’s Most Influential', fmt='Profiles',
                   dek='Over 100 microprofiles for the 2021 list, including honourees in Singapore and the Philippines',
                   pic='editorial-tatler',
                   href='https://www.tatlerasia.com/power-purpose/ideas-education/art-influence-and-the-purveyors-responsibility-according-to-top-auctioneer-jonathan-crockett'),
    'smile': dict(title='In Basketball Country, An Oasis for Football', fmt='Cover Story',
                  dek='Barotac Nuevo, Iloilo, in the February 2020 issue of Smile, Cebu Pacific Air’s in-flight magazine',
                  pic='editorial-smile',
                  href='https://smile.ink-live.com/html5/reader/production/default.aspx?pubname=&amp;edid=029443cb-cf76-46cf-a91b-5360ee2806f0'),
    'goodmen': dict(title='A Few Good Men', fmt='Profile Series',
                    dek='Purpose-driven entrepreneurs, profiled for Esquire: {pastrana}, {moore}, {motte}, and {delantar}',
                    links=dict(pastrana=(ESQ + 'long-reads/profiles/quintin-pastrana-is-building-the-public-libraries-we-should-already-have-a00207-20171020-lfrm2', 'Quintin Pastrana'),
                               moore=(ESQ + 'long-reads/profiles/a-good-man-roy-moore-a00207-20171117-lfrm2', 'Roy Moore'),
                               motte=(ESQ + 'long-reads/profiles/henry-motte-munoz-a-good-man-a00207-20171026-lfrm', 'Henry Motte-Muñoz'),
                               delantar=(ESQ + 'long-reads/profiles/carlo-delantar-turns-travel-and-adventure-into-humanitarian-missions-for-clean-water-a00207-20171006-lfrm', 'Carlo Delantar')),
                    pic='work-goodmen'),
    'denim': dict(title='The First Filipino Selvedge Denim Label', fmt='Style Feature',
                  dek='The local denimheads behind Léon Denim, the first Filipino-made raw selvedge jeans, for Esquire Philippines',
                  pic='work-denim', href=ESQ + 'style/fashion/local-denimheads-have-produced-the-first-filipino-made-raw-selvedge-jeans-a00207-20171024-lfrm2'),
}
WK_SECTIONS = [('highlights', 'Highlights', ['aam', 'wiki', 'ncii', 'osc']),
               ('advertising', 'More Advertising Work', ['trust', 'nba', 'gotyme', 'alcon']),
               ('editorial', 'More Editorial Work', ['politics', 'eddie', 'tatler', 'smile', 'goodmen', 'denim'])]
W_STRAP = 'Twelve years of stories and campaigns, from Manila to Singapore'   # no full stop, as on Thoughts

# Type for the page's own roles: the band's titles a step above the index's; one subhead size throughout.
WK_T = {'hl_title': {'d': sf('font-size: 32px; font-weight: 400; line-height: 1.1; letter-spacing: -0.016em;', '-0.006em', '1.14'),
                     'm': sf('font-size: 26px; font-weight: 400; line-height: 1.12; letter-spacing: -0.012em;', '-0.004em', '1.18')},
        'row_title': {'d': ROW_H2['m'],
                      'm': sf('font-size: 22px; font-weight: 400; line-height: 1.18; letter-spacing: -0.008em;', '0em', '1.2')},
        'dek': {'d': BODY, 'm': f'font-size: 15px; line-height: 1.55; letter-spacing: {"0.02em" if TYPE_V101 else "0.01em"};'}}
WK_BAND = {'d': dict(top=64, bottom=96), 'm': dict(top=32, bottom=64)}   # the Highlights band: ink over the rule, under the words
# V77: placeholders for every piece, one ratio (4:3) at two sizes, so the pictures keep the sections' ranks: in the
# band, the column's full width (306 x 230); in the index, two columns across (197 x 148), the column after it left
# open so the titles stay on the band's second column line. (Tried and set aside: 'compact', a picture only as tall
# as a subhead's type, 91 x 68, beside the format; at that size the pictures read as icons.) The phone: across the
# measure in the band, 96 px wide below it.
WK_PIC = dict(ratio='4 / 3', rows='wide', row_h=round(F_CAP * 17 + 2 * 17 * 1.65, 2), m_thumb=96)
W_CSS = """a.me-wcard:hover .me-wtitle{text-decoration-line:underline;text-decoration-thickness:1px;text-underline-offset:.14em}
""" + GLOW_CSS   # V104
BOX_CLS = ' me-box' if BOXES and GLOW else ''   # V104: the boxes that light


def w_gap(head, body, optical):
    """Box gap that puts the body's capitals `optical` px under the head's last baseline."""
    return round(optical - base_foot(head) - cap_drop(body), 2)


def w_label(text, k, color=None, extra=''):
    return f'<p style="margin: 0; {LABEL(LABEL_PX[k], color)}{extra}">{text}</p>'


def wk_open(it, style, cls=''):
    """A piece with one link is that link; one with several links (in its text) or none is a plain block."""
    h = it.get('href')
    if h:
        return f'<a class="me-wcard{cls}" href="{h}" target="_blank" rel="noopener" style="{style} {NOUL}">', '</a>'
    return f'<div class="me-wcard{cls}" style="{style}">', '</div>'


def wk_dek(it, band=False):
    """The subhead, its names linked where a piece has several links (the site's underline; on the band, paper's)."""
    style = UL.replace('var(--ul)', C['frule']) if band else UL
    text = it['dek']
    if it.get('links'):
        text = text.format(**{n: ul_link(h, t.replace(' ', ' '), style=style) for n, (h, t) in it['links'].items()})   # a name stays whole
    return keep_compounds(text)


def wk_colors(band):
    """(title, label, subhead, divider, rule) on the band or on paper."""
    return (C['ffg'], C['f70'], C['f75'], C['frule'], C['frule']) if band else (C['fg'], C['fg70'], C['fg85'], C['fg'], C['rule'])


def wk_head(name, k, band=False):
    """A section opens on a heavy rule, its name under it in a label (V77: no count)."""
    fg, ink = (C['ffg'], C['fbg']) if band else (C['fg'], C['bg'])
    # V82: the capitals sit a touch above the box's middle (optical centre): 2px up on a desktop, 1.5px on a phone
    fs, pad = (14, '6px 14px 9px') if k == 'd' else (12, '5.5px 11px 7.5px')
    return (f'<div aria-hidden="true" style="border-top: {HEAVY}px solid {fg};"></div>\n'
            f'<h2 style="margin: 0; width: fit-content; padding: {pad}; background: {fg}; font-weight: 400; font-size: {fs}px; line-height: 1.2; '
            f'letter-spacing: 0.08em; text-transform: uppercase; color: {ink};">{name}</h2>')


def wk_ph(ratio, band=False, width=None):
    """A picture to come: a flat tone of the text colour over the ground (on the band, the band's own), no label."""
    bg = f'color-mix(in srgb, {C["ffg"]} 9%, transparent)' if band else C['wash']
    w = f' width: {width}px; flex-shrink: 0;' if width else ''
    return f'<div aria-hidden="true" style="aspect-ratio: {ratio};{w} background: {bg};"></div>'


# V89: the pictures Mig has supplied go into the slots; the rest keep the flat placeholder. Portrait sources are
# cropped to 4:3 at these heights (object-position y, %); landscape ones are 4:3 already.
WK_POS = {'home-age-checks': 35, 'home-whitewash': 25, 'home-pulpit': 40, 'ph-politics': 8}


def wk_pic(it, ratio, band=False, width=None):
    key = it.get('pic')
    if not key or key not in BLOB:
        return wk_ph(ratio, band, width)
    bg = f'color-mix(in srgb, {C["ffg"]} 9%, transparent)' if band else C['wash']
    w = f' width: {width}px; flex-shrink: 0;' if width else ''
    return (f'<div style="aspect-ratio: {ratio};{w} overflow: clip; background: {bg};">'
            f'<img src="{BLOB[key]}" alt="{html.escape(ALT[key], quote=True)}" draggable="false" '
            f'style="display: block; width: 100%; height: 100%; object-fit: cover; object-position: 50% {WK_POS.get(key, 50)}%;"></div>')


def wk_masthead(k):
    if k == 'd':
        return f"""<div style="padding: {TOP['d']}px 64px 0;">
<div style="{GRID12} align-items: end;">
<h1 style="grid-column: 1 / span 6; margin: 0; {TITLE_XL['d']} white-space: nowrap;">Work</h1>
<p style="grid-column: 7 / span 4; margin: 0 0 {THOUGHTS_SUB_DROP}px; {LEAD['d']} color: {C['fg75']}; text-wrap: balance;">{W_STRAP}</p>
</div>
</div>"""
    return f"""<div style="padding: {TOP['m']}px 20px 0;">
<h1 style="margin: 0; {TITLE_XL['m']}">Work</h1>
<p style="margin: {TEXT['m']}px 0 0; {LEAD['m']} color: {C['fg75']}; text-wrap: balance;">{W_STRAP}</p>
</div>"""


def wk_cards_d(keys, band):
    """Desktop, Highlights: four columns abreast, three grid columns each: a 4:3 picture, the format, the title, the
    subhead. The columns share the row's tracks (subgrid), so their titles and subheads start level; hairlines run
    between them."""
    fg, lab, dc, div, _ = wk_colors(band)
    t, d = WK_T['hl_title']['d'], WK_T['dek']['d']
    cards = []
    for i, key in enumerate(keys):
        it = WK[key]
        o, c = wk_open(it, 'grid-column: span 3; grid-row: span 4; display: grid; grid-template-rows: subgrid; position: relative;')
        rule = (f'<span aria-hidden="true" style="position: absolute; top: 0; bottom: 0; right: -12.5px; width: 1px; background: {div};"></span>'
                if i < len(keys) - 1 else '')
        cards.append(f'{o}{rule}{wk_pic(it, WK_PIC["ratio"], band)}'
                     f'<p style="margin: 18px 0 0; {LABEL(LABEL_PX["d"], lab)}">{it["fmt"]}</p>'
                     f'<h3 class="me-wtitle" style="margin: 10px 0 0; {t} color: {fg}; text-wrap: balance;">{keep_compounds(bind_hl(it["title"]))}</h3>'
                     f'<p style="margin: {w_gap(t, d, 20)}px 0 0; {d} color: {dc}; text-wrap: pretty;">{wk_dek(it, band)}</p>{c}')
    return (f'<div style="{GRID12} grid-template-rows: repeat(4, auto); row-gap: 0; margin-top: {BLOCK["d"]}px;">\n'
            + '\n'.join(cards) + '\n</div>')


def wk_rows_d(keys, band=False):
    """Desktop, Advertising and Editorial: an index, a row a piece on hairlines, on the band's column lines. Each row
    hangs from one line: the picture's top edge and the capitals of the format, the title and the subhead's first
    line. 'compact': a small 4:3 picture as tall as the subhead's type (its first capitals to its last baseline), the
    format beside it in the first three columns, the title in the next six, the subhead in the last three. 'wide': the
    picture fills the first two columns and the format rides above the title."""
    fg, lab, dc, _, rule = wk_colors(band)
    t, d, L = WK_T['row_title']['d'], WK_T['dek']['d'], LABEL(LABEL_PX['d'], lab)
    up = lambda css: f'margin-top: -{round(cap_drop(css), 2)}px;'
    rows = []
    for i, key in enumerate(keys):
        it = WK[key]
        last = i == len(keys) - 1
        o, c = wk_open(it, f'{GRID12} align-items: start; padding: 28px 0 28px; border-top: 1px solid {rule};'
                           + (f' border-bottom: 1px solid {rule};' if last else ''))
        title = f'<h3 class="me-wtitle" style="margin: 0; {t} color: {fg}; text-wrap: balance;">{keep_compounds(bind_hl(it["title"]))}</h3>'
        dek = f'<p style="grid-column: 10 / span 3; margin: 0; {up(d)} {d} color: {dc}; text-wrap: pretty;">{wk_dek(it, band)}</p>'
        if WK_PIC['rows'] == 'compact':
            h = WK_PIC['row_h']
            rows.append(f'{o}<div style="grid-column: 1 / span 3; display: flex; gap: 20px; align-items: flex-start;">'
                        f'{wk_ph(WK_PIC["ratio"], band, round(h * 4 / 3, 2))}<p style="margin: 0; {up(L)} {L}">{it["fmt"]}</p></div>'
                        f'<div style="grid-column: 4 / span 6; {up(t)}">{title}</div>{dek}{c}')
        else:
            rows.append(f'{o}<div style="grid-column: 1 / span 2;">{wk_pic(it, WK_PIC["ratio"], band)}</div>'
                        f'<div style="grid-column: 4 / span 6; {up(L)}"><p style="margin: 0; {L}">{it["fmt"]}</p>'
                        f'<div style="margin-top: 10px;">{title}</div></div>{dek}{c}')
    return f'<div style="margin-top: {BLOCK["d"]}px;">\n' + '\n'.join(rows) + '\n</div>'


# V112 (Mig: "a little tight"): the phone's Work boxes get more air, up and down. They had the Home rail's small-card
# spacing (12px inside, 12px apart) around much larger type, a 26px title over a 15px subhead, so a title all but ran
# into its subhead and the boxes into one another. Now the boxes stand 20px apart (the page's margin, so the stack keeps
# the page's rhythm); a subhead's capitals sit 18px under a big title's last baseline (14 before; the desktop has 18)
# and 16px under a small entry's picture and title (14 before); and the box closes 16px under its last line (12
# before). The sides and the small picture's inset stay at 12px, so no title rewraps (two would have at 16).
# WK_M_AIR = False puts V103's spacing back.
WK_M_AIR = True
WK_M = (dict(pad=BOX['pad']['m'], bottom=16, gap=20, dek_big=18, dek_row=16) if WK_M_AIR else
        dict(pad=BOX['pad']['m'], bottom=BOX['pad']['m'], gap=BOX['gap']['m'], dek_big=14, dek_row=14))


def wk_item_m(it, t, band=False, big=False, inner=0):
    """A phone entry. In the band (big): the 4:3 picture across the measure, then format, title and subhead. Below it:
    a small 4:3 picture beside the format and title, the subhead under both at the full measure."""
    fg, lab, dc, _, _ = wk_colors(band)
    d = WK_T['dek']['m']
    o, c = wk_open(it, 'display: block;')
    head = (f'{w_label(it["fmt"], "m", lab)}'
            f'<h3 class="me-wtitle" style="margin: 8px 0 0; {t} color: {fg}; text-wrap: balance;">{keep_compounds(bind_hl(it["title"]))}</h3>')
    dek = f'<p style="margin: {w_gap(t, d, WK_M["dek_big"])}px 0 0; {d} color: {dc}; text-wrap: pretty;">{wk_dek(it, band)}</p>'
    if big:
        if inner:   # V103: the picture to the box's edges, the words inside its padding
            return (f'{o}{wk_pic(it, WK_PIC["ratio"], band)}<div style="padding: 0 {inner}px;"><div style="margin-top: 16px;">{head}</div>{dek}</div>{c}')
        return f'{o}{wk_pic(it, WK_PIC["ratio"], band)}<div style="margin-top: 16px;">{head}</div>{dek}{c}'
    lift = round(cap_drop(LABEL(LABEL_PX['m'])), 2)
    return (f'{o}<div style="display: flex; gap: 16px; align-items: flex-start;">{wk_pic(it, WK_PIC["ratio"], band, WK_PIC["m_thumb"])}'
            f'<div style="flex: 1; min-width: 0; margin-top: -{lift}px;">{head}</div></div>'
            f'<p style="margin: {WK_M["dek_row"]}px 0 0; {d} color: {dc}; text-wrap: pretty;">{wk_dek(it, band)}</p>{c}')


def wk_list_m(keys, t, band=False, big=False):
    """Phone: the entries on hairlines, the list closed by one (V103: each entry a box, a short gap apart)."""
    rule = wk_colors(band)[4]
    if BOXES and not band:
        bp, g, bb = WK_M['pad'], WK_M['gap'], WK_M['bottom']   # V112
        flush = big and BOX['flush']
        cls = f' class="{BOX_CLS.strip()}"' if BOX_CLS else ''   # V104
        return (f'<div style="margin-top: {BLOCK["m"]}px; display: flex; flex-direction: column; gap: {g}px;">' + ''.join(
            f'<div{cls} style="{box_css()} padding: {"0 0 " + str(bb - TEXT_TAIL) + "px" if flush else str(bp) + "px " + str(bp) + "px " + str(bb - TEXT_TAIL) + "px"};">'
            f'{wk_item_m(WK[key], t, band, big, inner=bp if flush else 0)}</div>' for key in keys) + '</div>')
    return (f'<div style="margin-top: {BLOCK["m"]}px;">' + ''.join(
        f'<div style="border-top: 1px solid {rule}; padding: 20px 0 {24 - TEXT_TAIL}px;{" border-bottom: 1px solid " + rule + ";" if i == len(keys) - 1 else ""}">'
        f'{wk_item_m(WK[key], t, band, big)}</div>' for i, key in enumerate(keys)) + '</div>')


def wk_section(k, sid, name, keys):
    """Highlights sits in the ink band, straight under the title; the other two open on paper a full break apart."""
    pad = '64px' if k == 'd' else '20px'
    if sid == 'highlights':
        b = WK_BAND[k]
        body = wk_cards_d(keys, True) if k == 'd' else wk_list_m(keys, WK_T['hl_title']['m'], True, big=True)
        return (f'<section id="{sid}" class="me-wband" style="margin-top: {TITLE_TO_RULE[k]}px; padding: {b["top"]}px {pad} {b["bottom"]}px; '
                f'background: {C["fbg"]}; color: {C["ffg"]};">\n{wk_head(name, k, band=True)}\n{body}\n</section>')
    last = sid == WK_SECTIONS[-1][0]
    body = wk_rows_d(keys) if k == 'd' else wk_list_m(keys, WK_T['row_title']['m'])
    return (f'<section id="{sid}" style="padding: {SECTION[k]}px {pad} {PAGE_BOTTOM[k] if last else 0}px;">\n'
            f'{wk_head(name, k)}\n{body}\n</section>')


# ── V100: the Work page after Monocle and The Economist ─────────────────────────────────────────────────────────
# Out: the ink band and the Wired signposts (a heavy rule with the name in a black box). In: one paper page, every
# section opening on a hairline in the text colour with its name under it at a subhead's size, as the two papers do
# it. Highlights: four abreast, a 4:3 picture over each piece (as The Economist's front page lines up its top
# stories). The other two: a contents page in two columns, a piece to each half, the 4:3 picture at the left of its
# words, hairlines between the rows (Monocle's contents). Same pieces, pictures, ratios and words. WK_STYLE = 'wired'
# puts V99 back.
WK_STYLE = 'press'
WP = {'name': {'d': ROW_H2['d'], 'm': sf('font-size: 28px; font-weight: 400; line-height: 1.12; letter-spacing: -0.012em;', '-0.004em', '1.16')},
      'name_gap': {'d': 16, 'm': 12},       # hairline to the name's box
      'body_gap': {'d': 48, 'm': 28},       # the name to the first piece
      'hl_title': sf('font-size: 26px; font-weight: 400; line-height: 1.14; letter-spacing: -0.01em;', '-0.004em', '1.18'),
      'row_title': sf('font-size: 24px; font-weight: 400; line-height: 1.16; letter-spacing: -0.008em;', '-0.002em', '1.2'),
      'row_pad': 24}


def wp_head(name, k):
    return (f'<div aria-hidden="true" style="border-top: 1px solid {C["fg"]};"></div>\n'
            f'<h2 style="margin: {WP["name_gap"][k]}px 0 0; {WP["name"][k]} color: {C["fg"]};">{name}</h2>')


def wp_cards_d(keys):
    """Highlights, desktop: four abreast, three columns each: picture, format, title, subhead. The four share their
    rows (subgrid), so the titles and the subheads start level."""
    t, d, L = WP['hl_title'], WK_T['dek']['d'], LABEL(LABEL_PX['d'], C['fg70'])
    bp = BOX['pad']['d']
    # V103: each a box, the picture to its edges (or inside the padding), the words inside the padding
    box, side, last, pic_pad = ((box_css(), f' padding: 0 {bp}px;', f' padding: 0 {bp}px {bp}px;', '' if BOX['flush'] else f'padding: {bp}px {bp}px 0;')
                                if BOXES else ('', '', '', ''))
    cards = []
    for key in keys:
        it = WK[key]
        o, c = wk_open(it, f'grid-column: span 3; grid-row: span 4; display: grid; grid-template-rows: subgrid;{" " + box if box else ""}', BOX_CLS)
        pic = f'<div style="{pic_pad}">{wk_pic(it, WK_PIC["ratio"])}</div>' if pic_pad else wk_pic(it, WK_PIC["ratio"])
        cards.append(f'{o}{pic}'
                     f'<p style="margin: 20px 0 0;{side} {L}">{it["fmt"]}</p>'
                     f'<h3 class="me-wtitle" style="margin: 10px 0 0;{side} {t} color: {C["fg"]}; text-wrap: balance;">{keep_compounds(bind_hl(it["title"]))}</h3>'
                     f'<p style="margin: {w_gap(t, d, 18)}px 0 0;{last} {d} color: {C["fg85"]}; text-wrap: pretty;">{wk_dek(it)}</p>{c}')
    return (f'<div style="{GRID12} grid-template-rows: repeat(4, auto); row-gap: 0; margin-top: {WP["body_gap"]["d"]}px;">\n'
            + '\n'.join(cards) + '\n</div>')


def wp_rows_d(keys):
    """Advertising and Editorial, desktop: a contents page in two columns, a piece to each half (six columns): the
    picture across two, the format, title and subhead across four, hung from the picture's top edge. Hairlines run
    over each row and under the last, a gutter apart where the halves meet."""
    t, d, L = WP['row_title'], WK_T['dek']['d'], LABEL(LABEL_PX['d'], C['fg70'])
    up = lambda css: f'margin-top: -{round(cap_drop(css), 2)}px;'
    n = len(keys)
    last_row = (n - 1) // 2
    out = []
    for i, key in enumerate(keys):
        it = WK[key]
        bottom = f' border-bottom: 1px solid {C["rule"]};' if i // 2 == last_row else ''
        edges = (f'padding: {BOX["pad"]["d"]}px; {box_css()}' if BOXES else
                 f'padding: {WP["row_pad"]}px 0 {WP["row_pad"] + 4}px; border-top: 1px solid {C["rule"]};{bottom}')
        o, c = wk_open(it, f'grid-column: span 6; display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); column-gap: 24px; '
                           f'align-items: start; {edges}', BOX_CLS)
        out.append(f'{o}<div style="grid-column: 1 / span 2;">{wk_pic(it, WK_PIC["ratio"])}</div>'
                   f'<div style="grid-column: 3 / span 4; {up(L)}"><p style="margin: 0; {L}">{it["fmt"]}</p>'
                   f'<h3 class="me-wtitle" style="margin: 10px 0 0; {t} color: {C["fg"]}; text-wrap: balance;">{keep_compounds(bind_hl(it["title"]))}</h3>'
                   f'<p style="margin: {w_gap(t, d, 16)}px 0 0; {d} color: {C["fg85"]}; text-wrap: pretty;">{wk_dek(it)}</p></div>{c}')
    gap = f' row-gap: {BOX["gap"]["d"]}px;' if BOXES else ''
    return (f'<div style="{GRID12}{gap} margin-top: {WP["body_gap"]["d"]}px;">\n' + '\n'.join(out) + '\n</div>')


def wp_section(k, sid, name, keys):
    pad = '64px' if k == 'd' else '20px'
    first, last = sid == WK_SECTIONS[0][0], sid == WK_SECTIONS[-1][0]
    if k == 'd':
        body = wp_cards_d(keys) if first else wp_rows_d(keys)
    else:
        t = WK_T['hl_title']['m'] if first else WK_T['row_title']['m']
        body = wk_list_m(keys, t, False, big=first).replace(f'margin-top: {BLOCK["m"]}px;', f'margin-top: {WP["body_gap"]["m"]}px;', 1)
    top = TITLE_TO_RULE[k] if first else SECTION[k]
    return (f'<section id="{sid}" style="padding: {top}px {pad} {PAGE_BOTTOM[k] if last else 0}px;">\n'
            f'{wp_head(name, k)}\n{body}\n</section>')


def work_pages():
    """The one Work page, desktop and phone (V74: Mig's three sections; V75: no leads, Highlights in the band;
    V76: no pictures)."""
    for mobile in (False, True):
        k = 'm' if mobile else 'd'
        name = 'NewWorkMobile.dc.html' if mobile else 'NewWork.dc.html'
        sect = wp_section if WK_STYLE == 'press' else wk_section
        main = '\n'.join([wk_masthead(k)] + [sect(k, sid, label, keys) for sid, label, keys in WK_SECTIONS])
        h, body = page(name, 390 if mobile else 1440, 4200 if mobile else 3000, 'Work', main, mobile=mobile)
        write(name, dc('Work' + (', mobile' if mobile else ''), body, 390 if mobile else 1440, h, THEME_PROP, page_script(), extra_css=W_CSS))


def thoughts_block(links, mobile):
    date, title = ENTRY
    if not mobile:
        return f"""<div style="{GRID12} align-items: end;">
<h1 style="grid-column: 1 / span 6; margin: 0; {TITLE_XL['d']} white-space: nowrap;">{THOUGHTS_TITLE}</h1>
<p style="grid-column: 7 / span 4; margin: 0 0 {THOUGHTS_SUB_DROP}px; {LEAD['d']} color: {C['fg75']}; text-wrap: balance;">{THOUGHTS_SUB}</p>
</div>
<div style="margin-top: {TITLE_TO_RULE['d']}px; border-top: {HEAVY}px solid {C['fg']};">
<a class="entry" href="{links['ThoughtPost']}" style="{GRID12} align-items: baseline; padding: 40px 0 46px; border-bottom: 1px solid {C['rule']}; {NOUL}">
<time datetime="2026-08" style="grid-column: 1 / span 2; {LABEL(LABEL_PX['d'])}">{date}</time>
<h2 class="entry-title" style="grid-column: 7 / span 6; margin: 0; {H2['d']} text-wrap: balance; opacity: 0.62; transition: opacity 0.35s ease;">{bind_hl(title)}</h2>
</a>
</div>"""
    return f"""<h1 style="margin: 0; {TITLE_XL['m']}">{THOUGHTS_TITLE}</h1>
<p style="margin: {TEXT['m']}px 0 0; {LEAD['m']} color: {C['fg75']}; text-wrap: balance;">{THOUGHTS_SUB}</p>
<div style="margin-top: {LEAD_TO_RULE_M}px; border-top: {HEAVY}px solid {C['fg']};">
<a class="entry" href="{links['ThoughtPost']}" style="display: flex; flex-direction: column; gap: 12px; padding: 24px 0 28px; border-bottom: 1px solid {C['rule']}; {NOUL}">
<time datetime="2026-08" style="{LABEL(LABEL_PX['m'])}">{date}</time>
<h2 class="entry-title" style="margin: 0; {H2['m']} text-wrap: balance; opacity: 0.62; transition: opacity 0.35s ease;">{bind_hl(title)}</h2>
</a>
</div>"""


def thoughts_pages():
    name = 'NewThoughts.dc.html'
    main = f'<section style="flex-grow: 1; padding: {TOP["d"]}px 64px {PAGE_BOTTOM["d"]}px;">\n{thoughts_block(D_LINKS, False)}\n</section>'
    h, body = page(name, 1440, 1700, 'Thoughts', main)
    write(name, dc('Thoughts', body, 1440, h, THEME_PROP, page_script()))
    name = 'NewThoughtsMobile.dc.html'
    main = f'<section style="flex-grow: 1; padding: {TOP["m"]}px 20px {PAGE_BOTTOM["m"]}px;">\n{thoughts_block(M_LINKS, True)}\n</section>'
    h, body = page(name, 390, 1400, 'Thoughts', main, mobile=True)
    write(name, dc('Thoughts, mobile', body, 390, h, THEME_PROP, page_script()))


def post_pages():
    ps = '\n'.join(f'<p style="margin: {"0" if i == len(POST_PARAS) - 1 else "0 0 " + PARA};">{keep_compounds(html.escape(t, quote=False))}</p>'
                   for i, t in enumerate(POST_PARAS))
    name = 'NewThoughtPost.dc.html'
    main = f"""<header style="{GRID12} padding: {LABEL_TOP['d']}px 64px 0;">
<div style="grid-column: 5 / span 8;">
<p style="margin: 0; {LABEL(LABEL_PX['d'])}"><time datetime="2026-08-24">24 August 2026</time></p>
<h1 style="margin: {LABEL_GAP['d']}px 0 0; {H2['d']} text-wrap: balance;{HANG}">{bind_hl(POST_TITLE)}</h1>
<p style="margin: {TEXT['d']}px 0 0; max-width: 30em; {LEAD['d']} color: {C['fg75']}; text-wrap: balance;">{POST_DECK}</p>
</div>
</header>
<article style="{GRID12} padding: 88px 64px {PAGE_BOTTOM['d'] - TEXT_TAIL}px;">
<div style="grid-column: 5 / span 5; {BODY} color: {C['fg85']};">
{ps}
</div>
</article>"""
    h, body = page(name, 1440, 3600, 'Thoughts', main)
    write(name, dc('Thought post', body, 1440, h, THEME_PROP, page_script()))
    name = 'NewThoughtPostMobile.dc.html'
    main = f"""<header style="padding: {LABEL_TOP['m']}px 20px 0;">
<p style="margin: 0; {LABEL(LABEL_PX['m'])}"><time datetime="2026-08-24">24 August 2026</time></p>
<h1 style="margin: {LABEL_GAP['m']}px 0 0; {H2['m']} text-wrap: balance;{HANG}">{bind_hl(POST_TITLE)}</h1>
<p style="margin: {TEXT['m']}px 0 0; {LEAD['m']} color: {C['fg75']}; text-wrap: balance;">{POST_DECK}</p>
</header>
<article style="padding: 44px 20px {PAGE_BOTTOM['m'] - TEXT_TAIL}px; {BODY} color: {C['fg85']};">
{ps}
</article>"""
    h, body = page(name, 390, 5200, 'Thoughts', main, mobile=True)
    write(name, dc('Thought post, mobile', body, 390, h, THEME_PROP, page_script()))


def notfound_pages():
    def links(lk, mobile):
        items = [(lk['home'], 'Home'), (lk['Work'], 'Work'), (lk['Thoughts'], 'Thoughts')]
        return link_list(items, False, 19 if mobile else 22, 16 if mobile else 20, 'Helpful links', 18 if mobile else 20)
    name = 'NewNotFound.dc.html'
    main = f"""<section style="flex-grow: 1; padding: {LABEL_TOP['d']}px 64px {PAGE_BOTTOM['d']}px;">
<p style="margin: 0; {LABEL(LABEL_PX['d'])}">Error 404</p>
<h1 style="margin: {LABEL_GAP['d']}px 0 0; {TITLE_XL['d']}">Page not found</h1>
<div style="{GRID12} align-items: start; margin-top: {NF_GRID_TOP}px;">
<p style="grid-column: 1 / span 5; margin: -{NF_LEAD_LIFT}px 0 0; {LEAD['d']} color: {C['fg75']}; text-wrap: balance;">The page you’re looking for doesn’t exist or may have moved.</p>
<div style="grid-column: 7 / span 6;">
{links(D_LINKS, False)}
</div>
</div>
</section>"""
    h, body = page(name, 1440, 1700, None, main)
    write(name, dc('404', body, 1440, h, THEME_PROP, page_script()))
    name = 'NewNotFoundMobile.dc.html'
    main = f"""<section style="flex-grow: 1; padding: {LABEL_TOP['m']}px 20px {PAGE_BOTTOM['m']}px;">
<p style="margin: 0; {LABEL(LABEL_PX['m'])}">Error 404</p>
<h1 style="margin: {NF_TITLE_TOP_M if SERIF else LABEL_GAP['m']}px 0 0; {TITLE_XL['m2']}">Page not found</h1>
<p style="margin: {NF_LEAD_TOP_M if SERIF else TEXT['m']}px 0 0; {LEAD['m']} color: {C['fg75']}; text-wrap: balance;">The page you’re looking for doesn’t exist or may have moved.</p>
<div style="margin-top: {LEAD_TO_RULE_M}px;">
{links(M_LINKS, True)}
</div>
</section>"""
    h, body = page(name, 390, 1300, None, main, mobile=True)
    write(name, dc('404, mobile', body, 390, h, THEME_PROP, page_script()))


# ═════════════════════════════════════════════════════════════════════════════════════════════════════════════
nav_boards(); footer_boards(); menu_boards()
home_boards(); dark_previews()
work_pages(); thoughts_pages(); post_pages(); notfound_pages()

# Sanity checks: markup balance, link and import targets.
existing = {f for f in os.listdir(P) if f.endswith('.dc.html')}
for n, t in FILES.items():
    for imp in re.findall(r'<dc-import name="([^"]+)"', t):
        assert imp + '.dc.html' in existing, (n, imp)
    for href in re.findall(r'href="([^"#]+\.dc\.html)"', t):
        assert href in existing, (n, href)
    assert t.count('<a ') == t.count('</a>'), n
    for tag in ['div', 'section', 'article', 'p', 'h1', 'h2', 'nav', 'main', 'header', 'footer', 'span', 'button', 'time', 'video']:
        o = len(re.findall(rf'<{tag}[\s>]', t)); c = t.count(f'</{tag}>')
        assert o == c, (n, tag, o, c)
    assert 'JetBrains' not in t and 'Newsreader' not in t, n
    # no blue, nor what served it (V62: bar the Policy stage's own blue, in its custom property)
    tb = re.sub(r'--pol-blue:#0047BB;', '', t) if POLICY_FX else t
    assert not re.search(r'0047bb|5e87ca|me-onblue|me-ch-box|me-ch-first', tb, re.I), n
json.dump(sorted(FILES), open(os.path.join(SCR, 'redesign_files.json'), 'w'))
print(len(FILES), 'redesign artboards written', '(measure mode)' if MEASURE else '')
