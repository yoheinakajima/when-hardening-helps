# C17-fidelity-batch2: Second held-out validation, frozen measure

*Generated from the ledger by `packing/project.py`. Do not edit.*

**Question.** Does the frozen fidelity rule replicate on a second held-out batch?

**Hypothesis.** The scaffold-fidelity rule generalizes to a second held-out batch with the measure fully frozen.

**Decision rule.** Compute scaffold fidelity with the FROZEN measure (analysis/a12_a14.py, unchanged since A12). One-sided test: Spearman(fidelity, harden_gap_to_optimum) < -0.3 with p < 0.05 on these 8 held-out instances -> the rule survives a second frozen replication. These instances (n=13,14 and deeper triangle n) were never used in measure design (A12) or first validation (C13).

**Status.** closed — **decision:** replicates frozen (rho=-0.764, p=0.014)

## Head-to-head (best legalised container size per instance)

- harden vs rigid: **6 vs 2**, 0 ties (two-sided p = 0.2891)

| instance | harden | rigid |
|---|---|--|
| cross-in-squ n=14 | 10.073456 (16 runs) | 10.109717 (16 runs) |
| cross-in-tri n=11 | 14.059455 (16 runs) | 14.278740 (16 runs) |
| ltri-in-squ n=14 | 7.356130 (16 runs) | 7.438705 (16 runs) |
| ltri-in-tri n=11 | 10.254204 (16 runs) | 10.573128 (16 runs) |
| squ-in-squ n=14 | 4.000001 (16 runs) | 4.000000 (16 runs) |
| star5-in-squ n=13 | 5.594511 (16 runs) | 5.597779 (16 runs) |
| star5-in-tri n=10 | 7.422168 (16 runs) | 7.428108 (16 runs) |
| tri-in-squ n=13 | 2.595637 (16 runs) | 2.595601 (16 runs) |
