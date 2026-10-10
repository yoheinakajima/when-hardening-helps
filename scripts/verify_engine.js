// C00 engine verification.
// 1. Differential regression: new engine vs parent engine on convex families (must be bit-identical).
// 2. Concave geometry vs brute force: triangulation validity, overlap sign agreement,
//    gradient finite-difference check.
'use strict';
const NEW = require('../engine/engine2d.js');
const OLD = require('../engine/engine2d-base.js');

let failures = 0;
const ok = (cond, msg) => { if (!cond) { failures++; console.error('FAIL:', msg); } else console.log('ok:', msg); };

// ---------- 1. differential regression (convex) ----------
function canon(res) {
  return JSON.stringify({ L: res.L, evals: res.evals, steps: res.steps,
    poses: res.poses, frames: res.frames.map(f => [f.ph, f.s, f.g, f.u, f.L, f.p]) });
}
const diffCases = [
  { n: 6, piece: 'square', container: 'square', method: 'harden', seed: 1, budget: 0.05, frames: 5 },
  { n: 5, piece: 'triangle', container: 'square', method: 'rigid', seed: 2, budget: 0.05, frames: 5 },
  { n: 4, piece: 'hexagon', container: 'circle', method: 'grow', seed: 3, budget: 0.05, frames: 5 },
  { n: 4, piece: 'pentagon', container: 'square', method: 'sa', seed: 1, budget: 0.05, frames: 5 },
  { n: 5, piece: 'square', container: 'triangle', method: 'pc', seed: 7, budget: 0.05, frames: 5 },
];
for (const cfg of diffCases) {
  const a = canon(OLD.run(Object.assign({}, cfg)));
  const b = canon(NEW.run(Object.assign({}, cfg)));
  ok(a === b, `bit-identical convex: ${cfg.piece}/${cfg.container}/${cfg.method} (L=${JSON.parse(b).L})`);
}

// ---------- 2a. triangulation validity ----------
for (const name of ['ltri', 'cross', 'star5']) {
  const P = NEW.makePiece(name);
  let area = 0;
  for (const t of P.parts) {
    const tA = Math.abs(((t.g[2] - t.g[0]) * (t.g[5] - t.g[1]) - (t.g[4] - t.g[0]) * (t.g[3] - t.g[1])) / 2);
    area += tA;
    ok(tA > 1e-12, `${name}: triangle part has positive area`);
  }
  ok(Math.abs(area - P.area) / P.area < 1e-9, `${name}: part areas sum to piece area (${P.area.toFixed(4)}), nv=${P.nv}`);
  ok(P.rho > 0 && P.rho < P.R, `${name}: 0 < rho (${P.rho.toFixed(4)}) < R (${P.R.toFixed(4)})`);
  // rho disk must be inside the piece: sample points just inside the circle (the closed
  // disk may touch reflex vertices exactly, which strict point-in-polygon rejects)
  let inside = true;
  for (let i = 0; i < 72; i++) {
    const a = 2 * Math.PI * i / 72, x = P.rho * 0.999 * Math.cos(a), y = P.rho * 0.999 * Math.sin(a);
    if (!pointInPoly(x, y, P.g)) { inside = false; break; }
  }
  ok(inside, `${name}: rho-disk about centroid is inside the piece`);
}
function pointInPoly(x, y, g) {
  let c = false; const n = g.length / 2;
  for (let i = 0, j = n - 1; i < n; j = i++) {
    const xi = g[2 * i], yi = g[2 * i + 1], xj = g[2 * j], yj = g[2 * j + 1];
    if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c;
  }
  return c;
}

// ---------- 2b. overlap sign vs brute force (rigid, tau=0) ----------
function segInt(p1, p2, p3, p4) {
  const d = (p2[0] - p1[0]) * (p4[1] - p3[1]) - (p2[1] - p1[1]) * (p4[0] - p3[0]);
  if (Math.abs(d) < 1e-12) return false;
  const t = ((p3[0] - p1[0]) * (p4[1] - p3[1]) - (p3[1] - p1[1]) * (p4[0] - p3[0])) / d;
  const u = ((p3[0] - p1[0]) * (p2[1] - p1[1]) - (p3[1] - p1[1]) * (p2[0] - p1[0])) / d;
  return t > 1e-9 && t < 1 - 1e-9 && u > 1e-9 && u < 1 - 1e-9;
}
function bruteOverlap(P, a, b) { // a,b = [x,y,t]; true if interiors overlap
  const va = [], vb = [];
  const push = (arr, P, p) => { const c = Math.cos(p[2]), d = Math.sin(p[2]);
    for (const part of P.parts) for (let m = 0; m < part.nv; m++) {
      const gx = part.g[2 * m], gy = part.g[2 * m + 1];
      arr.push([p[0] + gx * c - gy * d, p[1] + gx * d + gy * c]);
    } };
  push(va, P, a); push(vb, P, b);
  const edges = (v) => { const e = []; for (let i = 0; i < v.length; i++) e.push([v[i], v[(i + 1) % v.length]]); return e; };
  // NOTE: parts share vertices; edge lists per part are needed, not one ring. Rebuild per part:
  const pedges = (P, p) => { const c = Math.cos(p[2]), d = Math.sin(p[2]), e = [];
    for (const part of P.parts) { const v = [];
      for (let m = 0; m < part.nv; m++) { const gx = part.g[2 * m], gy = part.g[2 * m + 1]; v.push([p[0] + gx * c - gy * d, p[1] + gx * d + gy * c]); }
      for (let i = 0; i < v.length; i++) e.push([v[i], v[(i + 1) % v.length]]);
    } return e; };
  const ea = pedges(P, a), eb = pedges(P, b);
  for (const [p1, p2] of ea) for (const [p3, p4] of eb) if (segInt(p1, p2, p3, p4)) return true;
  // containment: a vertex of A strictly inside B or vice versa (per-part polygons)
  const inPart = (x, y, poly) => { let c = false; for (let i = 0, j = poly.length - 1; i < poly.length; j = i++) {
    const xi = poly[i][0], yi = poly[i][1], xj = poly[j][0], yj = poly[j][1];
    if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; };
  const polys = (P, p) => { const c = Math.cos(p[2]), d = Math.sin(p[2]), out = [];
    for (const part of P.parts) { const v = [];
      for (let m = 0; m < part.nv; m++) { const gx = part.g[2 * m], gy = part.g[2 * m + 1]; v.push([p[0] + gx * c - gy * d, p[1] + gx * d + gy * c]); }
      out.push(v); } return out; };
  const pa = polys(P, a), pb = polys(P, b);
  for (const poly of pa) for (const q of pb) for (const v of q) if (inPart(v[0], v[1], poly)) return true;
  for (const poly of pb) for (const q of pa) for (const v of q) if (inPart(v[0], v[1], poly)) return true;
  return false;
}
{
  let agree = 0, total = 0, signErr = 0;
  const rng = (() => { let s = 42; return () => (s = (s * 1103515245 + 12345) & 0x7fffffff) / 0x7fffffff; })();
  for (const name of ['ltri', 'cross', 'star5']) {
    const P = NEW.makePiece(name), C = NEW.makeContainer('square');
    for (let t = 0; t < 400; t++) {
      const a = [(rng() - 0.5) * 6, (rng() - 0.5) * 6, rng() * 2 * Math.PI];
      const b = [a[0] + (rng() - 0.5) * 4 * P.R, a[1] + (rng() - 0.5) * 4 * P.R, rng() * 2 * Math.PI];
      const sd = NEW.rigidSd(P, a, b);
      const brute = bruteOverlap(P, a, b);
      total++;
      const s = sd < -1e-9 ? 'overlap' : sd > 1e-9 ? 'separate' : 'touch';
      if ((s === 'overlap') === brute) agree++; else if (s !== 'touch') signErr++;
    }
  }
  ok(signErr === 0, `concave overlap sign: ${agree}/${total} agree, ${signErr} hard disagreements (rest touching)`);
}

// ---------- 2c. gradient finite-difference check (concave, intermediate tau) ----------
{
  const P = NEW.makePiece('ltri'), C = NEW.makeContainer('square');
  const st = new NEW.State(2, P, C, 5);
  st.X[0] = 0.3; st.Y[0] = -0.2; st.T[0] = 0.7; st.X[1] = 1.1; st.Y[1] = 0.4; st.T[1] = 2.1;
  st.gam = 1; st.tau = 0.35; st.L = 6;
  const grad = NEW.gradient(st);
  const E = (xx) => { // energy recomputed with poses xx=[x0,y0,t0,x1,y1,t1]
    const s2 = new NEW.State(2, P, C, 5);
    s2.X[0] = xx[0]; s2.Y[0] = xx[1]; s2.T[0] = xx[2]; s2.X[1] = xx[3]; s2.Y[1] = xx[4]; s2.T[1] = xx[5];
    s2.gam = 1; s2.tau = 0.35; s2.L = 6;
    const g2 = NEW.gradient(s2);
    let e = 0;
    // recompute pair energy manually: (2r - sd)_+^2
    NEW.placeAll(s2);
    const sd = NEW.sdPair(s2, 0, 1), r = 1 * 0.35 * P.rho, o = 2 * r - sd;
    if (o > 0) e += o * o;
    return e;
  };
  const x0 = [st.X[0], st.Y[0], st.T[0], st.X[1], st.Y[1], st.T[1]];
  const h = 1e-6; let maxErr = 0;
  const analytic = [st.GX[0], st.GY[0], st.GT[0], st.GX[1], st.GY[1], st.GT[1]];
  // NOTE: st.GX includes wall terms too; use pieces far from walls so walls contribute ~0
  for (let k = 0; k < 6; k++) {
    const xp = x0.slice(), xm = x0.slice(); xp[k] += h; xm[k] -= h;
    const num = (E(xp) - E(xm)) / (2 * h);
    const err = Math.abs(num - analytic[k]) / (1 + Math.abs(analytic[k]));
    if (err > maxErr) maxErr = err;
  }
  ok(maxErr < 1e-4, `concave gradient finite-difference max rel err ${maxErr.toExponential(2)}`);
}

console.log(failures === 0 ? '\nALL CHECKS PASSED' : `\n${failures} FAILURES`);
process.exit(failures === 0 ? 0 : 1);
