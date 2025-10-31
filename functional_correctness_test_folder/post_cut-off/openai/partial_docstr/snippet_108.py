
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Type, TypeVar
import json
import os

T = TypeVar("T", bound="RecursiveLevel")


@dataclass
class RecursiveLevel:
    name: str
    lang: str = "en"
    sublevels: List["RecursiveLevel"] = field(default_factory=list)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.lang, str):
            raise ValueError("lang must be a string")
        if not isinstance(self.sublevels, list):
            raise ValueError("sublevels must be a list")
        for sl in self.sublevels:
            if not isinstance(sl, RecursiveLevel):
                raise ValueError(
                    "sublevels must contain RecursiveLevel instances")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return (
            f"RecursiveLevel(name={self.name!r}, lang={self.lang!r}, "
            f"sublevels={self.sublevels!r})"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "lang": self.lang,
            "sublevels": [sl.to_dict() for sl in self.sublevels],
        }

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        name = data.get("name")
        lang = data.get("lang", "en")
        sublevels_data = data.get("sublevels", [])
        sublevels = [cls.from_dict(sl) for sl in sublevels_data]
        return cls(name=name, lang=lang, sublevels=sublevels)

    @classmethod
    def from_recipe(cls: Type[T], name: str, lang: Optional[str] = "en") -> T:
        filename = f"{name}_{lang}.json"
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"Recipe file {filename} not found")
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls.from_dict(data)
