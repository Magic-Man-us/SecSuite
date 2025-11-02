"""Tests for the example module."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from secsuite.example import ExampleClass, example

if TYPE_CHECKING:
    from pathlib import Path


class TestExampleClass:
    """Test suite for ExampleClass."""

    def test_creation(self) -> None:
        """Test basic instance creation."""
        obj = ExampleClass(name="test", value=42)
        assert obj.name == "test"
        assert obj.value == 42
        assert obj.tags is None

    def test_creation_with_tags(self) -> None:
        """Test instance creation with tags."""
        obj = ExampleClass(name="test", value=42, tags=["a", "b"])
        assert obj.tags == ["a", "b"]

    def test_empty_name_raises(self) -> None:
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            ExampleClass(name="", value=42)

    def test_negative_value_raises(self) -> None:
        """Test that negative value raises ValueError."""
        with pytest.raises(ValueError, match="value must be non-negative"):
            ExampleClass(name="test", value=-1)

    def test_process(self) -> None:
        """Test the process method."""
        obj = ExampleClass(name="test", value=42)
        result = obj.process()
        assert result["name"] == "test"
        assert result["value"] == 42
        assert result["tag_count"] == 0

    def test_process_with_tags(self) -> None:
        """Test the process method with tags."""
        obj = ExampleClass(name="test", value=42, tags=["a", "b", "c"])
        result = obj.process()
        assert result["tag_count"] == 3

    def test_immutability(self) -> None:
        """Test that the dataclass is frozen."""
        obj = ExampleClass(name="test", value=42)
        with pytest.raises(AttributeError):
            obj.name = "new_name"  # type: ignore[misc]


class TestExampleFunction:
    """Test suite for the example function."""

    def test_basic_processing(self) -> None:
        """Test basic item processing."""
        result = example(["hello", "world"])
        assert result == ["HELLO", "WORLD"]

    def test_empty_list_raises(self) -> None:
        """Test that empty list raises ValueError."""
        with pytest.raises(ValueError, match="items cannot be empty"):
            example([])

    def test_single_item(self) -> None:
        """Test processing a single item."""
        result = example(["test"])
        assert result == ["TEST"]

    def test_output_to_file(self, tmp_path: Path) -> None:
        """Test writing output to a file."""
        output_file = tmp_path / "output.txt"
        result = example(["hello", "world"], output_path=output_file)

        assert result == ["HELLO", "WORLD"]
        assert output_file.exists()

        content = output_file.read_text(encoding="utf-8")
        assert content == "HELLO\nWORLD"

    def test_tuple_input(self) -> None:
        """Test that tuples work as input."""
        result = example(("a", "b", "c"))
        assert result == ["A", "B", "C"]


@pytest.mark.integration
def test_integration_example_class_and_function(tmp_path: Path) -> None:
    """Integration test combining ExampleClass and example function."""
    obj = ExampleClass(name="integration", value=100, tags=["tag1", "tag2"])
    result = obj.process()

    items = [str(result["name"]), "test", "data"]
    output = example(items, output_path=tmp_path / "integration.txt")

    assert len(output) == 3
    assert output[0] == "INTEGRATION"
