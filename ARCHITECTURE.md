# How this repository works

One question runs through everything here: **can we predict where hardening helps, and why?**

The parent project ([soft-to-rigid](https://yoheinakajima.github.io/soft-to-rigid/)) showed that *hardening* — starting each piece as its inscribed disk and morphing it into the target shape while the container compresses — is not a better default than rigid starts, but is a *different* search: on squares in a square it reached packings no other method found. On triangles, hexagons, pentagons, octagons and four held-out families it showed no advantage. This project tests a two-factor hypothesis that fits all of that data:

1. **Path length** — how different the polygon is from its inscribed disk (the "room" the morph has to work with): triangle ~40%, square ~21%, pentagon ~14%, hexagon ~9%, octagon ~4% of piece area.
2. **Hidden tilted optima** — best-known packings with orientations a rigid search cannot easily reach.

Square-in-square is the only tested family with both. The flagship prediction: **concave pieces** (L-trominoes, crosses, stars) have enormous deviation from their inscribed disk and their optima must involve interlocking orientations — hardening should show its *largest* advantage here. If it does not, the hypothesis is dead and the square result is corner- or schedule-specific. The falsification condition is pre-registered in the flagship campaign plan.

## Six nouns

| Noun | What it is | Where it lives |
|---|---|---|
| **family** | a shape and a container, e.g. `ltri-in-squ` (unit L-trominoes in a square) | `catalog/<family>.json`: geometry; concave families carry no external records (see below) |
| **instance** | a family at one n, e.g. `ltri-in-squ/n8` | an entry inside the family file |
| **method** | a path through shape space plus a schedule, e.g. `harden`, `rigid`, `sa`, `pc` | `methods/<method>.json` |
| **run** | one instance × method × seed × budget | one line in `campaigns/<C>/runs.jsonl` |
| **comparison** | a head-to-head cell result (concave families have no records to beat) | the ledger, rendered in `JOURNAL.md` |
| **finding** | a sentence we are willing to defend, linked to the runs that support it | the ledger, rendered in `JOURNAL.md` |

## Why no external records for concave families

No Friedman-style catalogue exists for concave packings. Every concave claim is therefore a *relative* statement at matched budget and frozen settings ("harden reached a smaller container than rigid on X of Y instances, exact two-sided sign test"), never a record claim. Convex control families reuse the parent project's catalogue values where available.

## Concave pieces are compound

A concave piece is a list of convex parts sharing one pose `(x, y, θ)`. Collision detection is part-pair separating-axis tests over the parts' world vertices; the morph transform

```
piece(γ, τ) = γ · [ (1−τ)·P ⊕ τ·ρc·D ]
```

is applied to every vertex of the whole piece about its centroid, with `ρc` the radius of a disk about the centroid guaranteed inside the piece (half the minimum centroid-to-edge distance). At τ=1 every piece is a disk; at τ=0 it is the exact concave polygon. The convex path through the engine is bit-identical to the parent project's and is regression-tested (C00).

## Campaigns are pre-registered

A campaign is a folder `campaigns/Cxx-name/`. Its `plan.json` is committed **before** any run: the question, hypothesis, instances, methods, seeds, budget, and the decision rule. Results are appended to `runs.jsonl`, one JSON object per run, never edited. `REPORT.md` in each campaign is generated, never written by hand.

## The ledger

The ledger is an [ActiveGraph](https://pypi.org/project/activegraph/) event store (`ledger/ledger.sqlite`, exported to `ledger/events.jsonl`, which is committed). Ingesting a campaign turns every run into an event and an object in the graph. Behaviors react: `runs.ingested` → cell summary objects; `campaign.closed` → summary objects (hit rates, best sides, timings). There is no polish/certify chain for concave families (see above); convex controls reuse the parent's tightening where records exist.

Findings are added by the researcher with evidence relations to campaigns and runs. Everything that a reader sees (the README table, `JOURNAL.md`, campaign reports, the site, the numbers in the paper) is a **projection** of the ledger, rebuilt by `python -m packing.project`. Replaying `events.jsonl` rebuilds the same state with no recomputation.

## Replays

The runner saves a decimated trajectory (shape softness, container size, every piece's pose, ~150 frames) for the best run of every instance × method. These live in `campaigns/<C>/replays/` and are what the site animates.

## Code

```
engine/     JavaScript simulators (fast inner loop)
  engine2d.js     every 2D method: harden, grow, rigid, sa, pc (+ concave compound pieces)
  run.js          worker: reads a job list, appends to runs.jsonl
packing/    Python
  ledger.py       ActiveGraph ledger: ingest, behaviors, findings
  project.py      projections: reports, journal, site data (incl. the front-page wall), paper numbers
  analyze.py      main tables (exact two-sided sign tests), best-of-k curves
  catalog.py      families and instances (concave families defined here, no external records)
  runner.py       campaign runner: expands plan.json into jobs, calls the node engine
scripts/    figures.py (paper figures), queue.sh (run campaigns in order)
paper/      the paper; its numbers are generated, never typed
site/       templates and viewers; built into _site/ and deployed by CI
```

## Rules

1. Nothing in a table is typed by hand. If a number appears, a projection produced it.
2. Raw results are append-only. Corrections are new runs.
3. A campaign's plan is committed before its first run.
4. Concave claims are relative (head-to-head), never records.
5. Failures are recorded the same way as successes.
