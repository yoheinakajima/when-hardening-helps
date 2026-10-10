#!/usr/bin/env python3
"""Meta-analysis for when-hardening-helps (pre-registered analysis/meta-plan.md).

Unit: (family, n). Y = 1 if harden best-of + 1e-4 < rigid best-of, else 0.
Dedup rule (recorded 2026-10-09): repeated (family,n) across campaigns -> use the
largest seed budget; ties (squ n=11: C02a and C04 both 32 seeds) -> use the
primary campaign (C02a), with the replicate reported as an agreement check.
"""
import json, glob, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 1e-4

# ---------------- load runs ----------------
runs = []
for f in glob.glob(os.path.join(ROOT, 'campaigns', '*', 'runs-w*.jsonl')):
    camp = f.split(os.sep)[-2]
    for line in open(f):
        line = line.strip()
        if not line:
            continue
        r = json.loads(line)
        r['_camp'] = camp
        runs.append(r)

# ---------------- inclusion set ----------------
# AMENDMENT 2026-10-10 (recorded, not a hypothesis change): the frozen plan
# misremembered C01's design as ltri/cross/star5 n=5..8 and squ/tri n=5..8.
# The actual C01 design (in campaigns/C01-concave-pilot/plan.json, pre-C04) is:
# ltri n=5..10, cross n=4..8, star5 n=5..10, squ n=8..12, tri n=8..10.
# The plan's *intent* ("C01 concave pilot cells + C01 convex controls") is kept;
# the n-ranges are corrected to the real design. C03/C05 stay excluded per plan
# (their harden/rigid arms exist but the plan excluded those campaigns).
INCLUDE = {
    'C01-concave-pilot': ([(f,n,16) for f in ('ltri-in-squ',) for n in (5,6,7,8,9,10)]
                        + [(f,n,16) for f in ('cross-in-squ',) for n in (4,5,6,7,8)]
                        + [(f,n,16) for f in ('star5-in-squ',) for n in (5,6,7,8,9,10)]
                        + [(f,n,16) for f in ('squ-in-squ',) for n in (8,9,10,11,12)]
                        + [(f,n,16) for f in ('tri-in-squ',) for n in (8,9,10)]),
    'C02a-baselines-replication': [('ltri-in-squ',5,32), ('star5-in-squ',9,32), ('squ-in-squ',11,32)],
    'C04-convex-rare': [(f,11,32) for f in ('squ-in-squ','tri-in-squ','pen-in-squ','hex-in-squ')],
    'C06-pen-in-pen': [('pen-in-pen',n,16) for n in (5,6,7,8)],
    'C07-concave-scale': [(f,n,16) for f in ('ltri-in-squ','cross-in-squ') for n in (9,10,11)]
                       + [('star5-in-squ',n,16) for n in (10,11)],
}
# dedup: (family, n) -> (campaign, seeds) with largest seeds; tie -> earliest campaign
pick = {}
for camp, cells in INCLUDE.items():
    for fam, n, seeds in cells:
        key = (fam, n)
        if key not in pick or seeds > pick[key][1]:
            pick[key] = (camp, seeds)

# ---------------- best-of per instance ----------------
best = {}  # (fam, n, method) -> (L, campaign)
for r in runs:
    key = (r['family'], r['n'])
    if key not in pick:
        continue
    camp, _seeds = pick[key]
    if r['_camp'] != camp:
        continue
    m = r['method']
    if m not in ('harden', 'rigid'):
        continue
    k = (r['family'], r['n'], m)
    if k not in best or r['L'] < best[k][0]:
        best[k] = (r['L'], r['_camp'])

# ---------------- covariates from pieces.json ----------------
pieces = json.load(open(os.path.join(ROOT, 'site', 'pieces.json')))

def reflex_count(outline):
    # outline: flat [x0,y0,x1,y1,...]; count reflex (interior angle > 180) vertices
    n = len(outline) // 2
    pts = [(outline[2*i], outline[2*i+1]) for i in range(n)]
    # signed area for orientation
    area2 = sum(pts[i][0]*pts[(i+1)%n][1] - pts[(i+1)%n][0]*pts[i][1] for i in range(n))
    ccw = area2 > 0
    cnt = 0
    for i in range(n):
        x0,y0 = pts[(i-1)%n]; x1,y1 = pts[i]; x2,y2 = pts[(i+1)%n]
        cross = (x1-x0)*(y2-y1) - (y1-y0)*(x2-x1)
        # reflex if turn is clockwise while polygon is ccw (or vice versa)
        if (cross < 0) == ccw:
            cnt += 1
    return cnt

def symmetry_order(outline, tol=1e-4):
    n = len(outline)//2
    pts = [(outline[2*i], outline[2*i+1]) for i in range(n)]
    cx = sum(p[0] for p in pts)/n; cy = sum(p[1] for p in pts)/n
    rp = [(x-cx, y-cy) for x,y in pts]
    for k in range(n, 0, -1):
        if n % k:
            continue
        ang = 2*math.pi/k
        c, s = math.cos(ang), math.sin(ang)
        ok = True
        for x, y in rp:
            rx, ry = x*c - y*s, x*s + y*c
            if not any((rx-bx)**2 + (ry-by)**2 < tol*tol for bx,by in rp):
                ok = False; break
        if ok:
            return k
    return 1

PIECE_OF = {'ltri-in-squ':'ltri','cross-in-squ':'cross','star5-in-squ':'star5',
            'squ-in-squ':'square','tri-in-squ':'triangle','pen-in-squ':'pentagon',
            'hex-in-squ':'hexagon','pen-in-pen':'pentagon'}
CONTAINER_SIDES = {'squ':4, 'pen':5}

cov = {}
for fam, piece_name in PIECE_OF.items():
    P = pieces[piece_name]
    concave = 1 if P['k'] < 0 else 0
    disk_share = math.pi * P['rho']**2 / P['area']
    cov[fam] = {
        'concave': concave,
        'n_reflex': reflex_count(P['outline']) if concave else 0,
        'disk_share': disk_share,
        'symmetry': symmetry_order(P['outline']),
        'container_sides': CONTAINER_SIDES[fam.split('-in-')[1]],
    }

# ---------------- build dataset ----------------
rows = []
for (fam, n), (camp, seeds) in sorted(pick.items()):
    h = best.get((fam,n,'harden')); ri = best.get((fam,n,'rigid'))
    assert h and ri, f"missing data for {(fam,n)}"
    Y = 1 if h[0] + TOL < ri[0] else 0
    rows.append({'family':fam,'n':n,'camp':camp,'seeds':seeds,
                 'harden':h[0],'rigid':ri[0],'Y':Y, **cov[fam]})
print(f"instances: {len(rows)}  events (Y=1): {sum(r['Y'] for r in rows)}")

print("\n--- dataset ---")
print(f"{'family':14} {'n':>3} {'seeds':>5} {'harden':>10} {'rigid':>10} Y concav refl disksh sym cside")
for r in rows:
    print(f"{r['family']:14} {r['n']:>3} {r['seeds']:>5} {r['harden']:>10.4f} {r['rigid']:>10.4f} "
          f"{r['Y']} {r['concave']:>6} {r['n_reflex']:>4} {r['disk_share']:>6.3f} {r['symmetry']:>3} {r['container_sides']:>5}")

json.dump(rows, open(os.path.join(ROOT,'analysis','meta-dataset.json'),'w'), indent=1)
print("\nwrote analysis/meta-dataset.json")

# ---------------- agreement check on duplicates ----------------
print("\n--- duplicate agreement check ---")
for fam, n in [('ltri-in-squ',5),('squ-in-squ',11)]:
    for camp in ('C01-concave-pilot','C02a-baselines-replication','C04-convex-rare'):
        hh = min((r['L'] for r in runs if r['_camp']==camp and r['family']==fam and r['n']==n and r['method']=='harden'), default=None)
        rr = min((r['L'] for r in runs if r['_camp']==camp and r['family']==fam and r['n']==n and r['method']=='rigid'), default=None)
        if hh is not None:
            print(f"{fam} n={n} {camp}: harden {hh:.4f} rigid {rr:.4f} Y={1 if hh+TOL<rr else 0}")
