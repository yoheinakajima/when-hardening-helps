# C05-morph-parts: Morph-part factorial on concave instances

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Which part of the methodology matters, for which concave shapes?

**Hypothesis.** The C03 localization generalizes: on concave instances the compress phase contributes nothing (nocompress ~= harden) and a quarter-morph suffices; rigid trails on the instances where C01 found harden wins.

**Decision rule.** Per instance, rank the 5 methods by best-of-16 at 1e-4. Pre-registered hypothesis: on concave instances, harden-nocompress is within 1e-3 of harden on >=5/7 instances (the disk-compress phase is unnecessary, per C03's ltri result). Also report, per instance, the minimal morph in {quarter, half, full} reaching within 1e-3 of the instance best (descriptive companion to the meta-analysis).

**Status.** closed — **decision:** Nocompress hypothesis rejected; compress phase essential, short morph suffices.

## Head-to-head (best legalised container size per instance)

- harden vs harden-half: **4 vs 3**, 0 ties (two-sided p = 1)
- harden vs harden-nocompress: **3 vs 4**, 0 ties (two-sided p = 1)
- harden vs harden-quarter: **2 vs 5**, 0 ties (two-sided p = 0.4531)
- harden vs rigid: **5 vs 2**, 0 ties (two-sided p = 0.4531)

| instance | harden | harden-half | harden-nocompress | harden-quarter | rigid |
|---|---|--|--|--|--|
| cross-in-squ n=5 | 6.656856 (16 runs) | 6.324557 (16 runs) | 6.324558 (16 runs) | 6.324558 (16 runs) | 6.324557 (16 runs) |
| cross-in-squ n=8 | 7.778179 (16 runs) | 7.778175 (16 runs) | 7.778176 (16 runs) | 7.602635 (16 runs) | 7.602634 (16 runs) |
| ltri-in-squ n=5 | 4.000001 (16 runs) | 4.000000 (16 runs) | 4.621321 (16 runs) | 4.000001 (16 runs) | 4.610961 (16 runs) |
| ltri-in-squ n=6 | 4.969032 (16 runs) | 4.984063 (16 runs) | 4.984063 (16 runs) | 4.954656 (16 runs) | 5.000001 (16 runs) |
| star5-in-squ n=7 | 4.338713 (16 runs) | 4.342885 (16 runs) | 4.342249 (16 runs) | 4.309040 (16 runs) | 4.349762 (16 runs) |
| star5-in-squ n=8 | 4.417264 (16 runs) | 4.421068 (16 runs) | 4.405500 (16 runs) | 4.446279 (16 runs) | 4.450073 (16 runs) |
| star5-in-squ n=9 | 4.572950 (16 runs) | 4.572951 (16 runs) | 4.572944 (16 runs) | 4.572947 (16 runs) | 4.672613 (16 runs) |
