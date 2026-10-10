# Meta-analysis plan (pre-registered 2026-10-09, before C04–C07 run)

Goal: predict which shapes/scenarios benefit from hardening, with statistical rigor.

## Unit and outcome
- Unit: one instance = (family, n) from the inclusion set below.
- Outcome Y = 1 if harden best-of beats rigid best-of at noise-robust tolerance 1e-4
  (harden_best + 1e-4 < rigid_best), else 0. Ties (within 1e-4) count as 0.
- "Best-of" uses the campaign's full seed budget for that instance.

## Inclusion set (fixed now; no peeking at C04–C07 when fitting)
- C01 concave pilot: ltri, cross, star5 × n=5..8; squ, tri controls × n=5..8
- C02a: ltri n=5, star5 n=9, squ n=11
- C04: squ, tri, pen, hex × n=11
- C06: pen-in-pen × n=5..8
- C07: ltri, cross, star5 × n=9..11
- Excluded: C02b (handoff, not harden-vs-rigid), C03/C05 (ablation methods),
  C00 (verification only). Rationale: the outcome is defined on harden-vs-rigid only.

## Covariates (fixed now; computed from pieces.json + catalog, never from outcomes)
1. concave: 1 if the piece has any reflex vertex, else 0
2. n_reflex: number of reflex (concave) vertices of the piece
3. disk_share: inscribed-disk area / piece area (from pieces.json)
4. symmetry: rotational symmetry order of the piece
5. n_pieces: n
6. container_sides: number of container walls (4 = square, 5 = pentagon, 3 = triangle)
7. Family random intercept (piece identity beyond the measured descriptors)

## Models (in this order; all reported even if null)
1. Mixed-effects logistic regression: Y ~ concave + n_reflex + disk_share + symmetry
   + n_pieces + container_sides + (1 | family). Report odds ratios with 95% CIs.
2. Pre-registered directional hypotheses (one-sided sign tests, alpha 0.05):
   - H1: concave instances have higher P(Y=1) than convex instances.
   - H2: within concave families, P(Y=1) increases with n_pieces (Cochran–Armitage trend).
   - H3: P(Y=1) decreases with disk_share (more disk-like pieces benefit less).
3. Ablation companion (descriptive, from C05): for each concave instance, which of
   {full, half, quarter, nocompress} reaches within 1e-3 of the best; report the
   minimal sufficient morph per instance. No confirmatory claim.

## Rigor notes
- Descriptors and inclusion set were frozen before C04–C07 ran (this file, git).
- Primary tolerance is 1e-4 (noise-robust; lesson of C01).
- Seeds are shared across methods within each campaign → paired comparisons.
- Every campaign is ingested whatever the outcome; null results are findings.
- This is observational across instances (not randomized over shapes); language will
  say "predicts/associated", never "causes", outside the mechanism experiments.
