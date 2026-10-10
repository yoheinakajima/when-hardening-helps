#!/usr/bin/env python3
"""A12/A13/A14: scaffold fidelity, basin narrowness, morph commitment timing.
All on existing replays/runs. Read-only.
"""
import json, glob, os, math
import numpy as np
from scipy import stats

ROOT = os.path.expanduser('~/workspace/research/when-hardening-helps')
CAMS = os.path.join(ROOT, 'campaigns')

# ---------- helpers ----------
def dist_matrix(poses):
    """poses: flat [x,y,t]*n -> n x n centroid distance matrix."""
    n = len(poses) // 3
    xy = np.array([(poses[3*i], poses[3*i+1]) for i in range(n)])
    d = np.linalg.norm(xy[:, None, :] - xy[None, :, :], axis=-1)
    return d

def upper(d):
    n = d.shape[0]
    return d[np.triu_indices(n, 1)]

def spearman_dmat(a, b):
    ua, ub = upper(a), upper(b)
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
    # prefer the replay with the best (lowest) final L
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

def final_poses(rep):
    return rep['frames'][-1]['p']

# ---------- dataset: 37 meta + 12 C10 ----------
meta = json.load(open(os.path.join(ROOT, 'analysis/meta-dataset.json')))
inst = [(r['family'], r['n'], r['camp'], r['harden'], r['rigid'], r['Y']) for r in meta]

# C10 instances
c10runs = []
for f in glob.glob(os.path.join(CAMS, 'C10-container-frustration/runs-w*.jsonl')):
    for line in open(f):
        line = line.strip()
        if line:
            c10runs.append(json.loads(line))
c10best = {}
for r in c10runs:
    k = (r['family'], r['n'], r['method'])
    if k not in c10best or r['L'] < c10best[k]:
        c10best[k] = r['L']
COV = {'ltri': (1, 1, 0.0576, 1), 'cross': (1, 4, 0.3142, 4), 'star5': (1, 5, 0.4077, 5)}
for fam in ['ltri-in-tri', 'cross-in-tri', 'star5-in-tri']:
    piece = fam.split('-in-')[0]
    concave, n_reflex, disk_share, symmetry = COV[piece]
    for n in [5, 6, 7, 8]:
        h = c10best[(fam, n, 'harden')]
        rg = c10best[(fam, n, 'rigid')]
        Y = 1 if h + 1e-4 < rg else 0
        inst.append((fam, n, 'C10-container-frustration', h, rg, Y))

print(f"instances: {len(inst)}, wins: {sum(y for *_, y in inst)}")

# ---------- per-instance measures ----------
rows = []
for fam, n, camp, hL, rL, Y in inst:
    margin = rL - hL
    row = dict(family=fam, n=n, camp=camp, Y=Y, margin=margin,
               fidelity=math.nan, narrow=math.nan, commit_u=math.nan)
    # A12: scaffold fidelity
    rp = find_replay(fam, n, 'harden', camp)
    if rp:
        rep = json.load(open(rp))
        sc = compress_end_poses(rep)
        if sc is not None:
            Ds = dist_matrix(sc)
            # D_opt: best final poses across methods
            Dopt, bestL = None, math.inf
            for m in ['harden', 'harden-quarter', 'rigid', 'snap']:
                rp2 = find_replay(fam, n, m)
                if rp2:
                    r2 = json.load(open(rp2))
                    if r2['L'] < bestL:
                        bestL, Dopt = r2['L'], dist_matrix(final_poses(r2))
            if Dopt is not None:
                row['fidelity'] = spearman_dmat(Ds, Dopt)
    # A13: basin narrowness from rigid runs
    rLs = []
    for f in glob.glob(os.path.join(CAMS, camp, 'runs-w*.jsonl')):
        for line in open(f):
            r = json.loads(line.strip())
            if r['family'] == fam and r['n'] == n and r['method'] == 'rigid' and 'L' in r:
                rLs.append(r['L'])
    if rLs:
        b = min(rLs)
        row['narrow'] = 1 - sum(1 for x in rLs if abs(x - b) <= 1e-4) / len(rLs)
        row['n_rigid_seeds'] = len(rLs)
    # A14: morph commitment timing (harden best replay)
    if rp:
        rep = json.load(open(rp))
        Dfin = dist_matrix(final_poses(rep))
        mfr = [f for f in rep['frames'] if f['ph'] == 'morph']
        cu = math.nan
        for f in mfr:
            if spearman_dmat(dist_matrix(f['p']), Dfin) > 0.95:
                cu = f['u']
                break
        row['commit_u'] = cu
    rows.append(row)

fid = np.array([r['fidelity'] for r in rows])
nar = np.array([r['narrow'] for r in rows])
mar = np.array([r['margin'] for r in rows])
Yv = np.array([r['Y'] for r in rows])
cmu = np.array([r['commit_u'] for r in rows])

print("\n=== A12: scaffold fidelity ===")
print(f"  coverage: {np.isfinite(fid).sum()}/{len(rows)}")
ok = np.isfinite(fid)
if ok.sum() > 5:
    w = Yv[ok] == 1
    mw = stats.mannwhitneyu(fid[ok][w], fid[ok][~w], alternative='greater')
    sp = stats.spearmanr(fid[ok], mar[ok])
    print(f"  fidelity | win: mean={fid[ok][w].mean():.3f} (n={w.sum()})  "
          f"non-win: mean={fid[ok][~w].mean():.3f} (n={(~w).sum()})")
    print(f"  Mann-Whitney (win > non-win): p={mw.pvalue:.4f}")
    print(f"  Spearman(fidelity, margin): rho={sp.statistic:.3f}, p={sp.pvalue:.4f}")

print("\n=== A13: basin narrowness ===")
print(f"  coverage: {np.isfinite(nar).sum()}/{len(rows)}")
ok = np.isfinite(nar)
if ok.sum() > 5:
    w = Yv[ok] == 1
    sp = stats.spearmanr(nar[ok], mar[ok])
    print(f"  narrowness | win: mean={nar[ok][w].mean():.3f} (n={w.sum()})  "
          f"non-win: mean={nar[ok][~w].mean():.3f} (n={(~w).sum()})")
    print(f"  Spearman(narrowness, margin): rho={sp.statistic:.3f}, p={sp.pvalue:.4f}")

print("\n=== A14: morph commitment timing (earliest u with corr(final)>0.95) ===")
print(f"  coverage: {np.isfinite(cmu).sum()}/{len(rows)}")
ok = np.isfinite(cmu)
if ok.sum() > 5:
    w = Yv[ok] == 1
    mw = stats.mannwhitneyu(cmu[ok][w], cmu[ok][~w], alternative='less')
    print(f"  commit_u | win: mean={cmu[ok][w].mean():.3f} (n={w.sum()})  "
          f"non-win: mean={cmu[ok][~w].mean():.3f} (n={(~w).sum()})")
    print(f"  Mann-Whitney (win commits earlier): p={mw.pvalue:.4f}")

# per-instance table for the report
print("\n=== per-instance (family n Y margin fidelity narrow commit_u) ===")
for r in rows:
    print(f"{r['family']:18} n={r['n']:2} Y={r['Y']} margin={r['margin']:+.4f} "
          f"fid={r['fidelity']:.3f} nar={r['narrow']:.3f} cu={r['commit_u']:.3f}")
