Security
========

Security checks included in this project
---------------------------------------

This project runs two automated security checks as part of CI and as local developer commands:

- Bandit: static analysis for common security issues in Python code. The workflow runs Bandit and produces both JSON and SARIF outputs. The SARIF file is uploaded to GitHub Code Scanning.
- Safety: checks vulnerabilities in pinned dependency metadata. The workflow runs Safety and outputs JSON.

CI integration
--------------

The CI workflow (`.github/workflows/ci.yml`) has a dedicated `security` job which:

- Installs `uv` and syncs project dev dependencies via `uv sync --all-extras`.
- Runs Bandit with JSON and SARIF outputs (`bandit-report.json`, `bandit-report.sarif`). The SARIF is uploaded to GitHub via the CodeQL SARIF uploader.
- Runs Safety and writes `safety-report.json`.
- Invokes project helper scripts to apply thresholds and determine job failure:

  - `scripts/security_bandit_check.py` — reads `bandit-report.json` and exits according to the `SECURITY_FAIL_LEVEL` environment variable (NONE | MEDIUM | HIGH).
  - `scripts/security_safety_check.py` — reads `safety-report.json` and fails if vulnerabilities are present.

Local usage (uv-first)
-----------------------

Run the security checks locally inside your uv-managed environment:

.. code-block:: bash

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

Artifacts and CI links
----------------------

The CI uploads the following artifacts for inspection:

- `bandit-report.json`
- `bandit-report.sarif` (uploaded to GitHub Code Scanning)
- `safety-report.json`

If you want to learn more about how thresholds are applied, inspect `scripts/security_bandit_check.py` and `scripts/security_safety_check.py` in the repository root.
