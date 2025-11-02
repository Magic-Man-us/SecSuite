"""Example module demonstrating best practices."""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExampleClass:
    """An example class following modern Python best practices.

    Attributes:
        name: The name of the example.
        value: An integer value.
        tags: Optional list of string tags.
    """

    name: str
    value: int
    tags: list[str] | None = None

    def __post_init__(self) -> None:
        """Validate the instance after initialization."""
        if not self.name:
            msg = "name cannot be empty"
            raise ValueError(msg)
        if self.value < 0:
            msg = f"value must be non-negative, got {self.value}"
            raise ValueError(msg)

    def process(self) -> dict[str, str | int]:
        """Process the example and return a result.

        Returns:
            A dictionary containing processed data.

        Examples:
            >>> ex = ExampleClass(name="test", value=42)
            >>> result = ex.process()
            >>> result["name"]
            'test'
        """
        logger.info("Processing example: %s with value %d", self.name, self.value)
        return {
            "name": self.name,
            "value": self.value,
            "tag_count": len(self.tags) if self.tags else 0,
        }


def example(
    items: Sequence[str],
    *,
    output_path: Path | None = None,
) -> list[str]:
    """Process a sequence of items and optionally write to a file.

    Args:
        items: Sequence of string items to process.
        output_path: Optional path to write results to.

    Returns:
        List of processed items in uppercase.

    Raises:
        ValueError: If items is empty.
        OSError: If writing to output_path fails.

    Examples:
        >>> example(["hello", "world"])
        ['HELLO', 'WORLD']
    """
    if not items:
        msg = "items cannot be empty"
        raise ValueError(msg)

    processed = [item.upper() for item in items]
    logger.debug("Processed %d items", len(processed))

    if output_path is not None:
        output_path.write_text("\n".join(processed), encoding="utf-8")
        logger.info("Wrote results to %s", output_path)

    return processed
