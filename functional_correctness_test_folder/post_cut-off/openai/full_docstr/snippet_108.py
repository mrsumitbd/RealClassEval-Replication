
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal, Dict, Any
import json

try:
    from huggingface_hub import hf_hub_download
except Exception:  # pragma: no cover
    hf_hub_download = None  # type: ignore


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

    whitespace: bool = field(default=False)
    delimiters: Optional[Union[str, List[str]]] = field(default=None)
    include_delim: Optional[Literal["prev", "next"]] = field(default=None)
    pattern: Optional[str] = field(default=None)
    pattern_mode: Literal["split", "extract"] = field(default="split")

    def _validate_fields(self) -> None:
        """Validate all fields have legal values."""
        if not isinstance(self.whitespace, bool):
            raise TypeError(
                f"whitespace must be bool, got {type(self.whitespace).__name__}")

        if self.delimiters is not None:
            if isinstance(self.delimiters, str):
                # keep as string; will be converted to list in __post_init__
                pass
            elif isinstance(self.delimiters, list):
                if not all(isinstance(d, str) for d in self.delimiters):
                    raise TypeError("All delimiters must be strings")
            else:
                raise TypeError("delimiters must be str, list of str, or None")

        if self.include_delim is not None and self.include_delim not in ("prev", "next"):
            raise ValueError('include_delim must be "prev", "next", or None')

        if self.pattern is not None and not isinstance(self.pattern, str):
            raise TypeError("pattern must be a string or None")

        if self.pattern_mode not in ("split", "extract"):
            raise ValueError('pattern_mode must be "split" or "extract"')

    def __post_init__(self) -> None:
        """Validate attributes."""
        # Normalize delimiters to list if string
        if isinstance(self.delimiters, str):
            self.delimiters = [self.delimiters]
        self._validate_fields()

    def __repr__(self) -> str:
        """Return a string representation of the RecursiveLevel."""
        return (
            f"RecursiveLevel(whitespace={self.whitespace}, "
            f"delimiters={self.delimiters}, "
            f"include_delim={self.include_delim}, "
            f"pattern={self.pattern}, "
            f"pattern_mode={self.pattern_mode})"
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
        return cls(**data)

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
        if hf_hub_download is None:
            raise RuntimeError("huggingface_hub is required to load recipes")

        try:
            path = hf_hub_download(
                repo_id="chonkie-ai/recipes",
                filename=f"{lang}/{name}.json",
                repo_type="dataset",
            )
        except Exception as exc:  # pragma: no cover
            raise ValueError(
                f"Recipe '{name}' not found for language '{lang}'") from exc

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls.from_dict(data)
