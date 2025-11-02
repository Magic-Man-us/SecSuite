"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator
    from pathlib import Path


@pytest.fixture(autouse=True)
def _reset_logging() -> Generator[None]:
    """Reset logging configuration for each test."""
    logging.basicConfig(level=logging.DEBUG, force=True)
    yield
    logging.shutdown()


@pytest.fixture
def tmp_path_factory_session(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Provide a session-scoped temporary directory."""
    return tmp_path_factory.mktemp("session")


@pytest.fixture
def sample_data() -> dict[str, str | int]:
    """Provide sample data for testing."""
    return {
        "name": "test",
        "value": 42,
        "description": "Sample test data",
    }
