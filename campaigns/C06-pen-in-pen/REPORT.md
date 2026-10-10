# C06-pen-in-pen: Pentagons in a pentagon

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the hardening effect survive a change of container shape?

**Hypothesis.** Two-sided scoping: container shape interacts with the hardening effect. If pen-in-pen shows harden wins where pen-in-squ did not (C15: 1 vs 8), the container - not just the piece - belongs in the predictor set.

**Decision rule.** Instance-level reporting (best-of-16 harden vs rigid at 1e-4); sign test across the 4 instances is descriptive only (n=4 is underpowered by design - this is a scoping campaign for the container axis). No external records exist for pen-in-pen; all comparisons are relative.

**Status.** closed — **decision:** All ties; no hardening advantage for pentagons in pentagons.

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **0 vs 3**, 1 ties (two-sided p = 0.25)

| instance | harden | rigid |
|---|---|--|
| pen-in-pen n=5 | 2.618034 (16 runs) | 2.618034 (16 runs) |
| pen-in-pen n=6 | 2.618034 (16 runs) | 2.618034 (16 runs) |
| pen-in-pen n=7 | 3.078690 (16 runs) | 3.078690 (16 runs) |
| pen-in-pen n=8 | 3.335175 (16 runs) | 3.335175 (16 runs) |
