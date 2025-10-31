
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Union, List, Literal, Dict
import json

# Optional import – only used if the recipe store is available
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

    whitespace: bool
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
        return {
            "whitespace": self.whitespace,
            "delimiters": self.delimiters,
            "include_delim": self.include_delim,
            "pattern": self.pattern,
            "pattern_mode": self.pattern_mode,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RecursiveLevel":
        """Create RecursiveLevel object from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError(f"data must be a dict, got {type(data).__name__}")
        return cls(
            whitespace=data.get("whitespace", False),
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
        if hf_hub_download is None:
            raise ValueError(
                "huggingface_hub is required to load recipes from the recipe store"
            )

        try:
            # The recipe store is a dataset; each recipe is a JSON file under <lang>/<name>.json
            file_path = hf_hub_download(
                repo_id="chonkie-ai/recipes",
                filename=f"{lang}/{name}.json",
                repo_type="dataset",
            )
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as exc:  # pragma: no cover
            raise ValueError(
                f"Could not load recipe '{name}' for language '{lang}': {exc}") from exc

        return cls.from_dict(data)
