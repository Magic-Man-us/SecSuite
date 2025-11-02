<!-- Use this file to provide workspace-specific custom instructions to Copilot. -->

## Project: SecSuite

A modern Python package using uv, pytest with coverage, Sphinx documentation, and Ruff for linting/formatting.

### Development Tools
- **uv**: Package management and virtual environment
- **Ruff**: Linting and formatting
- **mypy**: Type checking
- **pytest**: Testing with coverage
- **Sphinx**: Documentation

### Project Structure
- `src/secsuite/`: Main package source
- `tests/`: Test suite
- `docs/`: Sphinx documentation
- `pyproject.toml`: All configuration

### Commands
- `uv run pytest`: Run tests
- `uv run pytest --cov`: Run tests with coverage
- `uv run ruff check .`: Lint code
- `uv run ruff format .`: Format code
- `uv run mypy src`: Type check
- `uv run sphinx-build -b html docs docs/_build`: Build docs
