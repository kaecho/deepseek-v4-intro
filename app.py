import streamlit as st

st.set_page_config(
    page_title="DeepSeek V4 Pro 0813",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Design tokens: DeepSeek blue #4D6BFE, radius 10px, Geist + Geist Mono.
# Host is Streamlit (HF Space / Docker). Motion is CSS only.

st.markdown(
    """
<style>
@font-face {
  font-family: "Geist";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("/app/static/fonts/geist-400.woff2") format("woff2");
}
@font-face {
  font-family: "Geist";
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url("/app/static/fonts/geist-500.woff2") format("woff2");
}
@font-face {
  font-family: "Geist";
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url("/app/static/fonts/geist-600.woff2") format("woff2");
}
@font-face {
  font-family: "Geist";
  font-style: normal;
  font-weight: 700;
  font-display: swap;
  src: url("/app/static/fonts/geist-700.woff2") format("woff2");
}
@font-face {
  font-family: "Geist Mono";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url("/app/static/fonts/geist-mono-400.woff2") format("woff2");
}
@font-face {
  font-family: "Geist Mono";
  font-style: normal;
  font-weight: 500;
  font-display: swap;
  src: url("/app/static/fonts/geist-mono-500.woff2") format("woff2");
}

:root {
  --bg: #eceef2;
  --bg-elev: #f6f7f9;
  --ink: #16181d;
  --muted: #4e5560;
  --line: #d4d8e0;
  --accent: #2f4bd6;
  --accent-ink: #ffffff;
  --code: #16181d;
  --code-bg: #e4e7ee;
  --scrim: rgba(16, 17, 20, 0.55);
  --shadow: 0 18px 40px rgba(22, 24, 29, 0.08);
  --radius: 10px;
  --nav-h: 64px;
  --z-nav: 40;
  --z-grain: 60;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #101114;
    --bg-elev: #181a20;
    --ink: #eceef2;
    --muted: #9aa1ad;
    --line: #2c3038;
    --accent: #6b86ff;
    --accent-ink: #101114;
    --code: #d7dbe3;
    --code-bg: #0c0d10;
    --scrim: rgba(10, 11, 14, 0.55);
    --shadow: 0 18px 40px rgba(0, 0, 0, 0.28);
  }
}

html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}

.stApp, [data-testid="stAppViewContainer"], .stApp header {
  background: var(--bg) !important;
  color: var(--ink);
}
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
[data-testid="stFooter"],
#MainMenu, .stDeployButton { display: none !important; }
.block-container {
  max-width: 100% !important;
  padding: 0 !important;
}
.stMarkdown, .stMarkdown p { margin: 0; }
.stApp { color: var(--ink); }
div[data-testid="stHtml"], .stHtml { padding: 0 !important; }
.stApp a.btn-primary, .stApp a.nav-cta { color: var(--accent-ink) !important; }
.stApp a.btn-ghost, .stApp .brand, .stApp .links-row a { color: var(--ink) !important; text-decoration: none !important; }
.stApp .nav-links a { color: var(--muted) !important; text-decoration: none !important; }
.stApp .run-block a, .stApp .note a, .stApp .foot a { color: var(--accent) !important; }

.page, .page * { font-family: "Geist", ui-sans-serif, system-ui, sans-serif !important; }
.page {
  background: var(--bg);
  color: var(--ink);
  min-height: 100dvh;
}
.mono, .page code, .page pre, .num, .metric-value, .score-value, .mode-name {
  font-family: "Geist Mono", ui-monospace, monospace !important;
}

.grain {
  position: fixed;
  inset: 0;
  z-index: var(--z-grain);
  pointer-events: none;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='.55'/%3E%3C/svg%3E");
}

.wrap {
  width: min(1400px, calc(100% - 2.5rem));
  margin: 0 auto;
}
@media (max-width: 767px) {
  .wrap { width: calc(100% - 2rem); }
}

/* Web frosted-glass approximation, not Apple Liquid Glass */
.nav {
  position: sticky;
  top: 0;
  z-index: var(--z-nav);
  height: var(--nav-h);
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--line);
  background: color-mix(in srgb, var(--bg) 82%, transparent);
  backdrop-filter: blur(18px) saturate(140%);
  -webkit-backdrop-filter: blur(18px) saturate(140%);
}
@media (prefers-reduced-transparency: reduce) {
  .nav { background: var(--bg); backdrop-filter: none; -webkit-backdrop-filter: none; }
}
.nav-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1.5rem;
  width: min(1400px, calc(100% - 2.5rem));
  margin: 0 auto;
  height: 100%;
}
.brand {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  color: var(--ink);
  text-decoration: none;
  font-weight: 600;
  letter-spacing: -0.03em;
  white-space: nowrap;
}
.brand img {
  height: 22px;
  width: auto;
  display: block;
}
@media (prefers-color-scheme: dark) {
  .brand img { filter: invert(1) hue-rotate(180deg) saturate(2.2); }
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 1.35rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.nav-links a {
  color: var(--muted);
  text-decoration: none;
  font-size: 0.92rem;
  font-weight: 500;
}
.nav-links a:hover { color: var(--ink); }
.nav-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  background: var(--accent) !important;
  color: var(--accent-ink) !important;
  padding: 0.45rem 0.85rem;
  border-radius: var(--radius);
  font-size: 0.88rem;
  font-weight: 600;
  text-decoration: none !important;
  white-space: nowrap;
}
.nav-cta:hover { filter: brightness(1.06); }
.nav-cta:active { transform: scale(0.98); }
.nav-more { display: none; }
.nav-more summary {
  list-style: none;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
}
.nav-more summary::-webkit-details-marker { display: none; }
.nav-more a {
  display: block;
  padding: 0.45rem 0;
  color: var(--ink);
  text-decoration: none;
}

.hero {
  min-height: calc(100dvh - var(--nav-h));
  display: grid;
  grid-template-columns: 1.05fr 0.95fr;
  gap: 3rem;
  align-items: center;
  padding: 3.5rem 0 3rem;
}
.hero h1 {
  margin: 0 0 1.1rem;
  font-size: clamp(2.2rem, 4.1vw, 3.35rem);
  line-height: 1.08;
  letter-spacing: -0.055em;
  font-weight: 600;
}
.hero h1 em {
  font-style: normal;
  color: var(--accent);
}
.lede {
  margin: 0 0 1.6rem;
  max-width: 42ch;
  color: var(--muted);
  font-size: 1.05rem;
  line-height: 1.6;
}
.cta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  align-items: center;
}
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.7rem 1.05rem;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none;
  white-space: nowrap;
  border: 1px solid transparent;
}
.btn:active { transform: scale(0.98); }
.btn-primary {
  background: var(--accent) !important;
  color: var(--accent-ink) !important;
  text-decoration: none !important;
}
.btn-primary:hover { filter: brightness(1.06); }
.btn-ghost {
  background: transparent !important;
  color: var(--ink) !important;
  border-color: var(--line) !important;
  text-decoration: none !important;
}
.btn-ghost:hover { border-color: var(--ink); }
.icon {
  width: 1em;
  height: 1em;
  display: block;
}
@media (prefers-color-scheme: dark) {
  .icon-on-ink { filter: invert(1); }
}
.btn-primary .icon, .nav-cta .icon { filter: none; }
@media (prefers-color-scheme: light) {
  .btn-primary .icon, .nav-cta .icon { filter: invert(1); }
}
@media (prefers-color-scheme: dark) {
  .btn-primary .icon, .nav-cta .icon { filter: none; }
}

.hero-visual {
  position: relative;
  border-radius: var(--radius);
  overflow: hidden;
  min-height: 28rem;
  background: var(--bg-elev);
}
.hero-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  min-height: 28rem;
}


.metrics {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
}
.metric {
  padding: 1.4rem 1.1rem 1.5rem 0;
  border-right: 1px solid var(--line);
}
.metric:last-child { border-right: 0; padding-right: 0; }
.metric-label {
  display: block;
  color: var(--muted);
  font-size: 0.8rem;
  margin-bottom: 0.45rem;
}
.metric-value {
  font-size: 1.85rem;
  letter-spacing: -0.04em;
  font-weight: 500;
}
.metric-value small {
  font-size: 0.78rem;
  color: var(--accent);
  margin-left: 0.35rem;
  letter-spacing: 0;
}

.links-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem 1.4rem;
  padding: 1.1rem 0 0;
}
.links-row a {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  color: var(--ink);
  text-decoration: none;
  font-size: 0.88rem;
  font-weight: 500;
}
.links-row a:hover { color: var(--accent); }
.links-row img {
  width: 16px;
  height: 16px;
}
@media (prefers-color-scheme: dark) {
  .links-row img { filter: brightness(0) invert(1); }
}
@media (prefers-color-scheme: light) {
  .links-row img { filter: brightness(0); }
}

.section {
  padding: 5.5rem 0 1rem;
}
.section h2 {
  margin: 0 0 0.75rem;
  font-size: clamp(1.8rem, 3.2vw, 2.6rem);
  letter-spacing: -0.045em;
  line-height: 1.1;
  font-weight: 600;
  max-width: 22ch;
}
.section > .lede { margin-bottom: 2rem; }

.bento {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 0.75rem;
}
.cell {
  background: var(--bg-elev);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: 1.25rem 1.3rem 1.35rem;
  min-height: 10.5rem;
}
.cell h3 {
  margin: 0 0 0.55rem;
  font-size: 1.12rem;
  letter-spacing: -0.03em;
  font-weight: 600;
}
.cell p {
  margin: 0;
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.55;
  max-width: 46ch;
}
.bento-hero {
  grid-column: 1;
  grid-row: 1 / span 2;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  min-height: 22rem;
}
.bento-hero img {
  width: 100%;
  height: 55%;
  object-fit: cover;
  display: block;
  min-height: 12rem;
}
.bento-hero .cell-copy { padding: 1.25rem 1.3rem 1.4rem; }
.cell-accent {
  background: var(--accent);
  color: var(--accent-ink);
  border-color: transparent;
}
.cell-accent p { color: color-mix(in srgb, var(--accent-ink) 82%, transparent); }
.cell-photo {
  padding: 0;
  overflow: hidden;
  position: relative;
  min-height: 12rem;
}
.cell-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  min-height: 12rem;
}
.cell-photo .cell-copy {
  position: absolute;
  inset: auto 0 0 0;
  padding: 1.1rem 1.2rem;
  background: linear-gradient(transparent, var(--scrim));
  color: #f3f4f7;
}
.cell-photo .cell-copy p { color: #d5d8e0; }

.context {
  margin-top: 4.5rem;
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 0;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  background: var(--bg-elev);
}
.context-copy { padding: 2.4rem 2.2rem; }
.context-copy h2 { margin-bottom: 0.8rem; }
.stat-pair {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.2rem;
  margin-top: 1.8rem;
}
.stat-pair .num {
  display: block;
  font-size: 2rem;
  letter-spacing: -0.05em;
  color: var(--accent);
  font-weight: 500;
}
.stat-pair span {
  display: block;
  color: var(--muted);
  font-size: 0.88rem;
  margin-top: 0.3rem;
  max-width: 22ch;
}
.context-visual {
  min-height: 22rem;
  position: relative;
}
.context-visual img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  min-height: 22rem;
  filter: saturate(0.75);
}

.feat {
  display: grid;
  grid-template-columns: 1.15fr 1fr;
  grid-template-rows: auto auto auto;
  gap: 0.75rem;
}
.feat-main {
  grid-column: 1;
  grid-row: 1 / span 3;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 22rem;
  position: relative;
  color: #f3f4f7;
}
.feat-main img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.feat-main .shade {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(16,17,20,0.15), rgba(16,17,20,0.78));
}
.feat-main .cell-copy {
  position: relative;
  padding: 1.5rem 1.4rem;
}
.feat-main p { color: #d5d8e0; }
.score-value {
  display: block;
  font-size: clamp(2.4rem, 4vw, 3.4rem);
  letter-spacing: -0.06em;
  font-weight: 500;
  line-height: 1;
  margin-bottom: 0.45rem;
}
.score-name { font-weight: 600; display: block; margin-bottom: 0.35rem; }
.compare {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem 2.5rem;
  margin-top: 2.2rem;
}
.compare-col h3 {
  margin: 0 0 0.9rem;
  font-size: 1rem;
  font-weight: 600;
}
.row {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  padding: 0.7rem 0;
  align-items: baseline;
}
.row + .row { border-top: 1px solid var(--line); }
.row b { font-weight: 500; }
.row .now { font-family: "Geist Mono", ui-monospace, monospace; color: var(--ink); }
.row .was { font-family: "Geist Mono", ui-monospace, monospace; color: var(--muted); }
.col-head {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 1rem;
  color: var(--muted);
  font-size: 0.75rem;
  margin-bottom: 0.2rem;
}
.note {
  margin: 1.4rem 0 0;
  color: var(--muted);
  font-size: 0.88rem;
  line-height: 1.55;
  max-width: 72ch;
}

.modes {
  display: flex;
  flex-direction: column;
}
.mode {
  display: grid;
  grid-template-columns: 8.5rem 1fr;
  gap: 1.5rem;
  padding: 1.35rem 0;
  border-top: 1px solid var(--line);
  align-items: start;
}
.mode:last-child { border-bottom: 1px solid var(--line); }
.mode-name {
  font-family: "Geist Mono", ui-monospace, monospace;
  font-size: 1.05rem;
  font-weight: 500;
  color: var(--accent);
}
.mode h3 {
  margin: 0 0 0.35rem;
  font-size: 1.15rem;
  letter-spacing: -0.03em;
}
.mode p { margin: 0; color: var(--muted); max-width: 62ch; line-height: 1.6; }

.run-block { margin-bottom: 1.4rem; }
.run-block h3 {
  margin: 0 0 0.55rem;
  font-size: 1.05rem;
  font-weight: 600;
}
.run-block a { color: var(--accent); }
pre {
  margin: 0;
  padding: 1.1rem 1.15rem;
  background: var(--code-bg);
  color: var(--code);
  border-radius: var(--radius);
  border: 1px solid var(--line);
  overflow-x: auto;
  font-size: 0.82rem;
  line-height: 1.55;
}
code { font-size: inherit; }

.foot {
  margin-top: 5rem;
  padding: 1.6rem 0 2.4rem;
  border-top: 1px solid var(--line);
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 2rem;
  color: var(--muted);
  font-size: 0.85rem;
  line-height: 1.55;
}
.foot a { color: var(--ink); }
.foot ul { list-style: none; margin: 0; padding: 0; }
.foot li { margin: 0.25rem 0; }

@media (prefers-reduced-motion: no-preference) {
  .hero-copy {
    animation: rise 0.8s cubic-bezier(0.16, 1, 0.3, 1) both;
  }
  .hero-visual {
    animation: rise 0.9s cubic-bezier(0.16, 1, 0.3, 1) 0.08s both;
  }
  .reveal {
    animation: rise 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
    animation-timeline: view();
    animation-range: entry 0% entry 32%;
  }
}
@keyframes rise {
  from { opacity: 0; transform: translateY(18px); }
  to { opacity: 1; transform: translateY(0); }
}
@media (prefers-reduced-motion: reduce) {
  .hero-copy, .hero-visual, .reveal { animation: none; }
}

@media (max-width: 1024px) {
  .hero { grid-template-columns: 1fr; gap: 1.6rem; padding-top: 2.4rem; }
  .hero h1 { max-width: none; }
  .hero-visual, .hero-visual img { min-height: 20rem; }
  .bento { grid-template-columns: 1fr 1fr; grid-template-rows: none; }
  .bento-hero { grid-column: 1 / span 2; grid-row: auto; }
  .context { grid-template-columns: 1fr; }
}
@media (max-width: 767px) {
  .nav-inner { width: calc(100% - 2rem); }
  .nav-links { display: none; }
  .nav-more { display: block; position: relative; }
  .nav-more[open] {
    position: absolute;
    right: 1rem;
    top: 0.7rem;
    background: var(--bg-elev);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    padding: 0.7rem 1rem 0.9rem;
    min-width: 12rem;
  }
  .metrics { grid-template-columns: 1fr 1fr; }
  .metric:nth-child(odd) { padding-right: 1rem; }
  .metric:nth-child(-n+2) { border-bottom: 1px solid var(--line); }
  .metric:nth-child(2n) { border-right: 0; }
  .bento, .feat, .compare { grid-template-columns: 1fr; }
  .bento-hero, .feat-main { grid-column: auto; grid-row: auto; }
  .mode { grid-template-columns: 1fr; gap: 0.35rem; }
  .stat-pair { grid-template-columns: 1fr; }
  .foot { grid-template-columns: 1fr; }
  .section { padding-top: 3.6rem; }
}
</style>
""",
    unsafe_allow_html=True,
)

ICON_EXT = """<img class="icon" src="/app/static/icons/arrow-up-right.svg" alt="">"""
ICON_EXT_INK = """<img class="icon icon-on-ink" src="/app/static/icons/arrow-up-right.svg" alt="">"""

st.html(
    f"""
<div class="page">
  <div class="grain" aria-hidden="true"></div>
  <header class="nav">
    <div class="nav-inner">
      <a class="brand" href="#top">
        <img src="/app/static/logo.svg" alt="DeepSeek">
        <span>V4 Pro</span>
      </a>
      <ul class="nav-links">
        <li><a href="#architecture">Architecture</a></li>
        <li><a href="#context">Context</a></li>
        <li><a href="#benchmarks">Benchmarks</a></li>
        <li><a href="#run">Run</a></li>
        <li><a class="nav-cta" href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813">Get the model {ICON_EXT}</a></li>
      </ul>
      <details class="nav-more">
        <summary>Menu</summary>
        <a href="#architecture">Architecture</a>
        <a href="#context">Context</a>
        <a href="#benchmarks">Benchmarks</a>
        <a href="#run">Run</a>
        <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813">Get the model</a>
      </details>
    </div>
  </header>

  <main id="top">
    <section class="hero wrap">
      <div class="hero-copy">
        <h1>DeepSeek V4 Pro<br>for production agents.</h1>
        <p class="lede">Official 0813 release of DeepSeek-V4-Pro. Stronger agents in production, with DSpark speculative decoding.</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813">Get the model {ICON_EXT}</a>
          <a class="btn btn-ghost" href="https://arxiv.org/abs/2606.19348">Technical report {ICON_EXT_INK}</a>
        </div>
      </div>
      <figure class="hero-visual">
        <img src="/app/static/hero.jpg" alt="Server racks with sparse indicator lights" width="1200" height="1600">
      </figure>
    </section>

    <div class="wrap">
      <div class="metrics reveal">
        <div class="metric"><span class="metric-label">Total parameters</span><span class="metric-value">1.6T</span></div>
        <div class="metric"><span class="metric-label">Active per token</span><span class="metric-value">49B <small>3.1%</small></span></div>
        <div class="metric"><span class="metric-label">Context window</span><span class="metric-value">1M</span></div>
        <div class="metric"><span class="metric-label">License</span><span class="metric-value">MIT</span></div>
      </div>
      <div class="links-row">
        <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813"><img src="/app/static/icons/huggingface.svg" alt="">Hugging Face</a>
        <a href="https://arxiv.org/abs/2606.19348"><img src="/app/static/icons/arxiv.svg" alt="">arXiv 2606.19348</a>
        <a href="https://chat.deepseek.com/"><img src="/app/static/icons/terminal.svg" alt="">Open chat</a>
        <a href="https://github.com/deepseek-ai"><img src="/app/static/icons/github.svg" alt="">deepseek-ai</a>
      </div>
    </div>

    <section class="section wrap" id="architecture">
      <h2>Architecture</h2>
      <p class="lede">Same DeepSeek-V4-Pro structure as the preview, with a DSpark module attached for speculative decoding.</p>
      <div class="bento reveal">
        <article class="cell bento-hero">
          <img src="/app/static/architecture.jpg" alt="Close-up of a circuit board" width="1600" height="1000">
          <div class="cell-copy">
            <h3>Hybrid attention</h3>
            <p>Compressed Sparse Attention plus Heavily Compressed Attention. At 1M tokens this is 27% of DeepSeek-V3.2 single-token FLOPs and 10% of the KV cache.</p>
          </div>
        </article>
        <article class="cell">
          <h3>MoE routing</h3>
          <p>1.6 trillion parameters in the pool. 49 billion activate per token, so most of the model stays dark on any one step.</p>
        </article>
        <article class="cell">
          <h3>mHC connections</h3>
          <p>Manifold-Constrained Hyper-Connections thicken residual paths while keeping training stable.</p>
        </article>
        <article class="cell">
          <h3>Muon optimizer</h3>
          <p>Used across the 32T+ token pre-training run for faster convergence and fewer unstable spikes.</p>
        </article>
        <article class="cell cell-accent">
          <h3>DSpark</h3>
          <p>Speculative decoding shipped in 0813. One flag in vLLM (<span class="mono">method: dspark</span>) or SGLang (<span class="mono">DSPARK</span>). Draft and target weights share the checkpoint.</p>
        </article>
      </div>
    </section>

    <section class="wrap" id="context">
      <div class="context reveal">
        <div class="context-copy">
          <h2>Long Context</h2>
          <p class="lede">One million tokens in a single window, so a repo, a paper pile, or a long agent trace can stay in view instead of being chopped into disconnected chunks.</p>
          <div class="stat-pair">
            <div><span class="num">27%</span><span>of V3.2 single-token FLOPs at 1M context</span></div>
            <div><span class="num">10%</span><span>of V3.2 KV cache at 1M context</span></div>
          </div>
        </div>
        <div class="context-visual">
          <img src="/app/static/context.jpg" alt="Dense library shelves standing in for a long context window" width="1600" height="1000">
        </div>
      </div>
    </section>

    <section class="section wrap" id="benchmarks">
      <h2>Benchmarks</h2>
      <p class="lede">0813 beats the V4-Pro preview on the public agent suites below. It sits with the strongest closed models, not ahead of every one of them.</p>
      <div class="feat reveal">
        <article class="cell feat-main">
          <img src="/app/static/desk.jpg" alt="Laptop on a desk with a code editor open" width="1400" height="1050">
          <div class="shade" aria-hidden="true"></div>
          <div class="cell-copy">
            <span class="score-value">62.7</span>
            <span class="score-name">DeepSWE</span>
            <p>Preview scored 12.8. This is the largest jump on the 0813 card.</p>
          </div>
        </article>
        <article class="cell">
          <span class="score-value">87.9</span>
          <span class="score-name">Terminal Bench 2.1</span>
          <p>Preview 72.1. Kimi K3 reports 88.3 on the same table.</p>
        </article>
        <article class="cell">
          <span class="score-value">83.3</span>
          <span class="score-name">Cybergym</span>
          <p>Preview 52.7. Security and exploit-repair style tasks.</p>
        </article>
        <article class="cell">
          <span class="score-value">60.0</span>
          <span class="score-name">HLE with tools</span>
          <p>42.7 without tools. Preview was 37.7 / 48.2.</p>
        </article>
      </div>
      <div class="compare">
        <div class="compare-col">
          <h3>Coding agents</h3>
          <div class="col-head"><span>Task</span><span>0813</span><span>Preview</span></div>
          <div class="row"><span>NL2Repo</span><b class="now">61.5</b><span class="was">38.5</span></div>
          <div class="row"><span>DSBench-FullStack</span><b class="now">71.1</b><span class="was">41.8</span></div>
          <div class="row"><span>DSBench-Hard</span><b class="now">67.2</b><span class="was">31.1</span></div>
        </div>
        <div class="compare-col">
          <h3>Tool use</h3>
          <div class="col-head"><span>Task</span><span>0813</span><span>Preview</span></div>
          <div class="row"><span>Toolathlon-Verified</span><b class="now">74.1</b><span class="was">55.9</span></div>
          <div class="row"><span>Agents' Last Exam</span><b class="now">25.7</b><span class="was">16.5</span></div>
          <div class="row"><span>AutomationBench</span><b class="now">31.8</b><span class="was">12.8</span></div>
        </div>
      </div>
      <p class="note">Code-agent numbers use DeepSeek Harness in minimal mode, <span class="mono">reasoning_effort=max</span>, <span class="mono">temperature=1.0</span>, <span class="mono">top_p=0.95</span>. DSBench-FullStack and DSBench-Hard are internal sets. Source: the DeepSeek-V4-Pro-0813 model card.</p>
    </section>

    <section class="section wrap" id="reasoning">
      <h2>Reasoning</h2>
      <p class="lede"><span class="mono">reasoning_effort</span> is low, high, or max. It sets how long the model thinks before it answers.</p>
      <div class="modes reveal">
        <article class="mode">
          <div class="mode-name">low</div>
          <div>
            <h3>Short deliberation</h3>
            <p>Use when latency matters more than a long private chain of thought. Everyday transforms, lookups, and drafts.</p>
          </div>
        </article>
        <article class="mode">
          <div class="mode-name">high</div>
          <div>
            <h3>Standard thinking</h3>
            <p>Default for coding and multi-step work. Cap output at 384K tokens. Sample at temperature 1.0; use top_p 0.95 for agents, 1.0 otherwise.</p>
          </div>
        </article>
        <article class="mode">
          <div class="mode-name">max</div>
          <div>
            <h3>Full effort</h3>
            <p>Hardest proofs, long agent loops, and the numbers on this page. Same 384K output cap. 0813 was scored at this level on the code-agent suites.</p>
          </div>
        </article>
      </div>
    </section>

    <section class="section wrap" id="run">
      <h2>Run it</h2>
      <p class="lede">0813 is on Transformers, vLLM, and SGLang. There is no Jinja chat template; encode OpenAI-style messages with the <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/tree/main/encoding">encoding</a> scripts.</p>
      <div class="run-block reveal">
        <h3>vLLM, DSpark on</h3>
        <p class="note" style="margin-top:0;margin-bottom:0.7rem">Example from the model card, one 4×GB300 node. Full hardware notes: <a href="https://recipes.vllm.ai/deepseek-ai/DeepSeek-V4-Pro">vLLM recipe</a>.</p>
        <pre><code>vllm serve deepseek-ai/DeepSeek-V4-Pro-0813 \\
  --trust-remote-code --kv-cache-dtype fp8 --block-size 256 \\
  --data-parallel-size 4 --enable-expert-parallel \\
  --moe-backend deep_gemm_mega_moe \\
  --attention-config '{{"use_fp4_indexer_cache": true}}' \\
  --speculative-config '{{"method":"dspark","num_speculative_tokens":7,"draft_sample_method":"greedy"}}'</code></pre>
      </div>
      <div class="run-block">
        <h3>SGLang, DSpark on</h3>
        <p class="note" style="margin-top:0;margin-bottom:0.7rem">Do not set a separate draft model path. Cookbook: <a href="https://docs.sglang.io/cookbook/autoregressive/DeepSeek/DeepSeek-V4">SGLang DeepSeek-V4</a>.</p>
        <pre><code>sglang serve \\
  --trust-remote-code \\
  --model-path deepseek-ai/DeepSeek-V4-Pro-0813 \\
  --tp 4 \\
  --moe-runner-backend flashinfer_mxfp4 \\
  --speculative-algorithm DSPARK \\
  --mem-fraction-static 0.90 \\
  --chunked-prefill-size 4096 \\
  --swa-full-tokens-ratio 0.1</code></pre>
      </div>
      <p class="note">Local chat demos and weight conversion live in the <a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813/tree/main/inference">inference</a> folder. Try the hosted model at <a href="https://chat.deepseek.com/">chat.deepseek.com</a>.</p>
    </section>
  </main>

  <footer class="foot wrap">
    <div>
      Independent introduction of DeepSeek-V4-Pro-0813. Figures are from the Hugging Face model card and the DeepSeek-V4 technical report. This page does not call the model.
      <br><br>
      DeepSeek-AI, 2026. MIT License. Questions: <a href="mailto:service@deepseek.com">service@deepseek.com</a>
    </div>
    <ul>
      <li><a href="https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-0813">Get the model</a></li>
      <li><a href="https://arxiv.org/abs/2606.19348">Technical report</a></li>
      <li><a href="https://chat.deepseek.com/">Open chat</a></li>
      <li><a href="https://www.deepseek.com/">deepseek.com</a></li>
    </ul>
  </footer>
</div>
""",
)
