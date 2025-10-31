from dataclasses import dataclass, field
from typing import Optional, Union, List, Literal, Dict, Tuple
import re


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
    pattern_mode: Literal["split", "extract"] = "split"

    def _validate_fields(self) -> None:
        if not isinstance(self.whitespace, bool):
            raise TypeError("whitespace must be a bool")

        if self.delimiters is not None:
            if isinstance(self.delimiters, str):
                if not self.delimiters:
                    raise ValueError("delimiters string cannot be empty")
            elif isinstance(self.delimiters, list):
                if not self.delimiters:
                    raise ValueError("delimiters list cannot be empty")
                if not all(isinstance(d, str) and d for d in self.delimiters):
                    raise TypeError("all delimiters must be non-empty strings")
            else:
                raise TypeError(
                    "delimiters must be a string or a list of strings")

        if self.include_delim is not None and self.include_delim not in ("prev", "next"):
            raise ValueError(
                'include_delim must be one of: None, "prev", "next"')

        if self.pattern is not None:
            if not isinstance(self.pattern, str) or not self.pattern:
                raise ValueError("pattern must be a non-empty string")
            try:
                re.compile(self.pattern)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern: {e}") from e

        if self.pattern_mode not in ("split", "extract"):
            raise ValueError('pattern_mode must be "split" or "extract"')

        if self.pattern_mode == "extract" and self.pattern is None:
            raise ValueError(
                'pattern_mode "extract" requires a non-empty pattern')

        specified = sum([
            bool(self.whitespace),
            self.delimiters is not None,
            self.pattern is not None
        ])
        if specified == 0:
            raise ValueError(
                "At least one of whitespace, delimiters, or pattern must be specified")
        if specified > 1:
            raise ValueError(
                "Only one of whitespace, delimiters, or pattern can be specified at a time")

        if self.include_delim is not None:
            if self.delimiters is None and not (self.pattern is not None and self.pattern_mode == "split"):
                raise ValueError(
                    "include_delim is only applicable when using delimiters or pattern with pattern_mode='split'")

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
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        return cls(
            whitespace=bool(data.get("whitespace", False)),
            delimiters=data.get("delimiters"),
            include_delim=data.get("include_delim"),
            pattern=data.get("pattern"),
            pattern_mode=data.get("pattern_mode", "split"),
        )

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if lang is not None and not isinstance(lang, str):
            raise TypeError("lang must be a string or None")

        key: Tuple[str, Optional[str]] = (
            name.lower().strip(), (lang or 'en').lower().strip())

        recipes: Dict[Tuple[str, Optional[str]], Dict] = {
            ("whitespace", "en"): {"whitespace": True},
            ("paragraph", "en"): {"pattern": r"(?:\r?\n){2,}", "pattern_mode": "split"},
            ("sentence", "en"): {"pattern": r"(?<=[.!?])\s+", "pattern_mode": "split", "include_delim": "prev"},
            ("line", "en"): {"delimiters": "\n", "include_delim": "prev"},
            ("codeblock", "en"): {"pattern": r"```.*?\n.*?\n```", "pattern_mode": "extract"},
            ("whitespace", "es"): {"whitespace": True},
            ("sentence", "es"): {"pattern": r"(?<=[.!?¡¿])\s+", "pattern_mode": "split", "include_delim": "prev"},
            ("paragraph", "es"): {"pattern": r"(?:\r?\n){2,}", "pattern_mode": "split"},
        }

        if key not in recipes:
            # Fallback to language-agnostic variants if available
            fallback_key = (name.lower().strip(), "en")
            if fallback_key in recipes:
                key = fallback_key
            else:
                raise ValueError(
                    f"Recipe '{name}' with lang '{lang}' not found")

        return cls.from_dict(recipes[key])
