# Development Guide

This document describes how to set up your development environment and run the quality checks used by this project.

## Prerequisites

- Python 3.11+
- uv (recommended)

## Quick setup

Using uv (recommended):

```bash
# Sync and install all development dependencies
uv sync --all-extras

# Activate venv (if needed)
source .venv/bin/activate  # Linux/Mac
# or
.venv\\Scripts\\activate  # Windows
```

Note: this project prefers `uv`. If you must use pip, follow your local environment's documented practices; this repo does not execute pip commands in CI.

## Common commands

Run tests with coverage:

```bash
uv run pytest --cov
```

Run Ruff linting and formatting:

```bash
uv run ruff check .
uv run ruff format .
```

Type check with mypy:

```bash
uv run mypy src
```

Build docs:

```bash
uv run sphinx-build -b html docs docs/_build
```

## CI

This repository uses GitHub Actions (`.github/workflows/ci.yml`) to run the test, lint, and type checks on push and pull requests against Python 3.11, 3.12, and 3.13.

Notes about the CI workflow:

- The workflow uses `uv` to create and manage the virtual environment and to run commands (`uv sync --all-extras`, `uv run pytest`, etc.).
- The `.venv` directory is cached between runs to speed up CI.
- Coverage artifacts (`coverage.xml` and `htmlcov`) and Sphinx-built docs (`docs/_build`) are uploaded as GitHub Actions artifacts per Python matrix job. You can download them from the Actions UI for each job run.

<!-- Artifact downloader removed by request: references removed to avoid requiring personal tokens. -->
