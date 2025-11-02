#!/usr/bin/env python3
"""Download artifacts from the latest successful GitHub Actions run.

Usage:
    export GITHUB_REPOSITORY="owner/repo"  # or pass --repo
    export GITHUB_TOKEN="ghp_..."          # optional, recommended for private repos

    python scripts/download_artifacts.py --workflow ci.yml --output artifacts

This script will:
- Query the Actions API for the latest successful workflow run for the named workflow
- List artifacts attached to that run
- Download and unpack chosen artifact(s) into the output directory

Notes:
- For public repositories you can omit GITHUB_TOKEN but you may hit rate limits.
- Requires Python 3.8+ and only uses the standard library.
"""

from __future__ import annotations

import argparse
import io
import json
import logging
import os
from pathlib import Path
import sys
from typing import Any, cast
import urllib.request
import zipfile

GITHUB_API = "https://api.github.com"


def api_get(url: str, token: str | None = None) -> Any:
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"token {token}")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def download_url(url: str, token: str | None = None) -> bytes:
    req = urllib.request.Request(url, headers={"Accept": "application/octet-stream"})
    if token:
        req.add_header("Authorization", f"token {token}")
    with urllib.request.urlopen(req) as resp:
        return cast("bytes", resp.read())


def latest_successful_run(owner: str, repo: str, workflow: str, token: str | None) -> dict[str, Any] | None:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/actions/workflows/{workflow}/runs?status=success&per_page=5"
    data = api_get(url, token)
    runs = data.get("workflow_runs", [])
    if not runs:
        return None
    return cast("dict[str, Any]", runs[0])


def list_artifacts(owner: str, repo: str, run_id: int, token: str | None) -> list[dict[str, Any]]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts"
    data = api_get(url, token)
    return cast("list[dict[str, Any]]", data.get("artifacts", []))


def download_and_extract(owner: str, repo: str, artifact: dict[str, Any], output_dir: Path, token: str | None) -> None:
    url = artifact["archive_download_url"]
    data = download_url(url, token)
    output_dir.mkdir(parents=True, exist_ok=True)
    # GitHub returns a zip file
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(path=output_dir)


def parse_repo(repo: str) -> tuple[str, str]:
    if "/" not in repo:
        msg = "Repo must be in 'owner/repo' format"
        raise SystemExit(msg)
    owner, r = repo.split("/", 1)
    return owner, r


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="Download artifacts from latest successful GitHub Actions run")
    parser.add_argument("--repo", help="owner/repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--workflow", help="workflow filename (name or id)", default="ci.yml")
    parser.add_argument("--output", help="output directory", default="artifacts")
    parser.add_argument("--list", action="store_true", help="list artifacts and exit")
    parser.add_argument("--download", nargs="*", help="names of artifacts to download (default: all)")
    args = parser.parse_args(argv)

    if not args.repo:
        parser.error("--repo or GITHUB_REPOSITORY environment variable is required")

    token = os.environ.get("GITHUB_TOKEN")
    owner, repo = parse_repo(args.repo)

    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    logging.info("Looking up latest successful run for workflow %s in %s/%s...", args.workflow, owner, repo)
    run = latest_successful_run(owner, repo, args.workflow, token)
    if not run:
        logging.error("No successful recent runs found")
        return 1

    run_id = run["id"]
    logging.info("Found run: id=%s, html_url=%s", run_id, run.get("html_url"))

    artifacts = list_artifacts(owner, repo, run_id, token)
    if not artifacts:
        logging.info("No artifacts found for this run")
        return 0

    logging.info("Artifacts:")
    for a in artifacts:
        logging.info(" - %s (size=%s bytes)", a["name"], a["size_in_bytes"])

    if args.list:
        return 0

    to_download = args.download if args.download else [a["name"] for a in artifacts]

    out_root = Path(args.output)
    for a in artifacts:
        if a["name"] in to_download:
            logging.info("Downloading %s...", a["name"])
            download_and_extract(owner, repo, a, out_root / a["name"], token)
            logging.info("Saved to %s", out_root / a["name"])

    logging.info("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
