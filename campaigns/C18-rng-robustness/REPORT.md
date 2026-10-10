# C18-rng-robustness: RNG robustness on key cells

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Are the key findings robust to RNG stream?

**Hypothesis.** The key findings are not RNG artifacts: cross n=12 win, ltri n=5 snap-catastrophe, and the cross n=5 tau-sweep ordering all replicate under a shifted seed stream (201-216).

**Decision rule.** Per instance, compare the qualitative verdict (win/tie/loss at 1e-4) between original seeds and shifted seeds (201-216). ROBUST iff >=4/5 instances keep the same verdict AND the C11 tau-sweep ordering (quarter<=tau05<=tau075<full on n=5) is preserved. If verdicts flip, the findings are RNG-sensitive and the paper must report seed-dependence.

**Status.** closed — **decision:** 2/3 robust; trap is probabilistic

## Head-to-head (best legalised container size per instance)

- harden vs harden-quarter: **1 vs 2**, 0 ties (two-sided p = 1)
- harden vs rigid: **1 vs 2**, 0 ties (two-sided p = 1)
- harden vs snap: **2 vs 1**, 0 ties (two-sided p = 1)

| instance | harden | harden-quarter | rigid | snap |
|---|---|--|--|--|
| cross-in-squ n=5 | 6.324558 (16 runs) | 6.324557 (16 runs) | 6.324557 (16 runs) | 6.324559 (16 runs) |
| cross-in-squ n=12 | 9.714507 (16 runs) | 9.616107 (16 runs) | 9.543965 (16 runs) | 9.249164 (16 runs) |
| ltri-in-squ n=5 | 4.000001 (16 runs) | 4.000001 (16 runs) | 4.610971 (16 runs) | 12.161633 (16 runs) |
