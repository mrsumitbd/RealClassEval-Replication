
from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal, Dict, Any, ClassVar
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

    _VALID_INCLUDE_DELIM: ClassVar = ("prev", "next")
    _VALID_PATTERN_MODE: ClassVar = ("split", "extract")

    def _validate_fields(self) -> None:
        if not isinstance(self.whitespace, bool):
            raise ValueError("whitespace must be a boolean.")
        if self.delimiters is not None:
            if not (isinstance(self.delimiters, str) or
                    (isinstance(self.delimiters, list) and all(isinstance(d, str) for d in self.delimiters))):
                raise ValueError(
                    "delimiters must be a string or a list of strings.")
        if self.include_delim is not None:
            if self.include_delim not in self._VALID_INCLUDE_DELIM:
                raise ValueError(
                    f"include_delim must be one of {self._VALID_INCLUDE_DELIM}.")
        if self.pattern is not None:
            if not isinstance(self.pattern, str):
                raise ValueError("pattern must be a string.")
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f"pattern is not a valid regex: {e}")
        if self.pattern_mode is not None:
            if self.pattern_mode not in self._VALID_PATTERN_MODE:
                raise ValueError(
                    f"pattern_mode must be one of {self._VALID_PATTERN_MODE}.")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        attrs = []
        attrs.append(f"whitespace={self.whitespace}")
        if self.delimiters is not None:
            attrs.append(f"delimiters={self.delimiters!r}")
        if self.include_delim is not None:
            attrs.append(f"include_delim={self.include_delim!r}")
        if self.pattern is not None:
            attrs.append(f"pattern={self.pattern!r}")
        if self.pattern_mode is not None:
            attrs.append(f"pattern_mode={self.pattern_mode!r}")
        return f"RecursiveLevel({', '.join(attrs)})"

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
        # Try to fetch from HuggingFace dataset
        url = f"https://huggingface.co/datasets/chonkie-ai/recipes/resolve/main/{lang}/{name}.json"
        try:
            resp = requests.get(url)
            if resp.status_code != 200:
                raise ValueError(
                    f"Recipe '{name}' not found for language '{lang}'.")
            data = resp.json()
            # The recipe may be a list of levels, or a single level
            if isinstance(data, list):
                # Use the first level if multiple
                data = data[0]
            return cls.from_dict(data)
        except Exception as e:
            raise ValueError(
                f"Could not fetch recipe '{name}' for language '{lang}': {e}")
