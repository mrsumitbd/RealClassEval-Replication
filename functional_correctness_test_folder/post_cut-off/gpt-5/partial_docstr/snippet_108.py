from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class RecursiveLevel:
    name: str
    lang: Optional[str] = "en"
    level: int = 0
    children: List["RecursiveLevel"] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name must be a non-empty string")
        if self.lang is not None and not isinstance(self.lang, str):
            raise TypeError("lang must be a string or None")
        if not isinstance(self.level, int) or self.level < 0:
            raise ValueError("level must be a non-negative integer")
        if not isinstance(self.children, list):
            raise TypeError("children must be a list")
        for c in self.children:
            if not isinstance(c, RecursiveLevel):
                raise TypeError(
                    "all children must be instances of RecursiveLevel")
        if not isinstance(self.meta, dict):
            raise TypeError("meta must be a dictionary")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        child_count = len(self.children)
        child_repr = ""
        if child_count:
            preview = ", ".join(repr(c.name) for c in self.children[:3])
            if child_count > 3:
                preview += f", ... (+{child_count - 3} more)"
            child_repr = f", children=[{preview}]"
        meta_repr = f", meta={self.meta}" if self.meta else ""
        lang_repr = f", lang={self.lang!r}" if self.lang is not None else ""
        return f"RecursiveLevel(name={self.name!r}, level={self.level}{lang_repr}{child_repr}{meta_repr})"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "lang": self.lang,
            "level": self.level,
            "meta": self.meta.copy(),
            "children": [c.to_dict() for c in self.children],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "RecursiveLevel":
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        name = data.get("name")
        lang = data.get("lang", "en")
        level = data.get("level", 0)
        meta = data.get("meta", {})
        raw_children = data.get("children", [])
        children: List[RecursiveLevel] = []
        for rc in raw_children:
            if isinstance(rc, RecursiveLevel):
                children.append(rc)
            elif isinstance(rc, dict):
                children.append(cls.from_dict(rc))
            else:
                raise TypeError(
                    "children must be dicts or RecursiveLevel instances")
        return cls(name=name, lang=lang, level=level, children=children, meta=meta)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = "en") -> "RecursiveLevel":
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        segments = [seg.strip() for seg in name.replace(
            "\\", "/").split("/") if seg.strip()]
        if not segments:
            raise ValueError("recipe name must contain at least one segment")
        root = cls(name=segments[0], lang=lang, level=0)
        current = root
        for idx, seg in enumerate(segments[1:], start=1):
            child = cls(name=seg, lang=lang, level=idx)
            current.children.append(child)
            current = child
        return root
