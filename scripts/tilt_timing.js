// Tilt-timing (post-hoc analysis, no new runs): for each morph-phase frame of the best
// harden replay, legalize the frame's poses AS RIGID PIECES. The tau at which the
// rigid-legalized size collapses to the final packing size is when the basin is found.
// Usage: node scripts/tilt_timing.js <replay.json>
'use strict';
const fs = require('fs');
const E = require('../engine/engine2d.js');
const rep = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const P = E.makePiece(E.PIECES[rep.piece]), C = E.makeContainer(rep.container);
const rows = [];
for (const fr of rep.frames) {
  if (fr.ph !== 'compress' && fr.ph !== 'morph') continue;
  const n = rep.n, X = new Float64Array(n), Y = new Float64Array(n), T = new Float64Array(n);
  for (let i = 0; i < n; i++) { X[i] = fr.p[3 * i]; Y[i] = fr.p[3 * i + 1]; T[i] = fr.p[3 * i + 2]; }
  const leg = E.legalize(P, C, X, Y, T);
  rows.push({ tau: fr.u, Lrigid: leg.L, Lsoft: fr.L });
}
console.log('tau\tL_rigid\tL_soft');
for (const r of rows) console.log(r.tau.toFixed(3) + '\t' + r.Lrigid.toFixed(4) + '\t' + r.Lsoft.toFixed(4));
const finalL = rows[rows.length - 1].Lrigid;
const hit = rows.find(r => r.Lrigid <= finalL + 1e-3);
console.log(`\nbasin found at tau=${hit.tau.toFixed(3)} (rigid-legalized L=${hit.Lrigid.toFixed(4)}, final=${finalL.toFixed(4)})`);
