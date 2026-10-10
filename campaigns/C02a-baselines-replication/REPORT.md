# C02a-baselines-replication: Engine replication (squ n=11, 32 seeds) + handoff baselines

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the generalized engine reproduce the parent's squ-in-squ n=11 signature, and what are fresh harden baselines on the handoff instances?

**Hypothesis.** The generalized engine reproduces the parent project's signature result: with 32 runs at budget 1, harden reaches Trump's n=11 record (3.87708359) while rigid does not. (C01's 16-seed control could not test this: the tilted basin is a rare event.) Fresh harden baselines on ltri n=5 and star5 n=9 supply checkpoints for the handoff test.

**Decision rule.** Replication passes iff harden best-of-32 <= 3.87709 (Trump's record 3.87708359 + 1e-5) AND harden best < rigid best - 1e-3 on squ-in-squ n=11. If replication fails, halt: do not interpret any handoff results until the engine difference is found. If it passes, the ltri n=5 and star5 n=9 harden runs supply the checkpoints for C02b-ltri and C02b-star5.

**Status.** closed — **decision:** Replication passes per the pre-registered rule (harden 3.87708674 <= 3.87709 and < rigid - 1e-3). Engine validated; C02b handoff launches with checkpoints extracted from these harden replays.

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **3 vs 0**, 0 ties (two-sided p = 0.25)

| instance | harden | rigid |
|---|---|--|
| ltri-in-squ n=5 | 4.000001 (16 runs) | 4.610961 (16 runs) |
| squ-in-squ n=11 | 3.877087 (32 runs) | 3.888267 (32 runs) |
| star5-in-squ n=9 | 4.572950 (16 runs) | 4.672613 (16 runs) |
