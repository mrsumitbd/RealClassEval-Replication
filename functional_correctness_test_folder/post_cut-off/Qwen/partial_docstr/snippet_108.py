
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RecursiveLevel:
    name: str
    lang: Optional[str] = 'en'
    levels: Optional['RecursiveLevel'] = None

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if self.lang is not None and not isinstance(self.lang, str):
            raise ValueError("lang must be a string or None")
        if self.levels is not None and not isinstance(self.levels, RecursiveLevel):
            raise ValueError(
                "levels must be a RecursiveLevel instance or None")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return f"RecursiveLevel(name={self.name!r}, lang={self.lang!r}, levels={self.levels!r})"

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'lang': self.lang,
            'levels': self.levels.to_dict() if self.levels else None
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        return cls(
            name=data['name'],
            lang=data.get('lang'),
            levels=cls.from_dict(data['levels']) if data.get(
                'levels') else None
        )

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        return cls(name=name, lang=lang)
