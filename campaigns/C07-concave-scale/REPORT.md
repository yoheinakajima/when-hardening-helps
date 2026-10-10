# C07-concave-scale: Concave n-scaling

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the hardening advantage grow with n?

**Hypothesis.** The harden advantage grows with piece count within concave families (more pieces -> more interlocking -> more steric barriers for rigid search).

**Decision rule.** Per family, Cochran-Armitage-style trend: pre-registered one-sided test of whether P(harden beats rigid at 1e-4) increases with n across the pooled instances (C01 n=5..8 + C02a + C07 n=9..11 for that family). Report per-instance bests and gaps regardless.

**Status.** closed — **decision:** No monotonic trend; family-dependent.

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **4 vs 4**, 0 ties (two-sided p = 1)

| instance | harden | rigid |
|---|---|--|
| cross-in-squ n=9 | 7.602634 (16 runs) | 7.602633 (16 runs) |
| cross-in-squ n=10 | 8.837508 (16 runs) | 8.708916 (16 runs) |
| cross-in-squ n=11 | 9.327933 (16 runs) | 9.192393 (16 runs) |
| ltri-in-squ n=9 | 6.000001 (16 runs) | 6.000001 (16 runs) |
| ltri-in-squ n=10 | 6.000001 (16 runs) | 6.000002 (16 runs) |
| ltri-in-squ n=11 | 6.576908 (16 runs) | 7.000002 (16 runs) |
| star5-in-squ n=10 | 5.103489 (16 runs) | 5.096753 (16 runs) |
| star5-in-squ n=11 | 5.251785 (16 runs) | 5.262914 (16 runs) |
