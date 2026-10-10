# C14-scaffold-transplant: Scaffold transplant: causal test on cross n=5

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the scaffold cause the morph's outcome (causal proof)?

**Hypothesis.** The disk scaffold causes the morph's outcome. Transplanting cross n=5's good scaffold (from harden-quarter, L=5.83) under a full morph rescues it to 6.3246, while transplanting the trap scaffold (from harden-full disks, L=3.29) keeps it trapped at 6.6569 - with identical morph dynamics. This is the causal intervention that turns the A12 correlation into a mechanism.

**Decision rule.** Best-of-8 per scaffold arm at tolerance 1e-4. CAUSAL CLAIM: good-scaffold arm reaches <= 6.3246+1e-3 (the known-good basin) AND bad-scaffold arm reaches >= 6.6569-1e-3 (stays trapped) with IDENTICAL morph dynamics (same method, same seeds structure, only init_from differs) -> the scaffold CAUSES the outcome; the morph is a local refiner that inherits its starting basin. If good-scaffold fails to reach 6.33, the scaffold alone is insufficient (morph dynamics or compress history matter). If bad-scaffold escapes to 6.32, the trap is not scaffold-determined. Random-init control already established by C11 (harden-full -> 6.6569).

**Status.** closed — **decision:** inconclusive: tau-path mismatch; superseded by C15

## Head-to-head (best legalised container size per instance)


| instance | harden-morphonly |
|---|---|
| cross-in-squ n=5 | 6.734792 (1 runs) |
