# C08-phase-decomp: Phase decomposition: compress vs morph

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Which phase of hardening does the work — the soft disk-compress, or the gradual morph?

**Hypothesis.** The C05 correction generalizes: what matters is the soft disk-compress phase (pieces slide past each other without corners catching), not the gradual morph. snap (compress as disks, then instant rigid polygons + settle, same total evals) should match harden; the morph is just the finish.

**Decision rule.** Per instance, rank {harden, harden-quarter, snap, rigid} by best-of-16 at tolerance 1e-4. PRIMARY: snap within 1e-3 of harden on >=4/6 instances -> the gradual morph is unnecessary; the disk-compress phase does the work (basin delivery = soft compress). ALTERNATIVE: harden beats snap by >1e-3 on >=4/6 instances -> the gradual morph path is essential. SECONDARY (replication): harden-quarter within 1e-3 of harden on >=4/6 (extends C05's quarter finding to the signature instances). All comparisons use paired seeds.

**Status.** closed — **decision:** verdict recorded

## Head-to-head (best legalised container size per instance)

- harden vs harden-quarter: **1 vs 5**, 0 ties (two-sided p = 0.2188)
- harden vs rigid: **5 vs 1**, 0 ties (two-sided p = 0.2188)
- harden vs snap: **5 vs 1**, 0 ties (two-sided p = 0.2188)

| instance | harden | harden-quarter | rigid | snap |
|---|---|--|--|--|
| ltri-in-squ n=5 | 4.000001 (16 runs) | 4.000001 (16 runs) | 4.610961 (16 runs) | 11.567258 (16 runs) |
| ltri-in-squ n=11 | 6.576908 (16 runs) | 6.527760 (16 runs) | 7.000002 (16 runs) | 22.108573 (16 runs) |
| squ-in-squ n=11 | 3.889408 (16 runs) | 3.886748 (16 runs) | 3.888267 (16 runs) | 3.889427 (16 runs) |
| star5-in-squ n=7 | 4.338713 (16 runs) | 4.309040 (16 runs) | 4.349762 (16 runs) | 4.342234 (16 runs) |
| star5-in-squ n=9 | 4.572950 (16 runs) | 4.572947 (16 runs) | 4.672613 (16 runs) | 4.572964 (16 runs) |
| tri-in-squ n=11 | 2.503693 (16 runs) | 2.490961 (16 runs) | 2.504794 (16 runs) | 2.490961 (16 runs) |
