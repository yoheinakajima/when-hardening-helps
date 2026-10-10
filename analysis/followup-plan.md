# Follow-up campaign slate (designed 2026-10-10)

Goal: maximize understanding of **what part** of hardening works, **when**, and **why**.
Four parallel run-campaigns + one analysis track. All preregistered below before launch.

## What part works
**C08-phase-decomp** — harden vs harden-quarter vs snap vs rigid on 6 signature
instances (ltri 5,11; star5 7,9; squ 11; tri 11), 16 seeds = 384 runs.
`snap` = disk compression, then rigid polygons at once (engine already supports it).
If snap ≈ harden, the gradual morph is unnecessary and the soft compress does the
work. If harden > snap, the morph path is essential.

## When
**C09-seed-scale** — harden vs rigid × 32 seeds on the same 6 instances = 384 runs.
Discovery curves: gap(k) = rigid_best(k) − harden_best(k) for k ∈ {8,16,32}.
Tests whether the advantage widens with budget (rare-basin discovery), motivated by
the squ n=11 duplicate (16 seeds missed it, 32 found it).

**C10-container-frustration** — ltri/cross/star5 × n=5..8 × {harden, rigid} × 16
seeds in a TRIANGLE container (new catalog families, engine already supports it)
= 384 runs. Tests whether geometric frustration creates harden wins where the
square had none — especially cross, 0/8 in square.

## Why (failure mode)
**C11-cross-anomaly** — tau0 sweep {0.25, 0.5, 0.75, 1.0} on cross n=5,8 × 16
seeds = 128 runs, plus replay trajectory analysis. Localizes where the full morph
breaks (C05: 6.6569 vs 6.3246 for everything else). Understanding where hardening
HURTS bounds where it can help.

## Why (mechanism) — analysis track
**C12-basin-structure** (no new runs initially): using existing replays,
1. cluster rigid's terminal packings per instance → count distinct basins, measure
   the best basin's discovery probability ("basin narrowness");
2. correlate basin narrowness with harden's win margin across the 37 meta instances;
3. orientation analysis: circular variance of terminal orientations (rigid vs harden),
   angular distance of rigid's modal orientations to the best-known optimum.
If basin narrowness predicts the win margin, it becomes the operationalization of
"when" — and a candidate for the paper's core claim.

Total new runs: 384 + 384 + 384 + 128 = 1280, all parallelizable.
