
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Union

try:
    from datasets import load_dataset
except Exception:  # pragma: no cover
    load_dataset = None  # type: ignore


@dataclass
class RecursiveLevel:
    """RecursiveLevels express the chunking rules at a specific level for the recursive chunker.

    Attributes:
        whitespace (bool): Whether to use whitespace as a delimiter.
        delimiters (Optional[Union[str, List[str]]]): Custom delimiters for chunking.
        include_delim (Optional[Literal["prev", "next"]]): Whether to include the delimiter at all, or in the previous chunk, or the next chunk.
        pattern (Optional[str]): Regex pattern for advanced splitting/extraction.
        pattern_mode (Literal["split", "extract"]): Whether to split on pattern matches or extract pattern matches.
    """

    whitespace: bool = False
    delimiters: Optional[Union[str, List[str]]] = None
    include_delim: Optional[Literal["prev", "next"]] = None
    pattern: Optional[str] = None
    pattern_mode: Literal["split", "extract"] = "split"

    def _validate_fields(self) -> None:
        """Validate all fields have legal values."""
        if not isinstance(self.whitespace, bool):
            raise TypeError(
                f"whitespace must be bool, got {type(self.whitespace).__name__}")

        if self.delimiters is not None:
            if isinstance(self.delimiters, str):
                pass
            elif isinstance(self.delimiters, list):
                if not all(isinstance(d, str) for d in self.delimiters):
                    raise TypeError("All delimiters must be strings")
            else:
                raise TypeError(
                    f"delimiters must be str or list of str, got {type(self.delimiters).__name__}"
                )

        if self.include_delim is not None:
            if self.include_delim not in ("prev", "next"):
                raise ValueError(
                    f"include_delim must be 'prev' or 'next', got {self.include_delim}"
                )

        if self.pattern is not None and not isinstance(self.pattern, str):
            raise TypeError(
                f"pattern must be str, got {type(self.pattern).__name__}")

        if self.pattern_mode not in ("split", "extract"):
            raise ValueError(
                f"pattern_mode must be 'split' or 'extract', got {self.pattern_mode}"
            )

    def __post_init__(self) -> None:
        """Validate attributes."""
        self._validate_fields()

    def __repr__(self) -> str:
        """Return a string representation of the RecursiveLevel."""
        return (
            f"RecursiveLevel(whitespace={self.whitespace!r}, "
            f"delimiters={self.delimiters!r}, "
            f"include_delim={self.include_delim!r}, "
            f"pattern={self.pattern!r}, "
            f"pattern_mode={self.pattern_mode!r})"
        )

    def to_dict(self) -> dict:
        """Return the RecursiveLevel as a dictionary."""
        result: Dict[str, Any] = {
            "whitespace": self.whitespace,
            "pattern_mode": self.pattern_mode,
        }
        if self.delimiters is not None:
            result["delimiters"] = self.delimiters
        if self.include_delim is not None:
            result["include_delim"] = self.include_delim
        if self.pattern is not None:
            result["pattern"] = self.pattern
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "RecursiveLevel":
        """Create RecursiveLevel object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict, got {type(data).__name__}")
        # Extract known keys, ignore unknown
        kwargs: Dict[str, Any] = {}
        for key in ("whitespace", "delimiters", "include_delim", "pattern", "pattern_mode"):
            if key in data:
                kwargs[key] = data[key]
        return cls(**kwargs)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = "en") -> "RecursiveLevel":
        """Create RecursiveLevel object from a recipe.

        The recipes are registered in the [Chonkie Recipe Store](https://huggingface.co/datasets/chonkie-ai/recipes). If the recipe is not there, you can create your own recipe and share it with the community!

        Args:
            name (str): The name of the recipe.
            lang (Optional[str]): The language of the recipe.

        Returns:
            RecursiveLevel: The RecursiveLevel object.

        Raises:
            ValueError: If the recipe is not found.
        """
        if load_dataset is None:
            raise RuntimeError("datasets library is required to load recipes")

        # Load the dataset; the dataset is expected to have a 'name' and 'lang' column
        dataset = load_dataset("chonkie-ai/recipes",
                               name="default", split="train")

        # Filter rows matching name and lang
        matches = [
            row
            for row in dataset
            if row.get("name") == name and row.get("lang") == lang
        ]

        if not matches:
            raise ValueError(
                f"Recipe '{name}' with language '{lang}' not found")

        recipe = matches[0]
        # Convert recipe dict to RecursiveLevel
        # The recipe may contain keys that match the dataclass fields
        return cls.from_dict(recipe)
