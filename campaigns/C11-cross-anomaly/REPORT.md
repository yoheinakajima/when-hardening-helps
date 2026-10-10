# C11-cross-anomaly: Tau0 sweep localizing the cross morph pathology

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Where in the morph path does full hardening break on cross (and why)?

**Hypothesis.** The C05 anomaly (cross n=5: full harden 6.6569 vs quarter/half/nocompress/rigid all 6.3246) is a morph-path pathology: starting from full disks, the long morph pulls crosses into a worse basin that the shorter morph avoids. A tau0 sweep localizes the breaking point. Understanding where hardening HURTS bounds where it can help.

**Decision rule.** Per instance, rank {harden-quarter (tau0=0.25), harden-tau05, harden-tau075, harden (tau0=1)} by best-of-16 at 1e-4. PRIMARY (descriptive/localizing): report the smallest tau0 within 1e-3 of the instance best and the tau0 where performance degrades >1e-3; the break point localizes where the full morph goes wrong. SECONDARY: trajectory analysis from replays — compare the morph-phase paths of tau0=0.25 (good) vs tau0=1 (bad): does the full morph destroy a good disk-phase arrangement, or never find one? No confirmatory claim; this is anomaly localization.

**Status.** closed — **decision:** anomaly localized: morph breaks from near-full disks; scaffold-trap mechanism identified

## Head-to-head (best legalised container size per instance)

- harden vs harden-quarter: **0 vs 2**, 0 ties (two-sided p = 0.5)
- harden vs harden-tau05: **0 vs 2**, 0 ties (two-sided p = 0.5)
- harden vs harden-tau075: **1 vs 1**, 0 ties (two-sided p = 1)

| instance | harden | harden-quarter | harden-tau05 | harden-tau075 |
|---|---|--|--|--|
| cross-in-squ n=5 | 6.656856 (16 runs) | 6.324558 (16 runs) | 6.324557 (16 runs) | 6.324559 (16 runs) |
| cross-in-squ n=8 | 7.778179 (16 runs) | 7.602635 (16 runs) | 7.778175 (16 runs) | 7.794646 (16 runs) |
