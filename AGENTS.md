# Notes for AI agents working in this repository

Read `ARCHITECTURE.md` first. The short version:

- **Never edit results.** `campaigns/*/runs*.jsonl` are append-only; `ledger/` is written only by `packing/ledger.py`.
- **Plan before running.** A new experiment is a new folder `campaigns/Cxx-name/plan.json` (question, hypothesis, instances, methods, budgets, seeds, decision rule), committed before its first run. If a plan must change after runs started, add an entry to its `amendments` list; do not rewrite it.
- **Run:** `.venv/bin/python -m packing.runner campaigns/<C>/plan.json --worker 0 --of 2` (and `--worker 1`). Resumable; safe to kill. (Node engine underneath; see `engine/`. Dependencies live in `.venv`, created with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.)
- **Record:** `.venv/bin/python -m packing.ledger ingest <C>`. Add conclusions with `.venv/bin/python -m packing.ledger finding "<text>" --evidence <cell ids> --campaign <C>` and `.venv/bin/python -m packing.ledger close <C> "<decision taken, citing the decision rule>"`.
- **Project:** `.venv/bin/python -m packing.project` regenerates README tables, `JOURNAL.md`, campaign reports, site data and paper numbers. Never type a number into those files by hand.
- **Concave pieces are compound.** A concave piece is a list of convex parts sharing one pose; collision is part-pair SAT. See `engine/engine2d.js` and `ARCHITECTURE.md`. The convex path is regression-tested against the parent project — do not "simplify" it.
- **No exact certificates for concave families.** `packing/certify.py` covers convex families only. Concave claims are head-to-head comparisons at matched budget (see ARCHITECTURE.md "Why no external records").
- **No personal email.** Do not put an email address in the paper, the site or any committed file. Before the first commit in a clone, set `git config user.email "<noreply>"` (name `Yohei Nakajima`), so the author address never enters the history.
