# C03-morph-fraction: Morph-fraction ablation on ltri n=5

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** How much of the morph path is needed to reach the ltri n=5 pinwheel basin?

**Hypothesis.** harden-half (tau0=0.5) reaches the ltri n=5 pinwheel (L<=4.001) but harden-quarter (tau0=0.25) does not: the basin is found in the first half of the morph, consistent with the tau~0.5 checkpoint handoff.

**Decision rule.** Compare best-of-16 legalised sizes. If harden-half reaches <= 4.001 while harden-quarter does not (gap > 0.01), the basin is found in the first half of the morph. If both reach it, even a quarter-morph suffices and the critical interval is tau in [0, 0.25]. If neither reaches it, the full morph path is needed and the checkpoint result (tau~0.5) stands as the localization. Descriptive; feeds the mechanism story, no confirmatory claim.

**Status.** closed — **decision:** Both half and quarter morphs reach the pinwheel: critical interval is tau in [0,0.25].

## Head-to-head (best legalised container size per instance)


| instance | harden-half | harden-quarter | rigid |
|---|---|--|--|
| ltri-in-squ n=5 | 4.000000 (16 runs) | 4.000001 (16 runs) | 4.610961 (16 runs) |
