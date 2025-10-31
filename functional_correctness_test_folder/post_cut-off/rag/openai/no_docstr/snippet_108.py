
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal, Dict, Any

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

    whitespace: bool
    delimiters: Optional[Union[str, List[str]]] = None
    include_delim: Optional[Literal["prev", "next"]] = None
    pattern: Optional[str] = None
    pattern_mode: Literal["split", "extract"] = field(default="split")

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
                raise TypeError("delimiters must be str or list of str")

        if self.include_delim is not None:
            if self.include_delim not in ("prev", "next"):
                raise ValueError('include_delim must be "prev" or "next"')

        if self.pattern is not None and not isinstance(self.pattern, str):
            raise TypeError("pattern must be a string")

        if self.pattern_mode not in ("split", "extract"):
            raise ValueError('pattern_mode must be "split" or "extract"')

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

    def to_dict(self) -> Dict[str, Any]:
        """Return the RecursiveLevel as a dictionary."""
        return {
            "whitespace": self.whitespace,
            "delimiters": self.delimiters,
            "include_delim": self.include_delim,
            "pattern": self.pattern,
            "pattern_mode": self.pattern_mode,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecursiveLevel":
        """Create RecursiveLevel object from a dictionary."""
        return cls(
            whitespace=data["whitespace"],
            delimiters=data.get("delimiters"),
            include_delim=data.get("include_delim"),
            pattern=data.get("pattern"),
            pattern_mode=data.get("pattern_mode", "split"),
        )

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
        dataset = load_dataset("chonkie-ai/recipes", name, split="train")

        # Filter by name and language
        matches = [
            row for row in dataset
            if row.get("name") == name and row.get("lang") == lang
        ]

        if not matches:
            raise ValueError(
                f"Recipe '{name}' with language '{lang}' not found")

        # Assume the first match is the desired recipe
        recipe = matches[0]

        # The recipe dict may contain keys that match RecursiveLevel fields
        # Extract only relevant keys
        relevant_keys = {
            "whitespace",
            "delimiters",
            "include_delim",
            "pattern",
            "pattern_mode",
        }
        recipe_data = {k: recipe[k] for k in relevant_keys if k in recipe}

        return cls.from_dict(recipe_data)
