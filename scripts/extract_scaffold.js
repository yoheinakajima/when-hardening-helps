// Extract the compress-end scaffold for the C14 transplant test.
// Deterministic rule (pre-registered in the C14 plan): for the best replay of
// (campaign, family, n, method), take the LAST 'compress'-phase frame and emit 8
// runner configs {name, params: {init_from: {p, L, pad: 1.0}, seed}} with fresh seeds.
// The question: does the scaffold determine the morph's outcome?
// Usage: node scripts/extract_scaffold.js <campaign> <family> <n> <method> > scaffold.json
'use strict';
const fs = require('fs'), path = require('path');
const [campaign, family, n, method] = process.argv.slice(2);
const repFile = path.join('campaigns', campaign, 'replays', `${family}_n${n}_${method}_B1_default.json`);
const rep = JSON.parse(fs.readFileSync(repFile, 'utf8'));
const cand = rep.frames.filter(fr => fr.ph === 'compress');
if (!cand.length) throw new Error('no compress frame in ' + repFile);
const fr = cand[cand.length - 1];
const cfgs = [];
for (let k = 0; k < 8; k++) {
  cfgs.push({ name: 'scaf' + k, params: { init_from: { p: fr.p, L: fr.L, pad: 1.0 }, seed: 2000 + k } });
}
console.log(JSON.stringify(cfgs));
