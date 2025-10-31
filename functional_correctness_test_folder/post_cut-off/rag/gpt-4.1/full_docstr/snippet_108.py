from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal, Dict, Any
import re
import requests


@dataclass
class RecursiveLevel:
    '''RecursiveLevels express the chunking rules at a specific level for the recursive chunker.
    Attributes:
        whitespace (bool): Whether to use whitespace as a delimiter.
        delimiters (Optional[Union[str, List[str]]]): Custom delimiters for chunking.
        include_delim (Optional[Literal["prev", "next"]]): Whether to include the delimiter at all, or in the previous chunk, or the next chunk.
        pattern (Optional[str]): Regex pattern for advanced splitting/extraction.
        pattern_mode (Literal["split", "extract"]): Whether to split on pattern matches or extract pattern matches.
    '''
    whitespace: bool = False
    delimiters: Optional[Union[str, List[str]]] = None
    include_delim: Optional[Literal["prev", "next"]] = None
    pattern: Optional[str] = None
    pattern_mode: Optional[Literal["split", "extract"]] = None

    def _validate_fields(self) -> None:
        if not isinstance(self.whitespace, bool):
            raise ValueError("whitespace must be a boolean")
        if self.delimiters is not None:
            if not (isinstance(self.delimiters, str) or (isinstance(self.delimiters, list) and all(isinstance(d, str) for d in self.delimiters))):
                raise ValueError(
                    "delimiters must be a string or a list of strings")
        if self.include_delim is not None:
            if self.include_delim not in ("prev", "next"):
                raise ValueError("include_delim must be 'prev' or 'next'")
        if self.pattern is not None:
            try:
                re.compile(self.pattern)
            except Exception as e:
                raise ValueError(f"pattern is not a valid regex: {e}")
        if self.pattern_mode is not None:
            if self.pattern_mode not in ("split", "extract"):
                raise ValueError("pattern_mode must be 'split' or 'extract'")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return (
            f"RecursiveLevel(whitespace={self.whitespace}, "
            f"delimiters={self.delimiters!r}, "
            f"include_delim={self.include_delim!r}, "
            f"pattern={self.pattern!r}, "
            f"pattern_mode={self.pattern_mode!r})"
        )

    def to_dict(self) -> dict:
        return {
            "whitespace": self.whitespace,
            "delimiters": self.delimiters,
            "include_delim": self.include_delim,
            "pattern": self.pattern,
            "pattern_mode": self.pattern_mode,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        return cls(
            whitespace=data.get("whitespace", False),
            delimiters=data.get("delimiters"),
            include_delim=data.get("include_delim"),
            pattern=data.get("pattern"),
            pattern_mode=data.get("pattern_mode"),
        )

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        # Try to fetch from HuggingFace Chonkie Recipe Store
        url = f"https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{lang}/{name}.json"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise ValueError(
                    f"Recipe '{name}' not found for language '{lang}'.")
            data = resp.json()
            # The recipe may be a list of levels, or a dict for a single level
            if isinstance(data, list):
                # Take the first level if multiple
                data = data[0]
            return cls.from_dict(data)
        except Exception as e:
            raise ValueError(
                f"Could not load recipe '{name}' for language '{lang}': {e}")
