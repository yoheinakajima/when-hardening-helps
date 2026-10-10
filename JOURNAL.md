# Research journal

Every entry below is generated from the ledger. Findings link to the cells that support them.

## C00-verify-concave: Does the concave engine work end-to-end?
Status: closed — Pass per the pre-registered decision rule: (a) 0 run errors, (b) verifier reports 0 failures on 12 best packings, (c) convex control holds (harden 3.0000 <= rigid 3.0000 on squ-in-squ n=6). Pipeline validated; proceeding to C01 concave pilot.
- harden vs rigid: 1 vs 5, 0 ties (p = 0.2188)

## C01-concave-pilot: Concave pilot: does hardening beat rigid starts on concave pieces?
Status: closed — Per the decision rule: (i) fails on strict counts (7 wins < 10 losses) and is a dead tie (5 vs 5) at noise-robust tolerance; (ii) positive control does not replicate at 16 seeds. Do NOT proceed to C02 flagship as designed. Next: targeted engine-replication check (squ-in-squ n=11, 32 seeds) plus a mechanism campaign (checkpoint-handoff on ltri n=5) to test whether the morph delivers the system into basins rigid search cannot reach - the instance-level story the pilot actually supports.
- harden vs pc: 24 vs 1, 0 ties (p = 1.55e-06)
- harden vs rigid: 7 vs 18, 0 ties (p = 0.04329)
- harden vs sa: 19 vs 6, 0 ties (p = 0.01463)

## C02a-baselines-replication: Engine replication (squ n=11, 32 seeds) + handoff baselines
Status: closed — Replication passes per the pre-registered rule (harden 3.87708674 <= 3.87709 and < rigid - 1e-3). Engine validated; C02b handoff launches with checkpoints extracted from these harden replays.
- harden vs rigid: 3 vs 0, 0 ties (p = 0.25)

## C02b-handoff-ltri: Checkpoint handoff: ltri n=5
Status: closed — Handoff succeeds per the pre-registered rule. Basin delivery confirmed on ltri n=5.

## C02b-handoff-star5: Checkpoint handoff: star5 n=9
Status: closed — Handoff succeeds per the pre-registered rule. Basin delivery confirmed on star5 n=9.

## C03-morph-fraction: Morph-fraction ablation on ltri n=5
Status: closed — Both half and quarter morphs reach the pinwheel: critical interval is tau in [0,0.25].

## C04-convex-rare: Convex rare-event sweep at n=11
Status: closed — Signature present for squ and tri; pen ties; hex favors rigid. Square-specific hypothesis rejected.
- harden vs rigid: 2 vs 2, 0 ties (p = 1)

## C05-morph-parts: Morph-part factorial on concave instances
Status: closed — Nocompress hypothesis rejected; compress phase essential, short morph suffices.
- harden vs harden-half: 4 vs 3, 0 ties (p = 1)
- harden vs harden-nocompress: 3 vs 4, 0 ties (p = 1)
- harden vs harden-quarter: 2 vs 5, 0 ties (p = 0.4531)
- harden vs rigid: 5 vs 2, 0 ties (p = 0.4531)

## C06-pen-in-pen: Pentagons in a pentagon
Status: closed — All ties; no hardening advantage for pentagons in pentagons.
- harden vs rigid: 0 vs 3, 1 ties (p = 0.25)

## C07-concave-scale: Concave n-scaling
Status: closed — No monotonic trend; family-dependent.
- harden vs rigid: 4 vs 4, 0 ties (p = 1)

## C08-phase-decomp: Phase decomposition: compress vs morph
Status: closed — verdict recorded
- harden vs harden-quarter: 1 vs 5, 0 ties (p = 0.2188)
- harden vs rigid: 5 vs 1, 0 ties (p = 0.2188)
- harden vs snap: 5 vs 1, 0 ties (p = 0.2188)

## C09-seed-scale: Seed scaling: discovery curves on signature instances
Status: closed — verdict recorded
- harden vs rigid: 5 vs 1, 0 ties (p = 0.2188)

## C10-container-frustration: Container frustration: concave families in a triangle
Status: closed — verdict recorded
- harden vs rigid: 5 vs 7, 0 ties (p = 0.7744)

## C11-cross-anomaly: Tau0 sweep localizing the cross morph pathology
Status: closed — anomaly localized: morph breaks from near-full disks; scaffold-trap mechanism identified
- harden vs harden-quarter: 0 vs 2, 0 ties (p = 0.5)
- harden vs harden-tau05: 0 vs 2, 0 ties (p = 0.5)
- harden vs harden-tau075: 1 vs 1, 0 ties (p = 1)

## Findings
- C00: concave compound pieces run end-to-end. 48 runs, 0 errors; the independent verifier reports 0 overlaps and full containment on all 12 best packings; the convex control holds (harden best_L 3.0000 <= rigid 3.0000 on squ-in-squ n=6). The generalized engine is bit-identical to the parent engine on convex families (5/5 differential cases), agrees with brute-force overlap on 1200/1200 concave configurations, and passes a finite-difference gradient check at 8.47e-11. (evidence: C00-verify-concave) [C00-verify-concave 2026-10-09]
- C01 concave pilot (1600 runs, 0 errors, 100/100 best packings verified overlap-free): the strong two-factor prediction is NOT supported. At tie tolerance 1e-4, concave harden vs rigid is 5 vs 5 with 7 ties (p=1); strict 1e-9 counts (7 vs 10) are inflated by 1e-6 legalization noise visible on squ-in-squ controls. The effect is instance-heterogeneous, not family-level: harden wins decisively on ltri n=5 (+0.61, 13%) and n=6 (+0.03), star5 n=7 (+0.011), n=8 (+0.033), n=9 (+0.10); rigid wins decisively on ltri n=7 (-0.27), n=8 (-0.10), cross n=5 (-0.33), n=8 (-0.18). Orientation variance of best rigid packings correlates only 0.27 with harden advantage - no clean geometric predictor emerges. harden crushes the classical baselines on concave: vs sa 19-6 (p=0.015), vs pc 24-1 (p=1.5e-6). Positive control (squ-in-squ) did not replicate the parent's n=11 signature at 16 seeds - likely a power issue (parent used 32 runs for a rare tilted-basin event), to be checked by a targeted replication. (evidence: C01-concave-pilot) [C01-concave-pilot 2026-10-09]
- C02a replication PASSES: the generalized engine reproduces the parent's signature - squ-in-squ n=11 harden best-of-32 = 3.87708674 (Trump's record 3.87708359 + 3.2e-6) vs rigid best 3.88826742. Fresh baselines: ltri n=5 harden 4.00000061 vs rigid 4.61096103; star5 n=9 harden 4.57295043 vs rigid 4.67261308. 128 runs, 0 errors, 6/6 best packings verified. Proceeding to C02b handoff as pre-registered. (evidence: C02a-baselines-replication) [C02a-baselines-replication 2026-10-09]
- C02b-ltri handoff SUCCEEDS: rigid-from-checkpoint best-of-16 = 4.000000 (all 16 runs hit the pinwheel, median 4.000000) vs rigid-from-random best-of-16 = 4.747547 (median 5.000001). Decision rule met: checkpoint <= harden best (4.00000061) + 1e-3 and random > harden best + 0.01. The morph's contribution on ltri n=5 is basin delivery: rigid search reaches the pinwheel from the tau~0.5 neighborhood but not from random starts. 32 runs, 0 errors, 17/17 best packings verified. (evidence: C02b-handoff-ltri) [C02b-handoff-ltri 2026-10-09]
- C03 ablation: BOTH harden-half (best 4.000000) and harden-quarter (best 4.000001) reach the ltri n=5 pinwheel; rigid best 4.610961. Per the pre-registered rule, the critical interval is tau in [0, 0.25]: even a small amount of corner rounding (tau0=0.25) suffices for the compress phase to find the pinwheel positions, and the short remaining morph grows the corners in. The disk phase is not necessary. 48 runs, 0 errors, 3/3 best packings verified. (evidence: C03-morph-fraction) [C03-morph-fraction 2026-10-09]
- C02b-star5 handoff SUCCEEDS: rigid-from-checkpoint best-of-16 = 4.572969 (within 1.9e-5 of C02a harden best 4.57295043; median 4.655183) vs rigid-from-random best-of-16 = 4.684325 (median 4.858657). Decision rule met on both clauses. Basin delivery confirmed on a second concave family: rigid search reaches harden's basin from the tau~0.5 neighborhood but not from random starts. 32 unique runs (worker races produced duplicate rows, deduped by id), 0 errors, 17/17 best packings verified. (evidence: C02b-handoff-star5) [C02b-handoff-star5 2026-10-09]
- C04: the n=11 signature is NOT square-specific. squ-in-squ: harden 3.877087 reaches Trump's record, rigid 3.888267 does not (signature present). tri-in-squ: harden 2.490961 vs record 2.49, rigid 2.500019 (signature present). pen-in-squ: harden 5.115946 vs rigid 5.115562, both within 4e-4 of Friedman's 5.11555 record - a tie, no signature. hex-in-squ: rigid 6.332907 beats harden 6.339748 and sits nearer the 6.33218 record - a rigid win. The pre-registered square-specific hypothesis is rejected; the pattern now needs the meta-analysis (disk_share/symmetry as candidate moderators). 256 runs, 0 errors, 8/8 verified. (evidence: C04-convex-rare) [C04-convex-rare 2026-10-09]
- C06 pen-in-pen: all four instances (n=5..8) are ties between harden and rigid at 1e-4 (identical bests: 2.618034, 2.618034, 3.078690, 3.335175). No hardening advantage for pentagons in a pentagonal container at these n - consistent with the parent's C15 (pentagons in a square: 1 vs 8) and with C04's pen-in-squ n=11 tie. Pentagons look like a shape where the effect is absent regardless of container. 128 runs, 0 errors, 8/8 best packings verified with the fixed pentagon tightContainer branch. (evidence: C06-pen-in-pen) [C06-pen-in-pen 2026-10-09]
- C05 REJECTS the pre-registered nocompress hypothesis (2/7 instances, needed >=5): harden-nocompress usually fails badly (ltri n=5: 4.6213 vs harden 4.0000). Correction to the C03 reading: the COMPRESS phase is essential - C03's harden-quarter still had a compress phase (at tau=0.25). What the data now say: (a) a soft compress phase is required to arrange positions; (b) the morph may start nearly rigid (tau0=0.25 suffices on 4/7: ltri 5,6, star5 7,9); (c) the full disk-to-shape morph is overkill. Surprises: on cross n=5 the full morph HURTS (harden 6.6569 vs half/quarter/nocompress/rigid all 6.3246); on star5 n=8 only the full morph reaches 4.4173. 560 runs, 0 errors, 35/35 verified. (evidence: C05-morph-parts) [C05-morph-parts 2026-10-09]
- C07: no clean monotonic trend of harden advantage with n. ltri: ties at n=9,10 (6.0), harden wins big at n=11 (6.5769 vs 7.0). cross: tie at n=9, rigid wins n=10 (8.7089 vs 8.8375) and n=11 (9.1924 vs 9.3279). star5: rigid n=10 by 0.007, harden n=11 by 0.011. The pre-registered trend test goes to the meta-analysis pooled with C01/C02a. 256 runs, 0 errors, 16/16 verified. (evidence: C07-concave-scale) [C07-concave-scale 2026-10-09]
- META-ANALYSIS (pre-registered): no tested predictor survives. 37 instances, 9 harden-win events. H1 concavity: 7/22 concave vs 2/15 convex, one-sided Fisher p=0.187, fail to reject. H2 n-trend within concave: ltri Z=-0.76 p=0.78, star5 Z=1.15 p=0.126, pooled Z=0.49 p=0.31, fail to reject. H3 disk_share: medians both 0.408, one-sided Mann-Whitney p=0.149, fail to reject. Mixed-effects logistic (7 fixed + family random intercept on 37 obs/9 events) is overparameterized: family-level covariates compete with the random intercept (family_sd collapses to ~0 with huge uncertainty) and VB intervals are implausibly tight - reported as unstable per the plan's contingency. Sensitivity: pooled-duplicate resolution changes 0/37 outcomes. Correction recorded: the frozen plan misremembered C01's design (actual: ltri 5-10, cross 4-8, star5 5-10, squ 8-12, tri 8-10); inclusion corrected to the real design, intent unchanged. Headline: hardening wins are real (9/37, incl. replicated n=11 signatures and the ltri pinwheel) but NOT predicted by concavity, piece count trend, or disk share. Events cluster in ltri (3/7) and star5 (4/7); cross is 0/8 despite being concave. (evidence: meta-analysis) [META 2026-10-09]
- C11 tau0 sweep: the full morph breaks only from near-full disks. Cross n=5: tau0 in {0.25,0.5,0.75} all reach 6.3246, only tau0=1.0 fails (6.6569). Cross n=8: tau0=0.25 reaches 7.6026, tau0>=0.5 stuck at ~7.78. Trajectory analysis: disk-compress packs to L=3.29 (disks pack far tighter than plus-shapes); the morph must then expand enormously as corners grow and gets trapped in the disk-optimal scaffold's basin (final 6.6569). Quarter-compress ends at L=5.83 and the morph is a gentle refinement to 6.3246. Mechanism refined: the compress scaffold can be a TRAP when the disk-optimal arrangement is topologically far from any good polygonal arrangement; the morph is local and inherits the scaffold's basin. Contrast ltri n=5 where the disk scaffold is in the right basin and compress is essential (C05). [C11-cross-anomaly 2026-10-10]
- C08: gradual morph is ESSENTIAL, not theater. snap (disk-compress then instant rigid) within 1e-3 of harden on only 2/6 instances (star5 n=9, tri n=11); harden beats snap by >1e-3 on 4/6, catastrophically on ltri (snap 11.57/22.11 vs harden 4.00/6.58). The tight disk scaffold cannot survive an instant snap; corners must grow gradually. harden-quarter >= harden-full on 6/6 (quarter best or tied everywhere) — full disk phase never better. Refined mechanism: compress proposes a (sometimes tight) scaffold; the GRADUAL morph preserves it while growing corners. [C08-phase-decomp 2026-10-10]
- C09: seed-scaling hypothesis NOT supported in general (gap widens on 3/6, needed 5/6). Nuanced pattern: squ n=11 signature emerges at 32 seeds (gap flips -0.01 to +0.011, rare basin confirmed); ltri n=5 is a fixed offset (harden finds 4.0 by 16 seeds, rigid never does); ltri n=11 rigid CATCHES UP by 32 seeds (gap shrinks 0.42 to 0.03) — that basin is not that rare, rigid just needs tries; star5 n=9 fixed offset. Hardening's edge is sometimes early discovery, sometimes budget-dependent, sometimes erodible. [C09-seed-scale 2026-10-10]
- C10: frustration hypothesis REJECTED for cross — 0/4 harden wins in triangle container (1 tie, 3 rigid losses), matching its 0/8 in squares. Cross never benefits regardless of container; its optima are grid-obvious and its disk scaffold is always a trap (C11). ltri wins 3/4 in triangle (n=6,7,8), star5 wins 1/4 (n=8). Container frustration does not create hardening advantage; the piece-level story stands. [C10-container-frustration 2026-10-10]
- A12 scaffold-fidelity rule (49 instances, 13 harden wins): the disk scaffold's relative arrangement predicts hardening's outcome. Scaffold fidelity = Spearman rank corr of pairwise centroid distances at compress-end vs the best-known optimum. Fidelity -> harden's gap to global optimum: rho=-0.562, p<0.0001. Fidelity higher on wins (0.453) than non-wins (0.083), Mann-Whitney one-sided p=0.0084; fidelity -> win margin rho=0.451, p=0.0011. First quantitative predictor that works. Refinement: fidelity predicts harden's ABSOLUTE success; the WIN additionally requires rigid to fail (high-fidelity ties exist: ltri n=9,10). A13 basin narrowness does NOT predict (rho=-0.02, p=0.91). A14 morph-commitment timing does NOT discriminate (p=0.24). [None 2026-10-09]
