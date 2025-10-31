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
    whitespace: bool
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
        fields = []
        fields.append(f"whitespace={self.whitespace!r}")
        if self.delimiters is not None:
            fields.append(f"delimiters={self.delimiters!r}")
        if self.include_delim is not None:
            fields.append(f"include_delim={self.include_delim!r}")
        if self.pattern is not None:
            fields.append(f"pattern={self.pattern!r}")
        if self.pattern_mode is not None:
            fields.append(f"pattern_mode={self.pattern_mode!r}")
        return f"RecursiveLevel({', '.join(fields)})"

    def to_dict(self) -> dict:
        data = {
            "whitespace": self.whitespace,
        }
        if self.delimiters is not None:
            data["delimiters"] = self.delimiters
        if self.include_delim is not None:
            data["include_delim"] = self.include_delim
        if self.pattern is not None:
            data["pattern"] = self.pattern
        if self.pattern_mode is not None:
            data["pattern_mode"] = self.pattern_mode
        return data

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
        # Try to fetch from HuggingFace dataset
        url = f"https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{lang}/{name}.json"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise ValueError(
                    f"Recipe '{name}' not found for language '{lang}'.")
            data = resp.json()
            # The recipe may be a dict with a "level" or "recursive_level" key, or just the fields
            if "recursive_level" in data:
                level_data = data["recursive_level"]
            elif "level" in data:
                level_data = data["level"]
            else:
                level_data = data
            return cls.from_dict(level_data)
        except Exception as e:
            raise ValueError(
                f"Could not fetch recipe '{name}' for language '{lang}': {e}")
