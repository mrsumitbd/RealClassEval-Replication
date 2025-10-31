
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RecursiveLevel:
    name: str = field(default_factory=str)
    level: int = field(default_factory=int)
    children: Dict[str, 'RecursiveLevel'] = field(default_factory=dict)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if not isinstance(self.level, int):
            raise ValueError("level must be an integer")
        if not isinstance(self.children, dict):
            raise ValueError("children must be a dictionary")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return f"RecursiveLevel(name={self.name}, level={self.level}, children={self.children})"

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'level': self.level,
            'children': {k: v.to_dict() for k, v in self.children.items()}
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        name = data.get('name', '')
        level = data.get('level', 0)
        children = {k: cls.from_dict(v)
                    for k, v in data.get('children', {}).items()}
        return cls(name=name, level=level, children=children)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        # Placeholder for actual implementation
        return cls(name=name, level=0, children={})
