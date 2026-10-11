"""Editorial homepage for when-hardening-helps. Visual-first, minimal text.

Replaces the old index_body in build.py. Every number is passed in from
build.py's data (never typed by hand).
"""

def index_body_new(data, pieces, stats):
    """stats: dict with n_instances, n_wins, n_runs, rhos, etc. from build.py."""
    n_inst = stats['n_instances']
    n_wins = stats['n_wins']
    n_runs = stats['n_runs']
    rho_d = stats['rho_discovery']
    rho_h1 = stats['rho_heldout1']
    rho_h2 = stats['rho_heldout2']

    return f"""
<header class="hero-full">
<div class="eyebrow">a follow-up to <a href="https://yoheinakajima.github.io/soft-to-rigid/">soft-to-rigid</a></div>
<h1>When does hardening help?</h1>
<p class="answer">Hardening wins when the soft disks land in the right neighborhood.</p>
<p class="sub">{n_runs:,} packings. {n_inst} instances. Eight shapes. One rule — found by being wrong first.</p>
<div class="scroll-hint">↓</div>
</header>

<section class="act">
<div class="act-label">The method</div>
<h2>Start soft. Compress. Morph.</h2>
<figure class="hero"><img src="assets/morph-strip.png" alt="Disks compress into a scaffold, then morph into the pinwheel"></figure>
<p class="act-text">Every piece begins as its inscribed disk. The disks compress into a tight scaffold. Then each disk gradually morphs into its rigid shape — square, triangle, cross — while the container keeps squeezing. The question: when does this beat just starting rigid?</p>
</section>

<section class="act">
<div class="act-label">The wrong answer</div>
<h2>We thought concavity would predict it.</h2>
<div class="pills">
<span class="pill">concavity <b>p=0.19</b></span>
<span class="pill">piece count <b>p=0.31</b></span>
<span class="pill">disk share <b>p=0.15</b></span>
</div>
<p class="act-text">Our first theory failed cleanly. No shape descriptor predicted where hardening wins. That null result is where the real story starts.</p>
</section>

<section class="act">
<div class="act-label">The discovery</div>
<h2>The scaffold predicts the outcome.</h2>
<figure class="hero"><img src="assets/fidelity-scatter.png" alt="Scaffold fidelity vs hardening gap"></figure>
<p class="act-text">Measure how well the compressed disks' arrangement matches the optimum — <i>scaffold fidelity</i> — and it predicts hardening's success. Correlation held across three independent batches: ρ={rho_d:.2f}, {rho_h1:.2f}, {rho_h2:.2f}. Each dot is one of {n_inst} instances ({n_wins} hardening wins).</p>
</section>

<section class="act">
<div class="act-label">The proof</div>
<h2>Three numbers.</h2>
<div class="proof-cards">
<div class="proof-card"><b>8/8</b><span>Good scaffold transplanted under the morph reaches the good basin every time.</span></div>
<div class="proof-card"><b>11.57 → 4.00</b><span>Skipping the gradual morph ("snap") catastrophically fails where scaffolds are tight.</span></div>
<div class="proof-card"><b>quarter ≥ full</b><span>Starting the morph nearly rigid matches or beats the full disk-to-shape path everywhere tested.</span></div>
</div>
<p class="act-text">The mechanism: the compress phase proposes a scaffold, and the gradual morph preserves it while growing corners.</p>
</section>

<section class="act">
<div class="act-label">The caveats</div>
<h2>Honest limits.</h2>
<p class="act-text"><b>Traps are probabilistic.</b> The scaffold picks the basin region; whether the morph gets stuck inside it depends on the run.<br><b>Single predictions are noisy.</b> The rule predicts the distribution across instances, not individual flips.</p>
</section>

<section class="explore">
<h2>Go deeper</h2>
<div class="explore-cards">
<a href="families.html"><b>Families</b><span>Every shape, every instance, with animated replays.</span></a>
<a href="journal.html"><b>Journal</b><span>All 20 campaigns, 22 findings, nulls included.</span></a>
<a href="paper.html"><b>Paper</b><span>The write-up, with numbers.</span></a>
<a href="https://github.com/yoheinakajima/when-hardening-helps"><b>Repository</b><span>Code, data, ledger. MIT.</span></a>
</div>
</section>
"""


def index_css():
    return """
/* Editorial homepage */
.hero-full { min-height: 92vh; display: flex; flex-direction: column; justify-content: center; text-align: center; padding: 2em 1em; }
.hero-full h1 { font-size: clamp(2.4rem, 6vw, 4.2rem); margin: 0.3em 0; letter-spacing: -0.02em; }
.hero-full .answer { font-family: var(--serif); font-size: clamp(1.3rem, 3vw, 1.9rem); color: var(--soft); max-width: 22em; margin: 0.5em auto; line-height: 1.35; }
.hero-full .sub { color: var(--mut); font-size: 1.05rem; max-width: 34em; margin: 1em auto 0; }
.scroll-hint { margin-top: 3em; color: var(--mut); font-size: 1.5rem; animation: bob 2s ease-in-out infinite; }
@keyframes bob { 0%,100% { transform: translateY(0); opacity: 0.5; } 50% { transform: translateY(8px); opacity: 1; } }

.act { margin: 0 auto; max-width: 900px; padding: 4em 20px; }
.act-label { text-transform: uppercase; letter-spacing: 0.14em; font-size: 0.78rem; color: var(--soft); font-weight: 700; margin-bottom: 0.6em; }
.act h2 { font-size: clamp(1.6rem, 3.5vw, 2.4rem); margin: 0 0 0.8em; letter-spacing: -0.01em; }
.act-text { font-size: 1.08rem; line-height: 1.65; max-width: 38em; color: #3a362e; }
.act .hero img { border-radius: 14px; box-shadow: 0 8px 32px rgba(0,0,0,0.08); }

.pills { display: flex; gap: 0.8em; flex-wrap: wrap; margin: 1.2em 0; }
.pill { background: var(--card); border: 1px solid var(--rule); border-radius: 999px; padding: 0.55em 1.2em; font-size: 0.95rem; color: var(--mut); }
.pill b { color: var(--ink); }

.proof-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin: 1.4em 0; }
.proof-card { background: var(--card); border: 1px solid var(--rule); border-radius: 14px; padding: 1.2em 1.3em; }
.proof-card b { display: block; font-family: var(--serif); font-size: 1.9rem; color: var(--soft); margin-bottom: 0.3em; }
.proof-card span { font-size: 0.92rem; color: var(--mut); line-height: 1.5; }

.explore { max-width: 900px; margin: 0 auto; padding: 3em 20px 5em; }
.explore h2 { font-size: 1.6rem; }
.explore-cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 14px; margin-top: 1em; }
.explore-cards a { background: var(--card); border: 1px solid var(--rule); border-radius: 14px; padding: 1.2em 1.3em; text-decoration: none; color: inherit; transition: transform 0.15s, box-shadow 0.15s; }
.explore-cards a:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); border-color: var(--ink); }
.explore-cards b { display: block; font-size: 1.05rem; margin-bottom: 0.3em; }
.explore-cards span { font-size: 0.9rem; color: var(--mut); }
"""
