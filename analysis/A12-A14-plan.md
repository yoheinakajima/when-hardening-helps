# A12/A13/A14 exploratory analyses (planned 2026-10-10, all on existing replays, no new runs)

Goal: a general predictive rule for when hardening wins. Three parallel analyses.

## A12 — scaffold-fidelity predictor (across instances)
Hypothesis: the morph preserves relative positions; hardening wins iff the disk
scaffold's relative arrangement already matches the optimum's.
- Per instance: D_scaffold = pairwise centroid-distance matrix at compress-end
  (last 'compress' frame) of harden's best run; D_opt = same matrix from the
  best-known final poses across ALL methods.
- Scaffold fidelity = Spearman rank correlation of upper-triangular entries
  (scale-invariant: scaffold is disks in a small container, optimum is polygons
  in a larger one).
- Test: one-sided — fidelity higher on the 9 harden-win instances than on the
  other ~40 (Mann-Whitney), and fidelity correlates with win margin
  (rigid_best − harden_best).

## A13 — basin narrowness / C12 (across instances)
Hypothesis: hardening wins where rigid's optimal basin is narrow.
- Per instance: cluster rigid's terminal packings by final L (1e-4); basin
  narrowness = 1 − (seeds reaching best L / total rigid seeds).
- Also: circular variance of rigid's terminal orientations vs harden's.
- Test: narrowness correlates with win margin (one-sided Spearman).

## A14 — within-method scaffold determination (across seeds, within instances)
Hypothesis: the scaffold decides the outcome seed-by-seed, not just on average.
- Per instance × harden seed: fidelity(seed) = Spearman(D_scaffold(seed), D_opt);
  correlate with that seed's final L.
- Test: negative correlation (higher fidelity → lower L) within instances,
  combined via Fisher's method. This controls for everything instance-level and
  tests "the scaffold decides" directly. No new runs; uses all harden seeds.
