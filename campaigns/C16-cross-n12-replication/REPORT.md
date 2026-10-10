# C16-cross-n12-replication: Fresh-seed replication of the cross n=12 win

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the predicted cross n=12 win replicate with fresh seeds?

**Hypothesis.** Cross-in-squ n=12's harden win (9.6112 vs 9.6589, predicted by scaffold fidelity 0.956) replicates with fresh seeds.

**Decision rule.** Best-of-16 at tolerance 1e-4 with FRESH seeds (101-116, never used). harden wins (h+1e-4 < r) -> the C13 headline prediction (first cross win, fidelity 0.956) replicates and is not a seed artifact. If harden does not win, the C13 cross result is noise and the 'predicted win' claim is withdrawn.

**Status.** closed — **decision:** does not replicate; prediction withdrawn

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **0 vs 1**, 0 ties (two-sided p = 1)

| instance | harden | rigid |
|---|---|--|
| cross-in-squ n=12 | 9.740784 (16 runs) | 9.557683 (16 runs) |
