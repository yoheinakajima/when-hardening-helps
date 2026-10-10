# C01-concave-pilot: Concave pilot: does hardening beat rigid starts on concave pieces?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** On three concave families at small n, does harden reach smaller containers than rigid starts at matched budget, and do the convex controls behave as in the parent project?

**Hypothesis.** Two-factor hypothesis: hardening beats rigid starts on concave families. (1) Path length: inscribed-disk share of piece area is ltri 6%, cross 31%, star5 41%, far below any convex piece (square 79%, triangle 61%, pentagon 86%), so the morph has far more room to work. (2) Hidden interlocking optima: concave optima require orientations a rigid search cannot easily reach. Positive control squ-in-squ (hardening wins in the parent project) should replicate; negative control tri-in-squ (tessellates) should tie or favour rigid.

**Decision rule.** Descriptive pilot; no confirmatory claim. Report per-family harden vs rigid exact two-sided sign tests (best legalised size per instance, relative tol 1e-9). Proceed to C02 (pre-registered flagship: 48 seeds, frozen settings, harden/rigid/sa/pc) if (i) harden wins >= rigid losses on concave families overall, and (ii) the positive control replicates qualitatively (harden >= rigid on squ-in-squ). If harden is systematically worse everywhere including the positive control, the method params do not transfer to this codebase state: run a concave tuning campaign before C02 and record it as an amendment here.

**Status.** closed — **decision:** Per the decision rule: (i) fails on strict counts (7 wins < 10 losses) and is a dead tie (5 vs 5) at noise-robust tolerance; (ii) positive control does not replicate at 16 seeds. Do NOT proceed to C02 flagship as designed. Next: targeted engine-replication check (squ-in-squ n=11, 32 seeds) plus a mechanism campaign (checkpoint-handoff on ltri n=5) to test whether the morph delivers the system into basins rigid search cannot reach - the instance-level story the pilot actually supports.

## Head-to-head (best legalised container size per instance)

- harden vs pc: **24 vs 1**, 0 ties (two-sided p = 1.55e-06)
- harden vs rigid: **7 vs 18**, 0 ties (two-sided p = 0.04329)
- harden vs sa: **19 vs 6**, 0 ties (two-sided p = 0.01463)

| instance | harden | pc | rigid | sa |
|---|---|--|--|--|
| cross-in-squ n=4 | 5.366564 (16 runs) | 5.390547 (16 runs) | 5.366564 (16 runs) | 5.367505 (16 runs) |
| cross-in-squ n=5 | 6.656856 (16 runs) | 6.874192 (16 runs) | 6.324557 (16 runs) | 6.335566 (16 runs) |
| cross-in-squ n=6 | 7.000004 (16 runs) | 7.089158 (16 runs) | 7.000002 (16 runs) | 7.044908 (16 runs) |
| cross-in-squ n=7 | 7.542474 (16 runs) | 7.659956 (16 runs) | 7.542473 (16 runs) | 7.613105 (16 runs) |
| cross-in-squ n=8 | 7.778179 (16 runs) | 8.188837 (16 runs) | 7.602634 (16 runs) | 7.716447 (16 runs) |
| ltri-in-squ n=5 | 4.000001 (16 runs) | 4.914326 (16 runs) | 4.610961 (16 runs) | 4.011695 (16 runs) |
| ltri-in-squ n=6 | 4.969032 (16 runs) | 5.169320 (16 runs) | 5.000001 (16 runs) | 4.981436 (16 runs) |
| ltri-in-squ n=7 | 5.267769 (16 runs) | 5.360269 (16 runs) | 5.000002 (16 runs) | 5.553591 (16 runs) |
| ltri-in-squ n=8 | 5.878353 (16 runs) | 5.969682 (16 runs) | 5.774855 (16 runs) | 5.225126 (16 runs) |
| ltri-in-squ n=9 | 6.000001 (16 runs) | 6.015380 (16 runs) | 6.000001 (16 runs) | 6.085403 (16 runs) |
| ltri-in-squ n=10 | 6.000001 (16 runs) | 6.674692 (16 runs) | 6.000002 (16 runs) | 6.297400 (16 runs) |
| squ-in-squ n=8 | 3.000001 (16 runs) | 3.019428 (16 runs) | 3.000000 (16 runs) | 3.001981 (16 runs) |
| squ-in-squ n=9 | 3.000001 (16 runs) | 3.046399 (16 runs) | 3.000000 (16 runs) | 3.005343 (16 runs) |
| squ-in-squ n=10 | 3.707108 (16 runs) | 3.776562 (16 runs) | 3.707107 (16 runs) | 3.741932 (16 runs) |
| squ-in-squ n=11 | 3.889408 (16 runs) | 4.041592 (16 runs) | 3.888267 (16 runs) | 3.922136 (16 runs) |
| squ-in-squ n=12 | 4.000001 (16 runs) | 4.054271 (16 runs) | 4.000000 (16 runs) | 4.011068 (16 runs) |
| star5-in-squ n=5 | 3.874576 (16 runs) | 3.988825 (16 runs) | 3.874561 (16 runs) | 3.946124 (16 runs) |
| star5-in-squ n=6 | 4.045087 (16 runs) | 4.196506 (16 runs) | 4.045086 (16 runs) | 4.096829 (16 runs) |
| star5-in-squ n=7 | 4.338713 (16 runs) | 4.486510 (16 runs) | 4.349762 (16 runs) | 4.357221 (16 runs) |
| star5-in-squ n=8 | 4.417264 (16 runs) | 4.841318 (16 runs) | 4.450073 (16 runs) | 4.406181 (16 runs) |
| star5-in-squ n=9 | 4.572950 (16 runs) | 5.180081 (16 runs) | 4.672613 (16 runs) | 4.659749 (16 runs) |
| star5-in-squ n=10 | 5.103489 (16 runs) | 5.198414 (16 runs) | 5.096753 (16 runs) | 5.112651 (16 runs) |
| tri-in-squ n=8 | 2.098077 (16 runs) | 2.178302 (16 runs) | 2.098077 (16 runs) | 2.098618 (16 runs) |
| tri-in-squ n=9 | 2.315726 (16 runs) | 2.310438 (16 runs) | 2.287510 (16 runs) | 2.295606 (16 runs) |
| tri-in-squ n=10 | 2.395733 (16 runs) | 2.435387 (16 runs) | 2.379720 (16 runs) | 2.384242 (16 runs) |
