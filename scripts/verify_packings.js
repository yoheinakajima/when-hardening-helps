// Independent packing verifier for C00: for the best run of every cell in a campaign,
// checks (a) no pairwise overlap: rigidSd >= -1e-9 for all pairs, (b) every vertex inside
// the container. rigidSd itself was verified against brute-force segment intersection in
// scripts/verify_engine.js, which is the independence chain for this check.
// Usage: node scripts/verify_packings.js campaigns/<C>
'use strict';
const fs = require('fs'), path = require('path');
const E = require('../engine/engine2d.js');
const dir = process.argv[2];
if (!dir) { console.error('usage: node scripts/verify_packings.js campaigns/<C>'); process.exit(2); }
const root = path.join(dir, '..', '..');

let best = {}; // cell -> row
for (const f of fs.readdirSync(dir)) {
  if (!/^runs.*\.jsonl$/.test(f)) continue;
  for (const line of fs.readFileSync(path.join(dir, f), 'utf8').split('\n')) {
    if (!line.trim()) continue;
    const r = JSON.parse(line);
    if (r.error) { console.error('RUN ERROR:', r.id, r.error.slice(0, 200)); process.exit(1); }
    const k = [r.family, r.n, r.method, r.budget, r.config].join('/');
    if (!best[k] || r.L < best[k].L) best[k] = r;
  }
}
let fails = 0, checked = 0;
for (const k of Object.keys(best).sort()) {
  const r = best[k];
  const F = JSON.parse(fs.readFileSync(path.join(root, 'catalog', r.family + '.json'), 'utf8'));
  const P = E.makePiece(E.PIECES[F.piece] !== undefined ? E.PIECES[F.piece] : F.piece);
  const C = E.makeContainer(F.container);
  const poses = r.poses;
  // (a) pairwise overlaps
  for (let i = 0; i < poses.length; i++) for (let j = i + 1; j < poses.length; j++) {
    const sd = E.rigidSd(P, poses[i], poses[j]);
    if (sd < -1e-9) { fails++; console.error(`FAIL overlap ${k}: pair (${i},${j}) sd=${sd}`); }
  }
  // (b) containment: every world vertex (or centre + radius, for circles) inside the container
  const pad = P.k === 0 ? 0.5 : 0;
  const verts = [];
  if (P.k === 0) for (const p of poses) verts.push([p[0], p[1]]);
  else for (const p of poses) verts.push(...E.worldVerts(P, p[0], p[1], p[2]));
  let bad = 0;
  for (const [x, y] of verts) {
    if (C.circle) { if (Math.hypot(x, y) + pad > r.L + 1e-9) bad++; }
    else for (let w = 0; w < C.beta.length; w++)
      if (C.normals[2 * w] * x + C.normals[2 * w + 1] * y + pad > C.beta[w] * r.L + 1e-9) { bad++; break; }
  }
  if (bad) { fails++; console.error(`FAIL containment ${k}: ${bad} vertices outside`); }
  checked++;
}
console.log(`verified ${checked} best packings, ${fails} failures`);
process.exit(fails ? 1 : 0);
