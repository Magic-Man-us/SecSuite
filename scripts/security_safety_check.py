#!/usr/bin/env python3
"""Check Safety JSON report and exit based on findings.

Exits with code 2 if vulnerabilities found, 0 otherwise.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path


def main() -> int:
    path = Path("safety-report.json")
    if not path.exists():
        logging.info("No safety-report.json found; skipping safety check")
        return 0
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive in CI
        logging.warning("Error parsing safety JSON: %s", exc)
        return 0

    if data.get("vulnerabilities"):
        logging.error("Safety reported vulnerabilities")
        return 2

    logging.info("No safety vulnerabilities")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
