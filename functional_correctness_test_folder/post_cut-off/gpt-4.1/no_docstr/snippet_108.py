
from dataclasses import dataclass, field
from typing import Optional, List, Any, Dict


@dataclass
class RecursiveLevel:
    name: str
    lang: str = 'en'
    sublevels: Optional[List['RecursiveLevel']] = field(default_factory=list)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("name must be a string")
        if not isinstance(self.lang, str):
            raise TypeError("lang must be a string")
        if self.sublevels is not None:
            if not isinstance(self.sublevels, list):
                raise TypeError("sublevels must be a list or None")
            for sub in self.sublevels:
                if not isinstance(sub, RecursiveLevel):
                    raise TypeError(
                        "All sublevels must be RecursiveLevel instances")

    def __post_init__(self) -> None:
        if self.sublevels is None:
            self.sublevels = []
        self._validate_fields()

    def __repr__(self) -> str:
        return (f"RecursiveLevel(name={self.name!r}, lang={self.lang!r}, "
                f"sublevels={self.sublevels!r})")

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'lang': self.lang,
            'sublevels': [sublevel.to_dict() for sublevel in self.sublevels] if self.sublevels else []
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        name = data.get('name')
        lang = data.get('lang', 'en')
        sublevels_data = data.get('sublevels', [])
        sublevels = [cls.from_dict(sub)
                     for sub in sublevels_data] if sublevels_data else []
        return cls(name=name, lang=lang, sublevels=sublevels)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        # For demonstration, create a dummy recipe with two sublevels
        sub1 = cls(name=f"{name}_sub1", lang=lang)
        sub2 = cls(name=f"{name}_sub2", lang=lang)
        return cls(name=name, lang=lang, sublevels=[sub1, sub2])
