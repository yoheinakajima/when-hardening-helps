#!/usr/bin/env python3
"""Confirmatory tests for when-hardening-helps (pre-registered analysis/meta-plan.md).

H1: concave instances have higher P(Y=1) than convex (one-sided Fisher exact).
H2: within concave families, P(Y=1) increases with n (Cochran-Armitage trend).
H3: P(Y=1) decreases with disk_share (one-sided Wilcoxon rank-sum: disk_share
    of Y=1 instances < disk_share of Y=0 instances).
Model 1: mixed-effects logistic Y ~ covariates + (1|family); reported as-is,
    including failure/instability (the plan requires reporting the failure directly).
"""
import json, math, os
import numpy as np
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = json.load(open(os.path.join(ROOT, 'analysis', 'meta-dataset.json')))
Y = np.array([r['Y'] for r in rows])

print(f"n={len(rows)}, events={Y.sum()}")
print("=" * 60)

# ---------------- H1: concave vs convex ----------------
conc = np.array([r['concave'] for r in rows])
a = int(((conc == 1) & (Y == 1)).sum())  # concave, Y=1
b = int(((conc == 1) & (Y == 0)).sum())  # concave, Y=0
c = int(((conc == 0) & (Y == 1)).sum())  # convex,  Y=1
d = int(((conc == 0) & (Y == 0)).sum())  # convex,  Y=0
print("\nH1: concave vs convex event rates")
print(f"  concave: {a}/{a+b} = {a/(a+b):.3f}   convex: {c}/{c+d} = {c/(c+d):.3f}")
_, p1 = stats.fisher_exact([[a, b], [c, d]], alternative='greater')
print(f"  one-sided Fisher exact p = {p1:.4f}  -> {'REJECT null (supports H1)' if p1 < 0.05 else 'fail to reject'}")

# ---------------- H2: Cochran-Armitage trend within concave ----------------
print("\nH2: trend of P(Y=1) with n within concave families (Cochran-Armitage)")
for fam in ('ltri-in-squ', 'cross-in-squ', 'star5-in-squ'):
    sub = [r for r in rows if r['family'] == fam]
    ns = sorted(set(r['n'] for r in sub))
    ts = [sum(1 for r in sub if r['n'] == n and r['Y'] == 1) for n in ns]
    ms = [sum(1 for r in sub if r['n'] == n) for n in ns]
    T, M = sum(ts), sum(ms)
    pbar = T / M
    # CA statistic with scores = n
    num = sum(ms[i] * (ns[i] - sum(ms[j]*ns[j] for j in range(len(ns)))/M) * (ts[i]/ms[i] - pbar) for i in range(len(ns)))
    # standard form: Z = sum t_i (x_i - xbar) / sqrt(pbar(1-pbar) * (sum m_i (x_i-xbar)^2 ... ))
    xbar = sum(ms[i]*ns[i] for i in range(len(ns))) / M
    sxx = sum(ms[i]*(ns[i]-xbar)**2 for i in range(len(ns)))
    z = sum((ts[i] - ms[i]*pbar)*(ns[i]-xbar) for i in range(len(ns))) / math.sqrt(pbar*(1-pbar)*sxx) if sxx > 0 and 0 < pbar < 1 else float('nan')
    p2 = 1 - stats.norm.cdf(z) if not math.isnan(z) else float('nan')
    print(f"  {fam:14} n={ns} Y={ts}  Z={z:.3f} one-sided p={p2:.4f}")
# pooled across concave families
sub = [r for r in rows if r['concave'] == 1]
ns = sorted(set(r['n'] for r in sub))
ts = [sum(1 for r in sub if r['n'] == n and r['Y'] == 1) for n in ns]
ms = [sum(1 for r in sub if r['n'] == n) for n in ns]
T, M = sum(ts), sum(ms); pbar = T / M
xbar = sum(ms[i]*ns[i] for i in range(len(ns))) / M
sxx = sum(ms[i]*(ns[i]-xbar)**2 for i in range(len(ns)))
z = sum((ts[i] - ms[i]*pbar)*(ns[i]-xbar) for i in range(len(ns))) / math.sqrt(pbar*(1-pbar)*sxx)
p2p = 1 - stats.norm.cdf(z)
print(f"  {'pooled concave':14} n={ns} Y={ts}  Z={z:.3f} one-sided p={p2p:.4f}")

# ---------------- H3: disk_share ----------------
print("\nH3: disk_share lower among Y=1 (one-sided Wilcoxon rank-sum)")
d1 = [r['disk_share'] for r in rows if r['Y'] == 1]
d0 = [r['disk_share'] for r in rows if r['Y'] == 0]
print(f"  Y=1 disk_share: n={len(d1)} median={np.median(d1):.3f}")
print(f"  Y=0 disk_share: n={len(d0)} median={np.median(d0):.3f}")
_, p3 = stats.mannwhitneyu(d1, d0, alternative='less')
print(f"  one-sided Mann-Whitney p = {p3:.4f}  -> {'REJECT null (supports H3)' if p3 < 0.05 else 'fail to reject'}")

# ---------------- Model 1: mixed-effects logistic ----------------
print("\n" + "=" * 60)
print("Model 1: mixed-effects logistic Y ~ concave + n_reflex + disk_share +")
print("         symmetry + n_pieces + container_sides + (1|family)")
try:
    import statsmodels.api as sm
    import pandas as pd
    df = pd.DataFrame(rows)
    fams = sorted(df['family'].unique())
    df['fam_id'] = df['family'].map({f: i for i, f in enumerate(fams)})
    exog = sm.add_constant(df[['concave','n_reflex','disk_share','symmetry','n','container_sides']].astype(float))
    fam_ids = df['fam_id'].to_numpy(dtype=int)
    n_groups = fam_ids.max() + 1
    exog_vc = np.zeros((len(df), n_groups))
    exog_vc[np.arange(len(df)), fam_ids] = 1.0
    ident = np.zeros(n_groups, dtype=int)  # one shared variance component
    model = sm.BinomialBayesMixedGLM(
        df['Y'].astype(float), exog, exog_vc, ident,
        fep_names=['intercept','concave','n_reflex','disk_share','symmetry','n_pieces','container_sides'],
        vcp_names=['family_sd'])
    res = model.fit_vb()
    print(res.summary())
    fe = np.asarray(res.fe_mean)
    sd = np.asarray(res.fe_sd)
    print("\n  odds ratios (95% CI):")
    for name, m, s in zip(['intercept','concave','n_reflex','disk_share','symmetry','n_pieces','container_sides'], fe, sd):
        print(f"    {name:15} OR={math.exp(m):.3f}  95% CI [{math.exp(m-1.96*s):.3f}, {math.exp(m+1.96*s):.3f}]")
except Exception as e:
    print(f"  MODEL FAILED: {type(e).__name__}: {e}")
    print("  (reported directly per the pre-registered plan)")

print("\nDone.")
