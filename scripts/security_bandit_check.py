#!/usr/bin/env python3
"""Check bandit JSON report and exit based on SECURITY_FAIL_LEVEL.

SECURITY_FAIL_LEVEL: NONE | HIGH | MEDIUM (default MEDIUM)
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path


def main() -> int:
    logging.basicConfig(level=logging.INFO)
    level = os.environ.get("SECURITY_FAIL_LEVEL", "MEDIUM").upper()
    path = Path("bandit-report.json")
    exit_code = 0
    if not path.exists():
        logging.info("No bandit-report.json found; skipping bandit threshold check")
        return exit_code

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - defensive in CI
        logging.warning("Error parsing bandit JSON: %s", exc)
        return exit_code

    sevs = {issue.get("issue_severity", "") for issue in data.get("results", [])}

    if level == "NONE":
        logging.info("SECURITY_FAIL_LEVEL=NONE: not failing on bandit issues")
        return exit_code

    if level == "HIGH":
        if "HIGH" in sevs:
            logging.error("Failing on HIGH bandit issues")
            exit_code = 2
        else:
            logging.info("No HIGH bandit issues")

    elif level == "MEDIUM":
        if sevs & {"HIGH", "MEDIUM"}:
            logging.error("Failing on MEDIUM or HIGH bandit issues")
            exit_code = 2
        else:
            logging.info("No MEDIUM/HIGH bandit issues")

    else:
        logging.warning("Unknown SECURITY_FAIL_LEVEL: %s", level)
        exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
