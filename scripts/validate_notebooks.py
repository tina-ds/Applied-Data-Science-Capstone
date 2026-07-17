"""Perform dependency-free structural validation of repository notebooks."""

from __future__ import annotations

import json
import os
from pathlib import Path


EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "artifacts",
    "pycache",
    "venv",
}


def _is_excluded_directory(relative_path: Path) -> bool:
    """Return whether a relative directory path should be skipped."""
    if any(part in EXCLUDED_DIRECTORY_NAMES for part in relative_path.parts):
        return True
    return relative_path.parts[-2:] == ("reports", "generated")


def find_notebooks(root: Path) -> list[Path]:
    """Return notebooks below root without traversing service directories."""
    notebooks: list[Path] = []
    for directory, subdirectories, filenames in os.walk(root):
        current_directory = Path(directory)
        subdirectories[:] = [
            name
            for name in subdirectories
            if not _is_excluded_directory(
                (current_directory / name).relative_to(root)
            )
        ]
        notebooks.extend(
            current_directory / filename
            for filename in filenames
            if filename.endswith(".ipynb")
        )
    return sorted(notebooks)


def validate_notebook(path: Path) -> list[str]:
    """Return structural validation errors for one notebook."""
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        return [f"{path}: cannot read notebook JSON: {exc}"]

    if not isinstance(notebook, dict):
        return [f"{path}: notebook root must be an object"]

    errors: list[str] = []
    nbformat = notebook.get("nbformat")
    if (
        not isinstance(nbformat, int)
        or isinstance(nbformat, bool)
        or nbformat != 4
    ):
        errors.append(f"{path}: expected nbformat 4")

    nbformat_minor = notebook.get("nbformat_minor")
    if (
        not isinstance(nbformat_minor, int)
        or isinstance(nbformat_minor, bool)
        or nbformat_minor < 0
    ):
        errors.append(f"{path}: nbformat_minor must be a non-negative integer")

    if not isinstance(notebook.get("metadata"), dict):
        errors.append(f"{path}: notebook metadata must be an object")

    cells = notebook.get("cells")
    if not isinstance(cells, list):
        errors.append(f"{path}: cells must be a list")
        return errors

    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            errors.append(f"{path}: cell {index} must be an object")
            continue

        cell_type = cell.get("cell_type")
        if not isinstance(cell_type, str) or cell_type not in {
            "code",
            "markdown",
            "raw",
        }:
            errors.append(f"{path}: cell {index} has an invalid cell_type")

        if not isinstance(cell.get("metadata"), dict):
            errors.append(f"{path}: cell {index} metadata must be an object")

        source = cell.get("source")
        if not isinstance(source, (str, list)):
            errors.append(f"{path}: cell {index} source must be text or a list")
        elif isinstance(source, list) and not all(
            isinstance(line, str) for line in source
        ):
            errors.append(f"{path}: cell {index} source contains non-text entries")

        if cell_type == "code":
            if not isinstance(cell.get("outputs"), list):
                errors.append(f"{path}: code cell {index} outputs must be a list")

            execution_count = cell.get("execution_count")
            if execution_count is not None and (
                not isinstance(execution_count, int)
                or isinstance(execution_count, bool)
            ):
                errors.append(
                    f"{path}: code cell {index} execution_count must be an integer or null"
                )

            if "execution_count" not in cell:
                errors.append(f"{path}: code cell {index} is missing execution_count")

    return errors


def main() -> int:
    notebooks = find_notebooks(Path.cwd())
    if not notebooks:
        print("No notebooks found")
        return 1

    errors = [error for path in notebooks for error in validate_notebook(path)]
    if errors:
        print("\n".join(errors))
        return 1

    print(f"Validated {len(notebooks)} notebook(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
