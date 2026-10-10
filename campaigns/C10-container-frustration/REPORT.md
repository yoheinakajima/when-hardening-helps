# C10-container-frustration: Container frustration: concave families in a triangle

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does container-piece geometric frustration create hardening advantage?

**Hypothesis.** Hardening helps where the container frustrates the piece's natural arrangement. Crosses tile square grids, so rigid search covers their orientation space in a square container (0/8 wins); a triangular container breaks the grid, creating non-obvious basins that only the morph discovers. New families ltri-in-tri, cross-in-tri, star5-in-tri (catalog added 2026-10-10); triangle container support already in engine.

**Decision rule.** Per instance, harden vs rigid best-of-16 at tolerance 1e-4. PRIMARY: on cross-in-tri, harden wins (h+1e-4 < r) on >=2/4 instances -> geometric frustration creates hardening advantage where the square container had none (cross was 0/8 in square). SECONDARY (descriptive): report ltri/star5 in triangle vs their square-container results; a uniform upward shift in harden wins supports the frustration story, a flat result bounds it.

**Status.** closed — **decision:** verdict recorded

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **5 vs 7**, 0 ties (two-sided p = 0.7744)

| instance | harden | rigid |
|---|---|--|
| cross-in-tri n=5 | 10.383663 (16 runs) | 10.383493 (16 runs) |
| cross-in-tri n=6 | 10.670730 (16 runs) | 10.670729 (16 runs) |
| cross-in-tri n=7 | 11.869225 (16 runs) | 11.738939 (16 runs) |
| cross-in-tri n=8 | 12.533935 (16 runs) | 12.529716 (16 runs) |
| ltri-in-tri n=5 | 7.386753 (16 runs) | 7.306768 (16 runs) |
| ltri-in-tri n=6 | 7.696154 (16 runs) | 7.732053 (16 runs) |
| ltri-in-tri n=7 | 8.154704 (16 runs) | 8.400633 (16 runs) |
| ltri-in-tri n=8 | 8.741164 (16 runs) | 8.990949 (16 runs) |
| star5-in-tri n=5 | 5.841364 (16 runs) | 5.841352 (16 runs) |
| star5-in-tri n=6 | 5.997446 (16 runs) | 5.997413 (16 runs) |
| star5-in-tri n=7 | 6.766501 (16 runs) | 6.766504 (16 runs) |
| star5-in-tri n=8 | 7.124285 (16 runs) | 7.125150 (16 runs) |
