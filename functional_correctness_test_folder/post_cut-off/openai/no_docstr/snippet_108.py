
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class RecursiveLevel:
    name: str
    lang: str = "en"
    sublevels: List["RecursiveLevel"] = field(default_factory=list)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str) or not self.name:
            raise ValueError("`name` must be a non‑empty string")
        if not isinstance(self.lang, str):
            raise ValueError("`lang` must be a string")
        if not isinstance(self.sublevels, list):
            raise ValueError("`sublevels` must be a list")
        for idx, sub in enumerate(self.sublevels):
            if not isinstance(sub, RecursiveLevel):
                raise ValueError(
                    f"sublevels[{idx}] is not a RecursiveLevel instance")

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
            "sublevels": [sub.to_dict() for sub in self.sublevels],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecursiveLevel":
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")
        name = data.get("name")
        lang = data.get("lang", "en")
        sublevels_data = data.get("sublevels", [])
        if not isinstance(sublevels_data, list):
            raise ValueError("sublevels must be a list")
        sublevels = [cls.from_dict(sub) for sub in sublevels_data]
        return cls(name=name, lang=lang, sublevels=sublevels)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = "en") -> "RecursiveLevel":
        """
        Create a new RecursiveLevel instance from a recipe name.
        This is a placeholder implementation that simply initializes
        the instance with the given name and language.
        """
        return cls(name=name, lang=lang or "en", sublevels=[])
