"""Render narrative visuals for the front page (all from real data, nothing hand-typed):
  - site/assets/fidelity-scatter.png : scaffold fidelity vs hardening's gap to optimum
  - site/assets/fidelity-stats.json  : numbers the page text needs (rhos, counts)
  - site/assets/morph-strip.png      : 4 frames of a real harden run (disks -> pinwheel)
Usage: python3 scripts/render_narrative.py
"""
import json, glob, math, os, sys
import numpy as np
from scipy import stats
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from render_thumbs import draw_packing, COLORS

CAMS = os.path.join(ROOT, 'campaigns')
ASSETS = os.path.join(ROOT, 'site', 'assets')


# ---------- fidelity machinery (mirrors analysis/a12_a14.py) ----------
def dist_matrix(poses):
    n = len(poses) // 3
    xy = np.array([(poses[3 * i], poses[3 * i + 1]) for i in range(n)])
    return np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=-1)


def spearman_dmat(a, b):
    ua = a[np.triu_indices(a.shape[0], 1)]
    ub = b[np.triu_indices(b.shape[0], 1)]
    if len(ua) < 3:
        return float('nan')
    r, _ = stats.spearmanr(ua, ub)
    return r


def find_replay(family, n, method, prefer_camp=None):
    pat = f"{family}_n{n}_{method}_B1_default.json"
    cands = glob.glob(os.path.join(CAMS, '*/replays', pat))
    if not cands:
        return None
    if prefer_camp:
        for c in cands:
            if f'/{prefer_camp}/' in c:
                return c
    best, bestL = None, math.inf
    for c in cands:
        try:
            r = json.load(open(c))
            if r['L'] < bestL:
                best, bestL = c, r['L']
        except Exception:
            pass
    return best


def compress_end_poses(rep):
    frs = [f for f in rep['frames'] if f['ph'] == 'compress']
    return frs[-1]['p'] if frs else None


METHODS = ['harden', 'harden-quarter', 'rigid', 'snap']


def global_best(family, n, method):
    """Best L for (family, n, method) across ALL campaigns (current knowledge)."""
    bestL = math.inf
    for f in glob.glob(os.path.join(CAMS, '*/runs-w*.jsonl')):
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
            except Exception:
                continue
            if r.get('family') == family and r.get('n') == n and r.get('method') == method:
                if r['L'] < bestL:
                    bestL = r['L']
    return bestL


def instance_row(family, n, camp, hL, rL, batch):
    # Win label uses CURRENT best knowledge across all campaigns, not the
    # originating campaign's snapshot (e.g. C13's cross-n=12 win was withdrawn
    # after C16/C18 showed rigid wins with fresh/shifted seeds).
    gh, gr = global_best(family, n, 'harden'), global_best(family, n, 'rigid')
    Y = 1 if gh + 1e-4 < gr else 0
    fid, hgap = math.nan, math.nan
    rp = find_replay(family, n, 'harden', camp)
    if rp:
        rep = json.load(open(rp))
        sc = compress_end_poses(rep)
        if sc is not None:
            Ds = dist_matrix(sc)
            Dopt, bestL = None, math.inf
            for m in METHODS:
                rp2 = find_replay(family, n, m)
                if rp2:
                    r2 = json.load(open(rp2))
                    if r2['L'] < bestL:
                        bestL, Dopt = r2['L'], dist_matrix(r2['frames'][-1]['p'])
            if Dopt is not None:
                fid = spearman_dmat(Ds, Dopt)
                hgap = hL - bestL
    return dict(family=family, n=n, Y=Y, margin=rL - hL,
                fidelity=fid, hgap=hgap, batch=batch)


def build_dataset():
    rows = []
    meta = json.load(open(os.path.join(ROOT, 'analysis', 'meta-dataset.json')))
    for r in meta:
        rows.append(instance_row(r['family'], r['n'], r['camp'],
                                r['harden'], r['rigid'], 'discovery'))
    # C10 (triangle containers)
    c10best = {}
    for f in glob.glob(os.path.join(CAMS, 'C10-container-frustration', 'runs-w*.jsonl')):
        for line in open(f):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            k = (r['family'], r['n'], r['method'])
            if k not in c10best or r['L'] < c10best[k]:
                c10best[k] = r['L']
    for fam in ['ltri-in-tri', 'cross-in-tri', 'star5-in-tri']:
        for n in [5, 6, 7, 8]:
            rows.append(instance_row(fam, n, 'C10-container-frustration',
                                     c10best[(fam, n, 'harden')],
                                     c10best[(fam, n, 'rigid')], 'discovery'))
    # C13 + C17 held-out batches
    for camp, insts in [
        ('C13-fidelity-validation',
         [('ltri-in-squ', 12), ('ltri-in-squ', 13), ('star5-in-squ', 12),
          ('cross-in-squ', 12), ('cross-in-squ', 13), ('squ-in-squ', 13),
          ('tri-in-squ', 12), ('ltri-in-tri', 9), ('ltri-in-tri', 10),
          ('star5-in-tri', 9)]),
        ('C17-fidelity-batch2',
         [('ltri-in-squ', 14), ('star5-in-squ', 13), ('cross-in-squ', 14),
          ('squ-in-squ', 14), ('tri-in-squ', 13), ('ltri-in-tri', 11),
          ('star5-in-tri', 10), ('cross-in-tri', 11)]),
    ]:
        best = {}
        for f in glob.glob(os.path.join(CAMS, camp, 'runs-w*.jsonl')):
            for line in open(f):
                r = json.loads(line)
                k = (r['family'], r['n'], r['method'])
                if k not in best or r['L'] < best[k]:
                    best[k] = r['L']
        for fam, n in insts:
            rows.append(instance_row(fam, n, camp, best[(fam, n, 'harden')],
                                     best[(fam, n, 'rigid')],
                                     'heldout1' if camp.startswith('C13') else 'heldout2'))
    return [r for r in rows if math.isfinite(r['fidelity']) and math.isfinite(r['hgap'])]


# ---------- scatter ----------
def render_scatter(rows):
    W, H = 1040, 680
    ml, mr, mt, mb = 78, 30, 46, 72
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    xs = [r['fidelity'] for r in rows]
    ys = [r['hgap'] for r in rows]
    x0, x1 = -1.0, 1.0
    y1 = max(ys) * 1.08

    def X(v):
        return ml + (v - x0) / (x1 - x0) * (W - ml - mr)

    def Y(v):
        return H - mb - v / y1 * (H - mt - mb)

    # grid
    for gv in [-1.0, -0.5, 0.0, 0.5, 1.0]:
        d.line([X(gv), mt, X(gv), H - mb], fill=(235, 232, 224))
        d.text((X(gv) - 12, H - mb + 8), f'{gv:.1f}', fill=(120, 120, 120))
    # zero line
    d.line([X(0), mt, X(0), H - mb], fill=(200, 196, 188), width=2)
    d.text((ml, 8), 'each dot: one packing instance', fill=(100, 100, 100))
    d.text((X(-1.0), H - 34), 'scaffold fidelity (disk arrangement vs optimum)', fill=(80, 80, 80))
    d.text((8, mt), "hardening's gap to best-known optimum", fill=(80, 80, 80))

    wins = [r for r in rows if r['Y'] == 1]
    rest = [r for r in rows if r['Y'] == 0]
    for r in rest:
        x, y = X(r['fidelity']), Y(r['hgap'])
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(148, 163, 184))
    for r in wins:
        x, y = X(r['fidelity']), Y(r['hgap'])
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=(232, 145, 45),
                  outline=(160, 90, 20), width=2)
    # legend
    lx, ly = W - mr - 220, mt + 10
    d.ellipse([lx, ly, lx + 12, ly + 12], fill=(232, 145, 45), outline=(160, 90, 20), width=2)
    d.text((lx + 18, ly - 2), f'hardening win (n={len(wins)})', fill=(60, 60, 60))
    d.ellipse([lx, ly + 24, lx + 12, ly + 36], fill=(148, 163, 184))
    d.text((lx + 18, ly + 22), f'tie / rigid wins (n={len(rest)})', fill=(60, 60, 60))

    out = os.path.join(ASSETS, 'fidelity-scatter.png')
    img.save(out)
    print('wrote', out)
    return {'n': len(rows), 'wins': len(wins)}


def batch_rho(rows, batch):
    sub = [(r['fidelity'], r['hgap']) for r in rows if r['batch'] == batch]
    if len(sub) < 5:
        return None
    r, p = stats.spearmanr([s[0] for s in sub], [s[1] for s in sub])
    return {'rho': r, 'p': p, 'n': len(sub)}


# ---------- morph strip ----------
def render_strip():
    import math as _m
    from PIL import Image as _I  # noqa
    pieces = json.load(open(os.path.join(ROOT, 'site', 'pieces.json')))
    rel = 'campaigns/C05-morph-parts/replays/ltri-in-squ_n5_harden_B1_default.json'
    rep = json.load(open(os.path.join(ROOT, rel)))
    P = pieces[rep['piece']]
    n = rep['n']
    frames = rep['frames']
    start = frames[0]
    cend = [f for f in frames if f['ph'] == 'compress'][-1]
    morph = [f for f in frames if f['ph'] == 'morph']
    mid = min(morph, key=lambda f: abs(f['u'] - 0.5))
    final = frames[-1]
    picks = [
        (start, '1 - random disks'),
        (cend, '2 - compressed scaffold'),
        (mid, '3 - morphing'),
        (final, '4 - pinwheel  L=%.4f' % final['L']),
    ]
    PW, PH, CAP = 300, 300, 40
    img = Image.new('RGB', (PW * 4, PH + CAP), 'white')
    d = ImageDraw.Draw(img)
    for k, (fr, label) in enumerate(picks):
        g, u = fr['g'], fr['u']
        L = fr['L']
        p = fr['p']
        size = PW - 12
        sc = size / L
        cx, cy = k * PW + PW / 2, PH / 2
        # container box
        d.rectangle([cx - L * sc / 2, cy - L * sc / 2,
                     cx + L * sc / 2, cy + L * sc / 2],
                    outline=(180, 180, 180), width=2)
        core_s = g * (1 - u)
        for i in range(n):
            x, y, t = p[3 * i], p[3 * i + 1], p[3 * i + 2]
            c, s = _m.cos(t), _m.sin(t)
            px, py = cx + x * sc, cy - y * sc
            if u > 0.9:
                # disk phase: filled disk of radius g*rho (outlines of
                # degenerate polygons do not stroke, hence explicit ellipse)
                r = g * P['rho'] * sc
                d.ellipse([px - r, py - r, px + r, py + r],
                          fill=(232, 145, 45), outline=(160, 90, 20))
            else:
                for part in P['parts']:
                    pts = []
                    for m_ in range(len(part) // 2):
                        vx, vy = part[2 * m_] * core_s, part[2 * m_ + 1] * core_s
                        wx = x + vx * c - vy * s
                        wy = y + vx * s + vy * c
                        pts.append((cx + wx * sc, cy - wy * sc))
                    if len(pts) > 2:
                        d.polygon(pts, outline=(232, 145, 45),
                                  width=max(1, int(2 * g * u * P['rho'] * sc)))
        d.rectangle([k * PW + 2, 2, k * PW + PW - 2, PH - 2], outline=(210, 206, 198))
        d.text((k * PW + 12, PH + 10), label, fill=(90, 90, 90))
    out = os.path.join(ASSETS, 'morph-strip.png')
    img.save(out)
    print('wrote', out)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    rows = build_dataset()
    info = render_scatter(rows)
    info['discovery'] = batch_rho(rows, 'discovery')
    info['heldout1'] = batch_rho(rows, 'heldout1')
    info['heldout2'] = batch_rho(rows, 'heldout2')
    overall = stats.spearmanr([r['fidelity'] for r in rows], [r['hgap'] for r in rows])
    info['overall'] = {'rho': overall.statistic, 'p': overall.pvalue}
    with open(os.path.join(ASSETS, 'fidelity-stats.json'), 'w') as f:
        json.dump(info, f, indent=1)
    print(json.dumps({k: (round(v['rho'], 3) if isinstance(v, dict) and 'rho' in v else v)
                      for k, v in info.items()}, indent=1))
    render_strip()


if __name__ == '__main__':
    main()
