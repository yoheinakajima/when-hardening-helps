# C13-fidelity-validation: Held-out validation of the scaffold-fidelity rule

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the scaffold-fidelity rule predict on held-out instances?

**Hypothesis.** The A12 scaffold-fidelity rule generalizes: on 10 held-out instances (no data in the 49-instance discovery set), higher scaffold fidelity predicts smaller harden gap to the optimum. These instances span ltri/star5/cross in squares, convex rare-event territory (squ/tri n=12,13), and triangle containers - chosen to include expected wins, ties, and losses.

**Decision rule.** PRIMARY (replication): compute scaffold fidelity exactly as in A12 (Spearman rank corr of pairwise centroid distances at compress-end vs best-known optimum across methods). One-sided test: Spearman(fidelity, harden_gap_to_optimum) < -0.3 with p < 0.05 on these 10 held-out instances -> the A12 rule replicates as a predictive relationship. SECONDARY (exploratory, not confirmatory): proxy fidelity using best-of-16 rigid arrangement as D_opt stand-in; assess whether it predicts win/tie a priori. If primary fails, the A12 rule does not generalize and is reported as overfit to the discovery set.

**Status.** closed — **decision:** rule replicates (rho=-0.795, p=0.003); predicted first cross win

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **5 vs 5**, 0 ties (two-sided p = 1)

| instance | harden | rigid |
|---|---|--|
| cross-in-squ n=12 | 9.611190 (16 runs) | 9.658884 (16 runs) |
| cross-in-squ n=13 | 10.023600 (16 runs) | 9.899997 (16 runs) |
| ltri-in-squ n=12 | 7.000002 (16 runs) | 6.882792 (16 runs) |
| ltri-in-squ n=13 | 7.000003 (16 runs) | 7.047380 (16 runs) |
| ltri-in-tri n=9 | 9.268482 (16 runs) | 9.350863 (16 runs) |
| ltri-in-tri n=10 | 9.921018 (16 runs) | 9.594905 (16 runs) |
| squ-in-squ n=13 | 4.000001 (16 runs) | 4.000001 (16 runs) |
| star5-in-squ n=12 | 5.390120 (16 runs) | 5.461827 (16 runs) |
| star5-in-tri n=9 | 7.196489 (16 runs) | 7.350270 (16 runs) |
| tri-in-squ n=12 | 2.569786 (16 runs) | 2.562444 (16 runs) |
