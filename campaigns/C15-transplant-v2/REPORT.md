# C15-transplant-v2: Scaffold transplant v2: matched tau paths

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the scaffold cause the morph's outcome (corrected causal test)?

**Hypothesis.** The scaffold causes the morph's outcome. With the tau path corrected (C14's flaw), transplanting cross n=5's good scaffold under its native quarter morph rescues it to 6.3246, while the trap scaffold under its native full morph stays trapped at 6.6569.

**Decision rule.** Best-of-8 per arm at tolerance 1e-4. CAUSAL CLAIM: good arm (quarter morph from good scaffold) reaches <= 6.3246+1e-3 AND bad arm (full morph from trap scaffold) reaches >= 6.6569-1e-3 -> the scaffold causes the outcome; the morph inherits its starting basin and the compress phase's job is fully captured by the scaffold it produces. If good arm fails, the compress DYNAMICS (not just its endpoint) matter. If bad arm escapes, the trap is not scaffold-determined. C14 is retained as a documented pilot: its good arm used the wrong tau path (full morph from a quarter scaffold), so its inconclusive result does not bear on this test.

**Status.** closed — **decision:** mixed: good scaffold sufficient (8/8), trap not scaffold-determined

## Head-to-head (best legalised container size per instance)


| instance | harden-morphonly | harden-quarter-morphonly |
|---|---|--|
| cross-in-squ n=5 | 6.734792 (1 runs) | 6.324560 (1 runs) |
