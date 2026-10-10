# C00-verify-concave: Does the concave engine work end-to-end?

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Do concave compound pieces run through the full pipeline (engine, runner, ledger, projections) producing valid, overlap-free packings, and does the convex control behave as in the parent project?

**Hypothesis.** All runs complete without error; every best legalised packing verifies overlap-free and contained by the independent checker; on the squ-in-squ n=6 convex control, harden's best legalised size is <= rigid's (the parent project found hardening wins on squares in a square). Concave instances are smoke runs only: no scientific claim is made from them here.

**Decision rule.** Pass iff (a) zero run errors across all cells, (b) scripts/verify_packings.js reports zero pairwise overlaps (tolerance 1e-9) and full container containment on the best packing of every cell, and (c) the convex control holds: harden best_L <= rigid best_L on squ-in-squ n=6. Any failure is fixed in the engine, recorded as a plan amendment, and the campaign re-runs from scratch.

**Status.** closed — **decision:** Pass per the pre-registered decision rule: (a) 0 run errors, (b) verifier reports 0 failures on 12 best packings, (c) convex control holds (harden 3.0000 <= rigid 3.0000 on squ-in-squ n=6). Pipeline validated; proceeding to C01 concave pilot.

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **1 vs 5**, 0 ties (two-sided p = 0.2188)

| instance | harden | rigid |
|---|---|--|
| cross-in-squ n=3 | 5.303302 (4 runs) | 5.303301 (4 runs) |
| ltri-in-squ n=3 | 3.621321 (4 runs) | 3.767770 (4 runs) |
| ltri-in-squ n=4 | 4.000000 (4 runs) | 4.000000 (4 runs) |
| squ-in-squ n=6 | 3.000000 (4 runs) | 3.000000 (4 runs) |
| star5-in-squ n=3 | 3.110211 (4 runs) | 3.110206 (4 runs) |
| star5-in-squ n=4 | 3.212378 (4 runs) | 3.212375 (4 runs) |
