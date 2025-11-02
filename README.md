# SecSuite

[![CI (uv)](https://github.com/Magic-Man-us/SecSuite/actions/workflows/ci.yml/badge.svg)](https://github.com/Magic-Man-us/SecSuite/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Security: safety](https://img.shields.io/badge/security-safety-blue.svg)](https://github.com/pyupio/safety)

A modern Python package template with best practices, using `uv` for package management, pytest with coverage, Sphinx documentation, and Ruff for linting/formatting.

## Installation

### Install

Recommended: use `uv` which manages virtual environments and installs reproducibly. For development, prefer syncing the project to create the venv and install dependencies.

```bash
# Create the development environment and install dependencies
uv sync --all-extras
# For installation instructions for uv itself see: https://docs.astral.sh/uv/
```

### Development Installation

Clone the repository and install with all development dependencies:

```bash
git clone https://github.com/Magic-Man-us/secsuite.git
cd secsuite
uv sync --all-extras
```

## Features

- **Modern Python**: Built for Python 3.11+ with full type hints
- **uv**: Fast, modern package management and virtual environments
- **Testing**: pytest with coverage reporting and fixtures
- **Documentation**: Sphinx with Read the Docs theme
- **Linting**: Ruff for ultra-fast linting and formatting
- **Type Safety**: mypy for static type checking
- **Best Practices**: PEP 8, PEP 257, PEP 484, PEP 585, PEP 604
- **src/ Layout**: Proper package structure
- **Pre-commit**: Automated checks before commits

## Security

This project runs automated security checks (Bandit for static analysis and Safety for dependency vulnerabilities). See the full documentation at :doc:`docs/security` or open the page at `docs/security.rst`.

Run the checks locally (uv-first):

```bash
# sync dev tools into the uv venv
uv sync --all-extras

# run Bandit (JSON + SARIF)
uv run bandit -r src/ -f json -o bandit-report.json
uv run bandit -r src/ -f sarif -o bandit-report.sarif

# run Safety
uv run safety check --json > safety-report.json

# apply threshold checks (same scripts CI uses)
python scripts/security_bandit_check.py
python scripts/security_safety_check.py
```

## Installation

### Install

Recommended: use `uv` for development and releases. To get set up for development, run:

```bash
uv sync --all-extras
# For uv installation instructions: https://docs.astral.sh/uv/
```

### Development Installation

Clone the repository and install with all development dependencies:

```bash
git clone https://github.com/Magic-Man-us/secsuite.git
cd secsuite
uv sync --all-extras
```

## Quick Start

```python
from secsuite import ExampleClass, example

# Use the example class
obj = ExampleClass(name="demo", value=42, tags=["python", "example"])
result = obj.process()
print(result)
# Output: {'name': 'demo', 'value': 42, 'tag_count': 2}

# Use the example function
items = example(["hello", "world"])
print(items)
# Output: ['HELLO', 'WORLD']
```

## Development

### Setup Development Environment

```bash
# Create virtual environment and install dependencies
uv sync --all-extras

# Activate the virtual environment (if needed)
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov

# Run specific test file
uv run pytest tests/test_example.py

# Run specific test
uv run pytest tests/test_example.py::TestExampleClass::test_creation
```

### Code Quality

```bash
# Lint code
uv run ruff check .

# Format code
uv run ruff format .

# Type check
uv run mypy src

# Run all checks
uv run ruff check . && uv run ruff format --check . && uv run mypy src
```

### Building Documentation

```bash
# Build HTML documentation
uv run sphinx-build -b html docs docs/_build

# Open in browser (Linux/Mac)
open docs/_build/index.html

# Open in browser (Windows)
start docs/_build/index.html
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run checks before commits:

```bash
uv run pre-commit install

# Run manually
uv run pre-commit run --all-files
```

## Project Structure

```
secsuite/
├── .github/
│   └── copilot-instructions.md  # GitHub Copilot instructions
├── docs/                         # Sphinx documentation
│   ├── api/
│   │   └── modules.rst
│   ├── conf.py
│   ├── index.rst
│   ├── installation.rst
│   ├── quickstart.rst
│   └── Makefile
├── src/
│   └── secsuite/                 # Main package
│       ├── __init__.py
│       ├── example.py
│       └── py.typed              # PEP 561 marker
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py               # pytest fixtures
│   └── test_example.py
├── .gitignore
├── .pre-commit-config.yaml       # Pre-commit hooks
├── LICENSE
├── pyproject.toml                # All project configuration
└── README.md
```

## Configuration

All configuration is centralized in `pyproject.toml`:

- **Build system**: Hatchling
- **Dependencies**: Core and optional (dev, docs)
- **Ruff**: Linting and formatting rules
- **mypy**: Type checking configuration
- **pytest**: Test discovery and coverage settings

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
 
## Continuous Integration & Development

This repository includes a GitHub Actions workflow located at `.github/workflows/ci.yml` that runs tests, Ruff, and mypy on push and pull requests for Python 3.11, 3.12 and 3.13.

For local development instructions, see `DEV.md`.
3. Make your changes
4. Run tests and linting (`uv run pytest && uv run ruff check .`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Built with:
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- [Ruff](https://github.com/astral-sh/ruff) - Ultra-fast Python linter and formatter
- [pytest](https://pytest.org/) - Testing framework
- [mypy](https://mypy-lang.org/) - Static type checker
- [Sphinx](https://www.sphinx-doc.org/) - Documentation generator

## Support

- Documentation: [Read the Docs](https://secsuite.readthedocs.io)
- Issues: [GitHub Issues](https://github.com/Magic-Man-us/secsuite/issues)
- Discussions: [GitHub Discussions](https://github.com/Magic-Man-us/secsuite/discussions)
