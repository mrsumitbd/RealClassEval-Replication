from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Any


@dataclass
class RecursiveLevel:
    name: str
    lang: str = 'en'
    children: List['RecursiveLevel'] = field(default_factory=list)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(self.lang, str) or not self.lang.strip():
            raise ValueError("lang must be a non-empty string")
        if not isinstance(self.children, list):
            raise ValueError("children must be a list")
        for c in self.children:
            if not isinstance(c, RecursiveLevel):
                raise ValueError(
                    "all children must be RecursiveLevel instances")

    def __post_init__(self) -> None:
        if self.children is None:
            self.children = []
        # Normalize values
        self.name = self.name.strip()
        self.lang = self.lang.strip()
        self._validate_fields()

    def __repr__(self) -> str:
        child_count = len(self.children)
        return f"RecursiveLevel(name={self.name!r}, lang={self.lang!r}, children={child_count} child{'ren' if child_count != 1 else ''})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "lang": self.lang,
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        if not isinstance(data, dict):
            raise ValueError("data must be a dict")
        name = data.get("name")
        lang = data.get("lang", "en")
        raw_children = data.get("children", [])
        if raw_children is None:
            raw_children = []
        if not isinstance(raw_children, list):
            raise ValueError("children must be a list in the input dict")
        children = [cls.from_dict(c) if not isinstance(
            c, RecursiveLevel) else c for c in raw_children]
        return cls(name=name, lang=lang, children=children)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        lang = 'en' if lang is None else lang
        segments = [seg.strip() for seg in name.replace(
            '>', '/').split('/') if seg.strip()]
        if not segments:
            raise ValueError("could not derive segments from name")
        root = cls(name=segments[0], lang=lang, children=[])
        current = root
        for seg in segments[1:]:
            node = cls(name=seg, lang=lang, children=[])
            current.children.append(node)
            current = node
        return root
