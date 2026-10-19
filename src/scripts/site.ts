// Site-wide behaviour (every page, from BaseLayout): the month on Home's
// dateline, reveals, statements that fill in as they're read, the section that
// holds while it's read, and weighted scrolling. The magazines are thrown by
// MagStack.astro, and Home's reel is driven from index.astro.
const root = document.documentElement;
root.classList.add('js-ready');
const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const clamp = (v: number) => (v < 0 ? 0 : v > 1 ? 1 : v);

// ── The month on Home's dateline: Singapore's (UTC+8, no daylight saving),
// "Oct 2026", set in capitals by the CSS. The page carries the month it was
// built in; this keeps it current. ──
const issues = document.querySelectorAll<HTMLTimeElement>('[data-issue]');
if (issues.length) {
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const tick = () => {
    const d = new Date(Date.now() + 8 * 3600 * 1000);
    const text = `${MON[d.getUTCMonth()]} ${d.getUTCFullYear()}`;
    const iso = `${d.getUTCFullYear()}-${String(d.getUTCMonth() + 1).padStart(2, '0')}`;
    issues.forEach((el) => {
      if (el.textContent !== text) el.textContent = text;
      if (el.getAttribute('datetime') !== iso) el.setAttribute('datetime', iso);
    });
  };
  tick();
  setInterval(tick, 60000);
}

// The nav's resting height (its line, from the top), which the page keeps
// clear of when it parks a section or glides to a link.
const nav = document.querySelector<HTMLElement>('[data-nav]');
const navh = () => (nav ? nav.offsetHeight : 0);

// ── Reveals: each part comes into play once, when its top is this far up the
// screen; anything already scrolled past counts as in. Parts in a row that
// scrolls sideways ([data-rv-row]: Home's cards on the phone) arrive together,
// as the row comes up the screen, not one by one as they're swiped into view. ──
const reveal = (selector: string, percent: number) => {
  const els = Array.from(document.querySelectorAll<HTMLElement>(selector));
  if (!els.length) return;
  if (reduce || !('IntersectionObserver' in window)) {
    els.forEach((el) => el.classList.add('is-in'));
    return;
  }
  const io = new IntersectionObserver(
    (entries) => {
      for (const en of entries) {
        if (en.isIntersecting || en.boundingClientRect.top < 0) {
          const t = en.target as HTMLElement;
          const parts = t.hasAttribute('data-rv-row') ? t.querySelectorAll<HTMLElement>(selector) : [t];
          parts.forEach((el) => el.classList.add('is-in'));
          io.unobserve(t);
        }
      }
    },
    { rootMargin: `0px 0px -${percent}% 0px` }
  );
  const watched = new Set<HTMLElement>();
  els.forEach((el) => watched.add(el.closest<HTMLElement>('[data-rv-row]') || el));
  watched.forEach((t) => io.observe(t));
};
reveal('[data-rv]', 10);
reveal('[data-rise]', 8);
reveal('[data-frame]', 22);

// ── Statements that fill in as they're read (--wp, 0 to 1), and sections that
// hold in place while they're read (Home's last): the stage parks with its words
// in the middle of the screen under the nav, for as long as the section runs on
// below it. Not with reduced motion, nor where the words wouldn't fit. ──
type Hold = HTMLElement & { holdStage?: number; holdTop?: number };
const words = Array.from(document.querySelectorAll<HTMLElement>('[data-words]'));
const holds = Array.from(document.querySelectorAll<Hold>('[data-hold]'));

// The screen's height with the browser's bars showing (100svh), which doesn't
// change as they come and go, so the parked words don't jump.
let probe: HTMLElement | null = null;
const svh = () => {
  if (!probe) {
    probe = document.createElement('div');
    probe.setAttribute('aria-hidden', 'true');
    probe.style.cssText =
      'position:fixed;top:0;left:0;width:0;height:100vh;height:100svh;visibility:hidden;pointer-events:none';
    document.body.appendChild(probe);
  }
  return probe.offsetHeight || window.innerHeight;
};

const fitHolds = () => {
  if (reduce || !holds.length) return;
  const room = svh() - navh();
  holds.forEach((el) => {
    const stage = el.querySelector<HTMLElement>('[data-hold-stage]');
    if (!stage) return;
    el.classList.add('is-hold');
    const cs = getComputedStyle(stage);
    const pt = parseFloat(cs.paddingTop) || 0;
    const sh = stage.offsetHeight;
    const ch = sh - pt - (parseFloat(cs.paddingBottom) || 0);
    if (pt + ch + 16 > room) {
      el.classList.remove('is-hold');
      return;
    }
    // Its height, for the CSS that parks it (home.css); then where that is.
    stage.style.setProperty('--hold-h', `${sh}px`);
    el.holdStage = sh;
    el.holdTop = parseFloat(getComputedStyle(stage).top) || navh();
  });
};
fitHolds();

let queued = false;
const frame = () => {
  queued = false;
  const vh = window.innerHeight;
  words.forEach((el) => {
    let p: number;
    const hold = el.closest<Hold>('[data-hold]');
    if (reduce) p = 1;
    else if (hold && hold.classList.contains('is-hold')) {
      // Filled by halfway through the hold, from a little before it starts;
      // then it stays, whole, for the rest.
      const hr = hold.getBoundingClientRect();
      const run = hr.height - (hold.holdStage ?? 0);
      p = clamp(((hold.holdTop ?? 0) + vh * 0.3 - hr.top) / (run * 0.5 + vh * 0.3));
    } else {
      const r = el.getBoundingClientRect();
      p = clamp((vh * 0.88 - r.top) / (r.height + vh * 0.38));
    }
    el.style.setProperty('--wp', p.toFixed(4));
  });
};
const queue = () => {
  if (!queued) {
    queued = true;
    requestAnimationFrame(frame);
  }
};
window.addEventListener('scroll', queue, { passive: true });
window.addEventListener('resize', () => {
  fitHolds();
  queue();
});
if (holds.length && document.fonts?.ready) {
  document.fonts.ready.then(() => {
    fitHolds();
    queue();
  });
}
frame();

// ── Smooth scrolling, with weight: the wheel sets a target and the page eases
// towards it (7.5% of the way each frame, at any frame rate). Same-page links
// glide the same way. Touch screens keep their own momentum; keys, scrollbars
// and find-in-page stay native; reduced motion, off. ──
if (!reduce && !window.matchMedia('(hover: none) and (pointer: coarse)').matches) {
  root.classList.add('has-smooth');
  const LERP = 0.075;
  let target = window.scrollY;
  let current = target;
  let running = false;
  let last = 0;
  const setY = (y: number) => window.scrollTo({ top: y, behavior: 'instant' });
  const maxY = () => Math.max(0, Math.max(root.scrollHeight, document.body.scrollHeight) - window.innerHeight);
  const tick = (now: number) => {
    const dt = last ? Math.min(64, now - last) : 16.7;
    last = now;
    const k = 1 - Math.pow(1 - LERP, dt / 16.7);
    current += (target - current) * k;
    if (Math.abs(target - current) < 0.35) {
      current = target;
      running = false;
    }
    setY(current);
    if (running) requestAnimationFrame(tick);
    else last = 0;
  };
  const glide = (y: number) => {
    if (!running) current = window.scrollY;
    target = Math.max(0, Math.min(maxY(), y));
    if (!running) {
      running = true;
      requestAnimationFrame(tick);
    }
  };
  // A scroller inside the page that can still move this way keeps the wheel.
  const nested = (node: EventTarget | null, dy: number) => {
    for (let el = node as HTMLElement | null; el && el.nodeType === 1 && el !== document.body && el !== root; el = el.parentElement) {
      const oy = getComputedStyle(el).overflowY;
      if ((oy === 'auto' || oy === 'scroll') && el.scrollHeight > el.clientHeight + 1) {
        if ((dy < 0 && el.scrollTop > 0) || (dy > 0 && el.scrollTop + el.clientHeight < el.scrollHeight - 1)) return true;
      }
    }
    return false;
  };
  window.addEventListener(
    'wheel',
    (e) => {
      if (e.ctrlKey || e.defaultPrevented) return;
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      if (nested(e.target, e.deltaY)) return;
      e.preventDefault();
      const d = e.deltaY * (e.deltaMode === 1 ? 16 : e.deltaMode === 2 ? window.innerHeight : 1);
      glide((running ? target : window.scrollY) + d);
    },
    { passive: false }
  );
  // Anything else that moves the page (keys, scrollbar) takes over.
  window.addEventListener(
    'scroll',
    () => {
      if (running && Math.abs(window.scrollY - Math.round(current)) > 2) {
        running = false;
        last = 0;
      }
      if (!running) target = current = window.scrollY;
    },
    { passive: true }
  );
  document.addEventListener('click', (e) => {
    const a = (e.target as Element | null)?.closest?.<HTMLAnchorElement>('a[href^="#"]');
    // The skip link stays native, so focus moves with it.
    if (!a || a.classList.contains('skip-link') || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey) return;
    const id = a.getAttribute('href')!.slice(1);
    const to = id ? document.getElementById(id) : null;
    if (!to && id !== 'top') return;
    e.preventDefault();
    glide(to ? to.getBoundingClientRect().top + window.scrollY - (navh() + 24) : 0);
  });
}
