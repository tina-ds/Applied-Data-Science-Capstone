"""Tests for the dependency-free notebook validator."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from typing import Any

from scripts.validate_notebooks import find_notebooks, validate_notebook


def valid_notebook() -> dict[str, Any]:
    """Return a minimal valid nbformat 4 notebook."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {},
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["# Example\n"],
            },
            {
                "cell_type": "code",
                "metadata": {},
                "source": "print('example')",
                "outputs": [],
                "execution_count": None,
            },
        ],
    }


class ValidateNotebookTests(unittest.TestCase):
    """Exercise successful and malformed notebook inputs."""

    def validate_payload(self, payload: object) -> list[str]:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "notebook.ipynb"
            path.write_text(json.dumps(payload), encoding="utf-8")
            return validate_notebook(path)

    def test_valid_notebook(self) -> None:
        self.assertEqual(self.validate_payload(valid_notebook()), [])

    def test_damaged_json(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "notebook.ipynb"
            path.write_text("{not valid JSON", encoding="utf-8")

            errors = validate_notebook(path)

        self.assertEqual(len(errors), 1)
        self.assertIn("cannot read notebook JSON", errors[0])

    def test_root_must_be_an_object(self) -> None:
        errors = self.validate_payload([])

        self.assertEqual(len(errors), 1)
        self.assertIn("notebook root must be an object", errors[0])

    def test_cell_must_be_an_object(self) -> None:
        notebook = valid_notebook()
        notebook["cells"] = [1]

        errors = self.validate_payload(notebook)

        self.assertEqual(len(errors), 1)
        self.assertIn("cell 0 must be an object", errors[0])

    def test_invalid_cell_type_is_reported(self) -> None:
        notebook = valid_notebook()
        notebook["cells"][0]["cell_type"] = []

        errors = self.validate_payload(notebook)

        self.assertEqual(len(errors), 1)
        self.assertIn("cell 0 has an invalid cell_type", errors[0])

    def test_required_root_fields(self) -> None:
        notebook = valid_notebook()
        notebook.pop("nbformat_minor")
        notebook.pop("metadata")

        errors = self.validate_payload(notebook)
        messages = "\n".join(errors)

        self.assertIn("nbformat_minor must be a non-negative integer", messages)
        self.assertIn("notebook metadata must be an object", messages)

    def test_required_code_cell_fields(self) -> None:
        notebook = valid_notebook()
        code_cell = notebook["cells"][1]
        code_cell.pop("metadata")
        code_cell.pop("outputs")
        code_cell.pop("execution_count")

        errors = self.validate_payload(notebook)
        messages = "\n".join(errors)

        self.assertIn("cell 1 metadata must be an object", messages)
        self.assertIn("code cell 1 outputs must be a list", messages)
        self.assertIn("code cell 1 is missing execution_count", messages)

    def test_source_must_contain_only_text(self) -> None:
        notebook = valid_notebook()
        notebook["cells"][0]["source"] = ["valid", 1]

        errors = self.validate_payload(notebook)

        self.assertEqual(len(errors), 1)
        self.assertIn("source contains non-text entries", errors[0])


class FindNotebooksTests(unittest.TestCase):
    """Verify that repository service directories are not traversed."""

    def test_service_directories_are_excluded(self) -> None:
        excluded_directories = (
            ".git",
            ".venv",
            "venv",
            ".ipynb_checkpoints",
            "artifacts",
            "reports/generated",
            "__pycache__",
            "pycache",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        )

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            included_notebook = root / "included.ipynb"
            included_notebook.write_text("{}", encoding="utf-8")

            for relative_directory in excluded_directories:
                directory = root / relative_directory
                directory.mkdir(parents=True)
                (directory / "excluded.ipynb").write_text("{}", encoding="utf-8")

            notebooks = find_notebooks(root)

        self.assertEqual(notebooks, [included_notebook])


if __name__ == "__main__":
    unittest.main()
