import io
import json
from pathlib import Path
import zipfile

import pytest
from scripts import download_artifacts


class DummyResponse:
    def __init__(self, data: bytes, headers=None):
        self._data = data
        self.headers = headers or {}

    def read(self) -> bytes:  # used by download_url
        return self._data

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def make_zip_bytes(files: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as zf:
        for name, data in files.items():
            zf.writestr(name, data)
    return buf.getvalue()


def test_download_and_extract(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    owner = "owner"
    repo = "repo"
    workflow = "ci.yml"

    # Fake API: latest_successful_run -> run id 1
    runs_payload = {"workflow_runs": [{"id": 1, "html_url": "https://example/1"}]}

    # Fake artifacts list
    artifacts_payload = {"artifacts": [{"id": 11, "name": "test-art", "size_in_bytes": 123, "archive_download_url": "https://example/art.zip"}]}

    # Fake zip content
    zip_bytes = make_zip_bytes({"file.txt": b"hello"})

    def fake_urlopen(req, *args, **kwargs):
        url = req.full_url if hasattr(req, "full_url") else req
        if "workflows" in url and "runs" in url:
            return DummyResponse(json.dumps(runs_payload).encode())
        if "/artifacts" in url:
            return DummyResponse(json.dumps(artifacts_payload).encode())
        if url.endswith("art.zip"):
            return DummyResponse(zip_bytes)
        msg = f"Unexpected URL: {url}"
        raise RuntimeError(msg)

    monkeypatch.setattr(download_artifacts.urllib.request, "urlopen", fake_urlopen)

    out = tmp_path / "out"
    # Exercise main flow: call functions directly
    run = download_artifacts.latest_successful_run(owner, repo, workflow, token=None)
    assert run is not None
    assert run["id"] == 1

    arts = download_artifacts.list_artifacts(owner, repo, run_id=1, token=None)
    assert len(arts) == 1

    # Download and extract
    download_artifacts.download_and_extract(owner, repo, arts[0], out / arts[0]["name"], token=None)
    extracted = (out / arts[0]["name"]) / "file.txt"
    assert extracted.exists()
    assert extracted.read_bytes() == b"hello"
