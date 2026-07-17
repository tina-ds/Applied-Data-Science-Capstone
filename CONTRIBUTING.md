# Contributing

This repository is being modernised in small, reviewable stages. The historical
course materials remain available while reusable code and reproducible results
are introduced alongside them.

## Branches and pull requests

- Keep `master` stable.
- Use `agent/<short-description>` for Codex-assisted work.
- Use one branch and one pull request per coherent task.
- Open pull requests as drafts until checks pass and the result has been
  reviewed.
- Prefer squash merging after approval.

Examples:

```text
agent/workflow-foundation
agent/reproducible-environment
agent/extract-data-pipeline
agent/modernise-dashboard
```

## Commit messages

Use a short imperative summary that describes the outcome:

```text
Add repository workflow foundation
Extract launch data transformations
Add dashboard smoke test
```

## Notebook policy

- Keep notebooks explanatory and reasonably small.
- Move reusable logic to importable modules.
- Avoid hidden state: restart the kernel and run all cells before publishing.
- Do not commit credentials or outputs containing sensitive data.
- Record the source and retrieval date for external data.
- Do not change a numerical conclusion without reproducible evidence.

## Pull request checklist

Before requesting review:

1. Confirm the change matches one stated goal.
2. Run the checks listed in `AGENTS.md`.
3. Inspect notebook and dashboard output when applicable.
4. Update documentation and provenance notes.
5. Confirm that the diff contains no secrets, unrelated files, or accidental
   notebook output.
