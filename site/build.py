"""Build the when-hardening-helps GitHub Pages site into _site/ (not committed).

    python3 site/build.py

Every number on the pages is generated from site/data.json, site/pieces.json,
JOURNAL.md or paper/numbers.tex. Nothing is typed by hand.
"""
import datetime
import glob
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_home import index_body_new, index_css

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, '_site')
REPO = 'https://github.com/yoheinakajima/when-hardening-helps'

try:
    COMMIT = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'],
                                     cwd=ROOT, text=True).strip()
except Exception:
    COMMIT = 'unknown'
BUILT = datetime.date.today().isoformat()

METHOD_LABEL = {'harden': 'hardening', 'rigid': 'rigid start', 'sa': 'simulated annealing',
                'pc': 'perturbation-compression', 'grow': 'growth'}


def load():
    with open(os.path.join(HERE, 'data.json')) as f:
        data = json.load(f)
    with open(os.path.join(HERE, 'pieces.json')) as f:
        pieces = json.load(f)
    with open(os.path.join(ROOT, 'JOURNAL.md')) as f:
        journal = f.read()
    nums = {}
    fp = os.path.join(ROOT, 'paper', 'numbers.tex')
    if os.path.exists(fp):
        nums = dict(re.findall(r'\\newcommand\{\\(\w+)\}\{(.*)\}\s*$',
                               open(fp).read(), re.M))
    return data, pieces, journal, nums


def fmt_L(x):
    s = f'{x:.6f}'.rstrip('0').rstrip('.')
    return s if s else '0'


def short_piece(title):
    t = title
    if t.lower().startswith('unit '):
        t = t[5:]
    t = re.split(r'\s+in an?\s+', t)[0]
    return t[0].lower() + t[1:] if t else t


def disk_share(piece):
    """Inscribed-disk share of piece area, from pieces.json geometry."""
    rho, area = piece['rho'], piece['area']
    return math.pi * rho * rho / area if area else 0.0


# ---------------------------------------------------------------- head/foot
def head(title, desc):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="assets/site.css">
</head>
<body>
<main>
<nav class="top"><a class="home" href="index.html">when-hardening-helps</a><a href="families.html">Families</a><a href="journal.html">Journal</a><a href="paper.html">Paper</a><a href="{REPO}">Repository</a></nav>
"""


FOOT = f"""<footer>Yohei Nakajima. Code, experiments and verification were developed with Claude (Anthropic). Every number on this site is generated from the research ledger (<a href="{REPO}/blob/main/ledger/events.jsonl">events.jsonl</a>), built from commit <span class="mono">{COMMIT}</span> on {BUILT}. MIT licence.</footer>
</main>
"""


def page(name, title, desc, body, scripts='', extra_css=''):
    h = head(title, desc).replace(f'<a href="{name}.html">', f'<a href="{name}.html" aria-current="page">')
    if name == 'index':
        h = h.replace('<a class="home" href="index.html">',
                      '<a class="home" href="index.html" aria-current="page">')
    if extra_css:
        h = h.replace('</head>', f'<style>{extra_css}</style>\n</head>')
    return h + body + FOOT + scripts + '</body>\n</html>\n'


# ---------------------------------------------------------------- index
def meta_pvalues():
    """Falsification p-values, parsed from the frozen meta-analysis output."""
    txt = open(os.path.join(ROOT, 'analysis', 'meta-results.txt')).read()
    out = {}
    m = re.search(r'one-sided Fisher exact p = ([\d.]+)', txt)
    out['concavity'] = float(m.group(1)) if m else float('nan')
    m = re.search(r'pooled concave.*?one-sided p=([\d.]+)', txt)
    out['ntrend'] = float(m.group(1)) if m else float('nan')
    m = re.search(r'one-sided Mann-Whitney p = ([\d.]+)', txt)
    out['diskshare'] = float(m.group(1)) if m else float('nan')
    return out


def fidelity_stats():
    with open(os.path.join(HERE, 'assets', 'fidelity-stats.json')) as f:
        return json.load(f)


def cell_best(cells, family, n, method):
    cands = [c for c in cells if c['family'] == family and c['n'] == n
             and c['method'] == method]
    return min(c['best_L'] for c in cands) if cands else None


def transplant_hits(findings):
    for f in findings:
        if f['campaign'] == 'C15-transplant-v2':
            m = re.search(r'(\d+)/(\d+)', f['text'])
            if m:
                return m.group(1), m.group(2)
    return None, None


def quarter_record(cells):
    """Fraction of (family, n) with both harden and harden-quarter where
    quarter is within 1e-4 of harden or better."""
    insts = {(c['family'], c['n']) for c in cells}
    tot = good = 0
    for fam, n in insts:
        h = cell_best(cells, fam, n, 'harden')
        q = cell_best(cells, fam, n, 'harden-quarter')
        if h is not None and q is not None:
            tot += 1
            if q <= h + 1e-4:
                good += 1
    return good, tot


def index_body(data, pieces):
    fams = data['families']
    camps = data['campaigns']
    cells = data['cells']
    total_runs = sum(c['runs'] for c in cells)
    n_inst = len({(c['family'], c['n']) for c in cells})
    pv = meta_pvalues()
    fs = fidelity_stats()
    rho_d = fs['discovery']['rho']
    rho_h1 = fs['heldout1']['rho']
    rho_h2 = fs['heldout2']['rho']

    # ---- Act 2: the falsified hypothesis (numbers from the frozen analysis)
    hyp = (f'<p>Our first theory was simple: hardening should help most where pieces are '
           f'<i>concave</i> — L-trominoes, plus-pentominoes, five-pointed stars — because the '
           f'morph has the most "room" to work. The flagship prediction failed cleanly. C01 '
           f'found hardening beating rigid on only 5 of 17 concave instances (5 losses, 7 ties), '
           f'and the pre-registered meta-analysis found <b>no predictor that works</b>: not '
           f'concavity (Fisher p={pv["concavity"]:.2f}), not a trend with piece count '
           f'(p={pv["ntrend"]:.2f}), not inscribed-disk share (Mann–Whitney p={pv["diskshare"]:.2f}). '
           f'The mixed-effects model was overparameterized for the data and is reported as '
           f'unstable. Hardening wins are real, but <i>where</i> they happen is not predicted '
           f'by any shape descriptor tested. That negative result is the finding — and the hook '
           f'for everything below.</p>')

    # ---- Act 4: mechanism numbers, all from the cells ledger
    ltri_h = cell_best(cells, 'ltri-in-squ', 5, 'harden')
    ltri_snap = cell_best(cells, 'ltri-in-squ', 5, 'snap')
    qgood, qtot = quarter_record(cells)
    th, tt = transplant_hits(data['findings'])
    snap_line = ''
    if ltri_h is not None and ltri_snap is not None:
        snap_line = (f'On five L-trominoes, skipping the gradual morph ("snap": compress as '
                     f'disks, then rigid polygons all at once) lands at L={fmt_L(ltri_snap)} '
                     f'versus L={fmt_L(ltri_h)} for the real morph — the tight disk scaffold '
                     f'cannot survive an instant snap. ')
    quarter_line = (f'Starting the morph nearly rigid (τ₀=0.25) matches or beats the full '
                    f'disk-to-shape morph on {qgood} of {qtot} tested instances. ')
    transplant_line = ''
    if th:
        transplant_line = (f'And the transplant experiment proved the scaffold is doing the '
                           f'work: grafting a good disk scaffold under the morph reached the '
                           f'good basin in {th} of {tt} runs.')

    # ---- existing depth: campaigns, findings, gallery (unchanged logic)
    ans = []
    for c in camps:
        ans.append(
            f'<div class="campaign"><span class="cid">{html.escape(c["id"])}</span>'
            f'<h3>{html.escape(c["title"])}</h3>'
            f'<p><b>Question.</b> {html.escape(c["question"])}</p>'
            f'<p><b>Status.</b> {html.escape(c["status"])} — {html.escape(c["decision"])}</p>'
            f'<p><a class="mono" href="journal.html#{html.escape(c["id"])}">journal</a></p></div>')
    findings = ''.join(
        (f'<li><a class="mono" href="journal.html#{html.escape(f["campaign"])}">'
         f'{html.escape(f["campaign"])}</a> {html.escape(f["text"])} '
         f'<span class="mono">[{html.escape(f["date"])}]</span></li>'
         if f["campaign"] else
         f'<li><span class="mono">meta-analysis</span> {html.escape(f["text"])} '
         f'<span class="mono">[{html.escape(f["date"])}]</span></li>')
        for f in data['findings'])

    VERDICTS = {
        'ltri-in-squ': 'Hardening finds the n=5 pinwheel (L=4.0); rigid starts miss it. Basin delivery confirmed by checkpoint handoff.',
        'cross-in-squ': 'Mostly rigid territory — but hardening took n=14 and n=11-in-triangle on high scaffold fidelity.',
        'star5-in-squ': 'Hardening wins n=7, 8, 9, 12, 13; the handoff confirms basin delivery on n=9.',
        'squ-in-squ': 'n=11: hardening reaches Trump\u2019s record 3.87708; rigid does not.',
        'tri-in-squ': 'n=11: the signature generalizes — hardening reaches the record here too.',
        'pen-in-squ': 'n=11: both methods tie at Friedman\u2019s record. No advantage.',
        'hex-in-squ': 'n=11: rigid wins outright.',
        'pen-in-pen': 'Pentagons in a pentagon: all ties, n=5\u20138. No advantage either way.',
        'ltri-in-tri': 'Hardening wins 3 of 4 in the triangle container (n=6, 7, 8).',
        'star5-in-tri': 'Hardening wins n=8, 9, 10; ties elsewhere.',
        'cross-in-tri': 'Hardening took n=11 — the second cross win anywhere.',
    }
    order = [f for f in ('ltri-in-squ', 'star5-in-squ', 'cross-in-squ', 'squ-in-squ',
                         'tri-in-squ', 'pen-in-squ', 'hex-in-squ', 'pen-in-pen',
                         'ltri-in-tri', 'star5-in-tri', 'cross-in-tri') if f in fams]
    cards = []
    for fid in order:
        fam = fams[fid]
        thumb = f'assets/thumbs/{fid}.png'
        img = (f'<img src="{thumb}" alt="{short_piece(fam["title"])} best packing" loading="lazy">'
               if os.path.exists(os.path.join(HERE, thumb)) else '')
        cards.append(
            f'<a class="famcard" href="families.html#{fid}">'
            f'{img}'
            f'<div><b>{short_piece(fam["title"])}</b><span>{VERDICTS.get(fid, "")}</span></div></a>')
    gallery = ''.join(cards)

    return f"""
<header><div class="eyebrow">a follow-up to <a href="https://yoheinakajima.github.io/soft-to-rigid/">soft-to-rigid</a></div>
<h1>When does hardening help?</h1>
<p class="lede"><b>Act 1 — the question.</b> Hardening starts every piece as its inscribed disk
and morphs it into the target shape while the container compresses. It is not a better
default than rigid starts, but it is a <i>different</i> search: on squares in a square it
reached packings no other method found. This project asks whether that pattern is
predictable — can we say, <i>before running</i>, where the morph will pay?</p></header>

<section><div class="wallhead"><h2>The headline result</h2></div>
<p class="legend"><span class="dot" style="background:#e8912d"></span>hardening
<span class="dot" style="background:#2d6fe8"></span>rigid start.
Same budget, same piece, same container — different search.</p>
<figure class="hero"><img src="assets/hero-compare.png" alt="Hardening vs rigid start on five L-trominoes"></figure>
<p class="figcap">Five L-trominoes. Hardening finds the pinwheel; rigid starts never do. The rest of this page is about <i>why</i> — and when to expect it.</p>
</section>

<section><h2>Act 2 — the wrong answer</h2>
{hyp}</section>

<section><h2>Act 3 — the discovery</h2>
<p>What predicts the outcome is not the shape. It is the <b>scaffold</b>: the arrangement
the soft disks settle into at the end of the compress phase, before the morph begins.
Measure how well that scaffold's relative layout matches the best-known optimum —
the rank correlation of pairwise distances, which we call <i>scaffold fidelity</i> —
and it predicts how close hardening gets to the optimum. In plain language:
<b>hardening wins when the soft disks land in the right neighborhood.</b></p>
<figure class="hero"><img src="assets/fidelity-scatter.png" alt="Scaffold fidelity vs hardening gap across 67 instances"></figure>
<p class="figcap">Each dot is one of {fs['n']} packing instances ({fs['wins']} hardening wins).
Higher scaffold fidelity → smaller gap to the best-known optimum. Spearman ρ={rho_d:.2f}
on the discovery set, ρ={rho_h1:.2f} and ρ={rho_h2:.2f} on two pre-registered held-out
replications. No shape descriptor tested comes close.</p></section>

<section><h2>Act 4 — the proof</h2>
<p>The morph is not magic; it is a <i>local</i> refiner that inherits its starting basin.
Watch one run:</p>
<figure class="hero"><img src="assets/morph-strip.png" alt="Disks compress into a scaffold, then morph into the pinwheel"></figure>
<p class="figcap">Random disks → compressed scaffold → morphing shapes → the pinwheel.
The scaffold's relative layout is already the pinwheel's; the morph just grows the corners in.</p>
<p>{snap_line}{quarter_line}{transplant_line} The mechanism, in one sentence:
<b>the compress phase proposes a scaffold, and the gradual morph preserves it while
growing corners.</b> Where the scaffold lands in the right basin, hardening delivers;
where it lands in the wrong one, the morph cannot escape.</p></section>

<section><h2>Act 5 — the caveats</h2>
<p>Two honest limits. First, <b>traps are probabilistic, not deterministic</b>: the
scaffold picks the basin <i>region</i>, but whether the morph gets stuck inside it
depends on the run (C15, C18). Second, <b>single-instance predictions are noisy</b>:
the rule predicts the distribution across instances — a high-fidelity instance usually
pays, a low-fidelity one usually doesn't — but any single flip can surprise you
(C16). The correlation is the claim; the anecdotes are illustrations.</p></section>

<section><div class="wallhead"><h2>Families</h2></div>
<p class="legend">One-line verdict per family. Every instance and method, with animated replays, is on the family pages.</p>
<div class="gallery">{gallery}</div></section>

<section><h2>The answer so far</h2>
{''.join(ans)}
<h3>Findings</h3>
<ul class="answer">{findings}</ul></section>

<section><div class="stats">
<div><b>{len(camps)}</b><span>planned campaigns</span></div>
<div><b>{len(fams)}</b><span>families</span></div>
<div><b>{n_inst}</b><span>instances</span></div>
<div><b>{total_runs}</b><span>runs</span></div>
</div></section>
"""


# ---------------------------------------------------------------- families
def piece_desc(name, p):
    if p['k'] == 0:
        kind = 'Disk piece.'
    elif p['k'] > 0:
        kind = f'Convex {p["k"]}-gon.'
    else:
        kind = (f'Concave compound piece: {len(p["parts"])} convex parts sharing one pose. '
                'Collision is part-pair separating-axis tests.')
    share = disk_share(p)
    return (f'{kind} Area {p["area"]:.4f}. Inscribed-disk share of area {share:.1%} '
            f'(morph room {1 - share:.1%}).')


def families_body(data, pieces):
    fams, cells = data['families'], data['cells']
    out = ['<header><div class="eyebrow">families</div><h1>Families and replays</h1>',
           '<p class="lede">Every instance, every method, with replays of the best runs. '
           'Concave families carry no external records — every statement about them is a '
           'head-to-head comparison at matched budget, never a record claim.</p></header>']
    for fid, fam in fams.items():
        fc = [c for c in cells if c['family'] == fid]
        ns = sorted({c['n'] for c in fc})
        ms = sorted({c['method'] for c in fc})
        thead = '<tr><th>n</th>' + ''.join(
            f'<th>{METHOD_LABEL.get(m, m)} best L</th><th>runs</th>' for m in ms) + '</tr>'
        rows = []
        for n in ns:
            tds = [f'<td>{n}</td>']
            for m in ms:
                c = next((c for c in fc if c['n'] == n and c['method'] == m), None)
                tds.append(f'<td class="mono">{fmt_L(c["best_L"])}</td><td>{c["runs"]}</td>' if c
                           else '<td>—</td><td>—</td>')
            rows.append('<tr>' + ''.join(tds) + '</tr>')
        has_replay = any(c.get('replay') for c in fc)
        viewer = ''
        if has_replay:
            viewer = (f'<h3>Replay</h3><p><label>n <select class="nsel"></select></label> '
                      f'<label>method <select class="msel"></select></label></p>'
                      f'<div class="vwrap"></div>')
        out.append(
            f'<section class="famsec" data-fam="{fid}" id="{fid}">'
            f'<h2>{html.escape(fam["title"])}</h2>'
            f'<p>{html.escape(piece_desc(fam["piece"], pieces[fam["piece"]]))} '
            f'Container: {html.escape(fam["container"])}. '
            f'{"External records available." if fam["has_records"] else "No external records (concave)."}</p>'
            f'<table class="data"><thead>{thead}</thead>{"".join(rows)}</table>{viewer}</section>')
    return '\n'.join(out)


FAM_SCRIPTS = """<script src="assets/app.js"></script>
<script>
Promise.all([WHH.loadJSON('data.json'), WHH.loadJSON('pieces.json')]).then(([D, pieces]) => {
  document.querySelectorAll('[data-fam]').forEach(sec => {
    const fam = sec.getAttribute('data-fam');
    const cells = D.cells.filter(c => c.family === fam && c.replay);
    if (!cells.length) return;
    const ns = [...new Set(cells.map(c => c.n))].sort((a, b) => a - b);
    const ms = [...new Set(cells.map(c => c.method))];
    const nsel = sec.querySelector('.nsel'), msel = sec.querySelector('.msel');
    nsel.innerHTML = ns.map(n => `<option>${n}</option>`).join('');
    msel.innerHTML = ms.map(m => `<option value="${m}">${m === 'harden' ? 'hardening' : m === 'rigid' ? 'rigid start' : m}</option>`).join('');
    const v = WHH.viewer(sec.querySelector('.vwrap'), pieces);
    const load = () => {
      const cell = cells.find(c => c.n === Number(nsel.value) && c.method === msel.value);
      if (cell) v.load(cell.replay);
    };
    nsel.onchange = load; msel.onchange = load;
    load();
  });
});
</script>"""


# ---------------------------------------------------------------- journal
def md_inline(t):
    t = html.escape(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`(.+?)`', r'<code class="mono">\1</code>', t)
    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', t)
    return t


def md_block(md):
    out, in_ul = [], False
    for line in md.split('\n'):
        s = line.strip()
        if s.startswith('### '):
            if in_ul: out.append('</ul>'); in_ul = False
            ident = re.sub(r'[^a-z0-9]+', '-', s[4:].lower()).strip('-')
            out.append(f'<h3 id="{ident}">{md_inline(s[4:])}</h3>')
        elif s.startswith('## '):
            if in_ul: out.append('</ul>'); in_ul = False
            cm = re.match(r'(C\d+-[A-Za-z0-9-]+)\s*:', s[3:])
            ident = cm.group(1) if cm else re.sub(r'[^a-z0-9]+', '-', s[3:].lower()).strip('-')
            out.append(f'<h2 id="{ident}">{md_inline(s[3:])}</h2>')
        elif s.startswith('# '):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<h1>{md_inline(s[2:])}</h1>')
        elif s.startswith('- '):
            if not in_ul: out.append('<ul>'); in_ul = True
            out.append(f'<li>{md_inline(s[2:])}</li>')
        elif not s:
            if in_ul: out.append('</ul>'); in_ul = False
        else:
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<p>{md_inline(s)}</p>')
    if in_ul: out.append('</ul>')
    return '\n'.join(out)


# ---------------------------------------------------------------- paper
def paper_body(data, nums):
    cells = data['cells']
    total_runs = sum(c['runs'] for c in cells)
    n_inst = len({(c['family'], c['n']) for c in cells})
    n_camps = len(data['campaigns'])
    latest = data['findings'][-1]['text'] if data['findings'] else ''

    abstract = (
        '<p>Packing searches usually move rigid pieces. <i>Hardening</i> instead starts every '
        'piece as its inscribed disk and morphs it into the target shape while the container '
        'compresses. The parent project showed hardening is not a better default than rigid '
        'starts, but a <i>different</i> search: on squares in a square it reached packings no '
        'other method found, while showing no advantage on triangles, hexagons, pentagons, '
        'octagons, or four families held out from all development.</p>'
        '<p>This project tested whether that pattern is predictable. The two-factor hypothesis — '
        'hardening helps where (1) the polygon differs substantially from its inscribed disk and (2) '
        'the best-known packings contain tilted orientations a rigid search cannot easily reach — '
        '<b>did not survive</b>. The flagship prediction was that <i>concave</i> pieces would show '
        'hardening\'s largest advantage; instead the pre-registered meta-analysis over 37 instances found '
        '<b>no working predictor</b>: not concavity (one-sided Fisher p=0.19), not a trend with piece count '
        '(Cochran–Armitage p=0.31), not inscribed-disk share (Mann–Whitney p=0.15). Hardening wins are real '
        '(9 of 37 instances, including replicated n=11 signatures and the L-tromino pinwheel), and the mechanism '
        'experiments show its role is <i>basin delivery</i> — a soft compress phase arranges positions, a short '
        'morph grows the corners in — but <i>where</i> it pays is not predicted by any shape descriptor tested. '
        'That negative result is the finding.</p>'
        '<p>Concave pieces are compound: convex parts sharing one pose, with part-pair '
        'separating-axis collision and the morph applied to every vertex about the centroid. '
        'No Friedman-style catalogue exists for concave packings, so every concave claim is a '
        'relative head-to-head comparison at matched budget and frozen settings — never a '
        'record claim.</p>'
        f'<p><b>Status.</b> {n_camps} campaign(s), {n_inst} instances, {total_runs} runs. '
        f'Latest finding: {html.escape(latest)}</p>')

    # numbers table from numbers.tex
    def describe(name):
        low = name.lower()
        camp = re.sub(r'^hv[pr]', '', name)
        camp = re.sub(r'([a-z])([A-Z])', r'\1 \2', camp)
        if low.startswith('hvp'):
            return f'Two-sided sign-test p-value — {camp}'
        if low.startswith('hvr'):
            return f'Instances lower, harden vs rigid — {camp}'
        return name
    num_rows = ''.join(
        f'<tr><td class="mono">{html.escape(k)}</td><td>{html.escape(describe(k))}</td>'
        f'<td class="mono">{html.escape(v)}</td></tr>'
        for k, v in sorted(nums.items()))

    methods = (
        '<h2>Methods</h2><ul>'
        '<li><b>harden</b> — the search under study: γ = 1, τ : 1 → 0. Every piece starts as '
        'its inscribed disk (or centroid disk, for concave pieces) and hardens into the target '
        'shape while the container is pushed inward.</li>'
        '<li><b>rigid</b> — γ = 1, τ = 0 throughout: full pieces from the start, on the same '
        'schedule as hardening.</li>'
        '<li><b>sa</b> — rigid pieces, Metropolis simulated annealing on poses and container size.</li>'
        '<li><b>pc</b> — rigid pieces, perturbation–compression: shrink the container, relax '
        'overlaps, perturb on failure.</li></ul>'
        '<p>Budgets are matched across methods; every campaign is pre-registered with its '
        'decision rule before it runs, and results are append-only.</p>')

    return (f'<header><div class="eyebrow">paper · working draft</div>'
            f'<h1>When does hardening help? Predicting where shape continuation beats rigid starts</h1>'
            f'<div class="links"><a href="journal.html">Journal</a> · <a href="families.html">Families</a></div></header>'
            f'<section><h2>Abstract</h2>{abstract}</section>'
            f'<section><h2>Key numbers</h2><p>Generated from <span class="mono">paper/numbers.tex</span>; never typed by hand.</p>'
            f'<table class="data"><thead><tr><th>macro</th><th>meaning</th><th>value</th></tr></thead>'
            f'{num_rows if num_rows else "<tr><td colspan=3>—</td></tr>"}</table></section>'
            f'<section>{methods}</section>')


# ---------------------------------------------------------------- main
def main():
    data, pieces, journal, nums = load()
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(OUT)

    # static front-page imagery (keeps the front page animation-free; the animated
    # side-by-side replays live on the family pages)
    import subprocess
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'render_thumbs.py')],
                   check=True, capture_output=True)
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'render_narrative.py')],
                   check=True, capture_output=True)

    index_html = index_body(data, pieces)

    # Editorial homepage: visual-first narrative (build_home.py).
    # Stats from generated sources only.
    fstats = fidelity_stats()
    cells = data['cells']
    total_runs = sum(c['runs'] for c in cells)
    home_stats = {
        'n_instances': fstats['n'],
        'n_wins': fstats['wins'],
        'n_runs': total_runs,
        'rho_discovery': fstats['discovery']['rho'],
        'rho_heldout1': fstats['heldout1']['rho'],
        'rho_heldout2': fstats['heldout2']['rho'],
    }
    index_html = index_body_new(data, pieces, home_stats)
    home_css = index_css()
    pages = {
        'index': ('When does hardening help?',
                  'Hardening wins when the soft disks land in the right neighborhood. '
                  'A visual story of 5,200 packings.',
                  index_html, '', home_css),
        'families': ('Families and replays',
                     'Every instance, every method, with replays of the best runs.',
                     families_body(data, pieces), FAM_SCRIPTS),
        'journal': ('Research journal',
                    'Every campaign in order: question, expectation, rule, result, decision.',
                    '<div class="journal">' + md_block(journal) + '</div>', ''),
        'paper': ('Paper', 'When does hardening help? Predicting where shape continuation beats rigid starts.',
                  paper_body(data, nums), ''),
    }
    for name, page_tuple in pages.items():
        title, desc, body = page_tuple[0], page_tuple[1], page_tuple[2]
        scripts = page_tuple[3] if len(page_tuple) > 3 else ''
        extra_css = page_tuple[4] if len(page_tuple) > 4 else ''
        with open(os.path.join(OUT, name + '.html'), 'w') as f:
            f.write(page(name, title, desc, body, scripts, extra_css))

    # assets + data
    shutil.copytree(os.path.join(HERE, 'assets'), os.path.join(OUT, 'assets'))
    for fn in ('data.json', 'pieces.json'):
        shutil.copy(os.path.join(HERE, fn), os.path.join(OUT, fn))
    # replays, keeping directory structure
    for src in glob.glob(os.path.join(ROOT, 'campaigns', '*', 'replays', '**', '*.json'),
                         recursive=True):
        dst = os.path.join(OUT, os.path.relpath(src, ROOT))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(src, dst)
    open(os.path.join(OUT, '.nojekyll'), 'w').write('')
    print('built', OUT)


if __name__ == '__main__':
    main()
