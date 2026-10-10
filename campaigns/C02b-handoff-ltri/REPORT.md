# C02b-handoff-ltri: Checkpoint handoff: ltri n=5

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does rigid search reach harden's ltri n=5 pinwheel basin when started from a mid-morph checkpoint?

**Hypothesis.** On ltri-in-squ n=5, where harden beat rigid by 0.61 in C01, rigid search started from harden's tau~0.5 checkpoint reaches harden's basin (L≈4.0) while rigid from random starts does not. This is a mechanism test, not an efficiency test: the checkpoint cost a harden run, which is beside the point - the question is WHERE the search goes.

**Decision rule.** Handoff succeeds iff rigid-from-checkpoint best-of-16 <= (C02a harden best on ltri n=5) + 1e-3 AND rigid-from-random best-of-16 > (C02a harden best) + 0.01. Success means the morph's contribution on this instance is basin delivery: rigid search reaches the pinwheel once started in its neighborhood but not from random starts. Failure (checkpoint cannot reach it either) means the late morph does essential work beyond basin delivery, or the checkpoint choice (tau~0.5) was wrong - either way the mechanism is not basin delivery alone.

**Status.** closed — **decision:** Handoff succeeds per the pre-registered rule. Basin delivery confirmed on ltri n=5.

## Head-to-head (best legalised container size per instance)


| instance | rigid |
|---|---|
| ltri-in-squ n=5 | 4.000000 (1 runs) |
