# C09-seed-scale: Seed scaling: discovery curves on signature instances

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does hardening's advantage grow with seed budget (rare-basin discovery)?

**Hypothesis.** Hardening's advantage is a rare-basin discovery effect: rigid's best plateaus early (it cannot find the basin at any budget) while harden keeps discovering better basins as seeds grow. Motivated by the squ n=11 duplicate: 16 seeds missed the signature (Y=0), 32 seeds found it (Y=1).

**Decision rule.** For k in {8,16,32}, best-of-first-k-seeds per method (paired seeds); gap(k) = rigid_best(k) - harden_best(k) at tolerance 1e-4. PRIMARY: gap(32) > gap(8) + 1e-4 on >=5/6 instances -> one-sided sign test, alpha 0.05 -> hardening's advantage widens with seed budget (rare-basin discovery). If gap is flat, the advantage is a fixed offset, not a discovery effect. Report full discovery curves (best vs seeds) per instance and method.

**Status.** closed — **decision:** verdict recorded

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **5 vs 1**, 0 ties (two-sided p = 0.2188)

| instance | harden | rigid |
|---|---|--|
| ltri-in-squ n=5 | 4.000001 (32 runs) | 4.610961 (32 runs) |
| ltri-in-squ n=11 | 6.576908 (32 runs) | 6.610989 (32 runs) |
| squ-in-squ n=11 | 3.877087 (32 runs) | 3.888267 (32 runs) |
| star5-in-squ n=7 | 4.309062 (32 runs) | 4.309020 (32 runs) |
| star5-in-squ n=9 | 4.572950 (32 runs) | 4.672613 (32 runs) |
| tri-in-squ n=11 | 2.490961 (32 runs) | 2.500019 (32 runs) |
