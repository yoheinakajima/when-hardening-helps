// Extract a mid-morph checkpoint for the C02 handoff test.
// Deterministic rule (pre-registered in the C02b plan): for the best harden replay of
// (family, n), take the 'morph'-phase frame whose tau is closest to 0.5 and emit 16
// runner configs {name, params: {init_from: {p, L, pad: 1.02}, seed}} with fresh seeds.
// The question: is the basin of harden's best packing reachable by rigid search from
// that neighborhood? (Per-seed pairing was considered and rejected: the best-run
// checkpoint is the pre-registered choice.)
// Usage: node scripts/extract_checkpoints.js <campaign> <family> <n> > checkpoints.json
'use strict';
const fs = require('fs'), path = require('path');
const [campaign, family, n] = process.argv.slice(2);
const repFile = path.join('campaigns', campaign, 'replays', `${family}_n${n}_harden_B1_default.json`);
const rep = JSON.parse(fs.readFileSync(repFile, 'utf8'));
const cand = rep.frames.filter(fr => fr.ph === 'morph');
cand.sort((a, b) => Math.abs(a.u - 0.5) - Math.abs(b.u - 0.5));
const fr = cand[0];
if (!fr) throw new Error('no morph frame in ' + repFile);
const cfgs = [];
for (let k = 0; k < 16; k++) {
  cfgs.push({ name: 'ckpt' + k, params: { init_from: { p: fr.p, L: fr.L, pad: 1.02 }, seed: 1000 + k } });
}
console.log(JSON.stringify(cfgs));
