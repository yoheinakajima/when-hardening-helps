# C04-convex-rare: Convex rare-event sweep at n=11

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the n=11 hardening signature generalize across convex shapes?

**Hypothesis.** The n=11 rare-event signature (harden reaches the record, rigid does not) is square-specific: present for squ-in-squ, absent for tri/pen/hex. Null (all four show it) is equally reportable.

**Decision rule.** Per family: 'signature present' iff harden best-of-32 <= record + 1e-3 AND rigid best-of-32 > record + 1e-3 (record from catalog; pen/hex records as listed). Report exact bests regardless. This is the generalization test of the parent's n=11 finding.

**Status.** closed — **decision:** Signature present for squ and tri; pen ties; hex favors rigid. Square-specific hypothesis rejected.

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **2 vs 2**, 0 ties (two-sided p = 1)

| instance | harden | rigid |
|---|---|--|
| hex-in-squ n=11 | 6.339748 (32 runs) | 6.332907 (32 runs) |
| pen-in-squ n=11 | 5.115946 (32 runs) | 5.115562 (32 runs) |
| squ-in-squ n=11 | 3.877087 (32 runs) | 3.888267 (32 runs) |
| tri-in-squ n=11 | 2.490961 (32 runs) | 2.500019 (32 runs) |
