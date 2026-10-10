# C02b-handoff-star5: Checkpoint handoff: star5 n=9

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does rigid search reach harden's star5 n=9 basin when started from a mid-morph checkpoint?

**Hypothesis.** On star5-in-squ n=9, where harden beat rigid by 0.10 in C01, rigid search started from harden's tau~0.5 checkpoint reaches harden's basin while rigid from random starts does not. Mechanism test, not efficiency test.

**Decision rule.** Handoff succeeds iff rigid-from-checkpoint best-of-16 <= (C02a harden best on star5 n=9) + 1e-3 AND rigid-from-random best-of-16 > (C02a harden best) + 0.01. Same interpretation as C02b-ltri.

**Status.** closed — **decision:** Handoff succeeds per the pre-registered rule. Basin delivery confirmed on star5 n=9.

## Head-to-head (best legalised container size per instance)


| instance | rigid |
|---|---|
| star5-in-squ n=9 | 4.654640 (1 runs) |
