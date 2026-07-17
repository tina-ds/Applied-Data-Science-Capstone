# AGENTS.md

This file defines how Codex and other coding agents should work in this
repository. Read it before planning or editing files.

## Project purpose

Turn the original IBM Data Science capstone into a reproducible portfolio
project while preserving its educational provenance. The finished project
should demonstrate data collection, data cleaning, exploratory analysis,
interactive visualisation, and supervised machine learning.

## Current state

- The default branch is `master`.
- Course notebooks, reports, certificates, images, and the Dash script are in
  the repository root.
- Project runtime dependencies are not yet defined; initial standard-library
  structural tests are available.
- Some notebooks depend on external services or data that may have changed.

Treat the existing notebooks and reports as source material. Do not rewrite or
delete them until a replacement has been verified and the change is explicitly
included in the active task.

## Non-negotiable rules

1. Do not work directly on `master` without separate, explicit permission from
   the repository owner; normally create a focused branch.
2. Plan before editing when a task touches more than one project layer.
3. Keep each pull request focused and independently reviewable.
4. Do not invent metrics, model scores, plots, or conclusions. Recompute them
   from versioned code and data.
5. Preserve attribution to IBM coursework and clearly distinguish supplied
   exercises from independent improvements.
6. Do not commit credentials, tokens, personal data, large generated files, or
   private customer data.
7. Pin or bound dependencies once the runtime is established.
8. Add or update tests whenever reusable Python logic changes.
9. Run the relevant checks before committing and report any check that could
   not be run.
10. Avoid broad notebook rewrites. Extract reusable logic into Python modules
    and keep notebooks focused on explanation and results.
11. Codex and other agents must not commit, push, merge, create tags, modify
    remote branches, or work directly on `master` without separate, explicit
    permission from the repository owner.

## Target repository layout

The target is incremental; do not create empty directories solely to match it.

```text
.
├── README.md
├── pyproject.toml
├── src/space_race/        # reusable data, analysis, and model code
├── app/                   # Dash application
├── notebooks/             # ordered, explanatory notebooks
├── data/
│   ├── raw/               # immutable input snapshots or download instructions
│   └── processed/         # reproducible derived datasets
├── tests/                 # unit and integration tests
├── docs/                  # workflow, provenance, and portfolio notes
└── .github/               # CI and contribution templates
```

## Development workflow

1. Open or select one issue with a clear outcome.
2. Create a branch named `agent/<short-description>`.
3. Record the goal, constraints, and definition of done in the issue or plan.
4. Make the smallest coherent change.
5. Run checks and inspect generated results.
6. Open a draft pull request against `master`.
7. Review the diff, evidence, and rendered outputs before merging.
8. Prefer squash merge for a clean portfolio history.

## Verification

Until a project environment is introduced, run:

```bash
python -m compileall -q SpaceX_dash_app.py scripts
python -m unittest discover -s tests
python scripts/validate_notebooks.py
```

As the repository is modernised, replace these minimal checks with the commands
defined in `pyproject.toml` and keep this section current. A future full check
should include formatting, linting, expanded unit and integration tests,
notebook/data validation, and a smoke test of the dashboard.

## Definition of done

A task is done only when:

- its acceptance criteria are satisfied;
- relevant automated checks pass;
- documentation matches the actual behaviour;
- results are reproducible from documented inputs;
- no secrets or unrelated generated files are included;
- the pull request explains what changed, why, and how it was verified.
