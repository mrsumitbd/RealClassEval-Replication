
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class RecursiveLevel:
    name: str = field(default_factory=str)
    children: list = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str):
            raise ValueError("name must be a string")
        if not isinstance(self.children, list):
            raise ValueError("children must be a list")
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dictionary")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return f"RecursiveLevel(name={self.name}, children={self.children}, metadata={self.metadata})"

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'children': [child.to_dict() for child in self.children],
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        name = data.get('name', '')
        children = [cls.from_dict(child) for child in data.get('children', [])]
        metadata = data.get('metadata', {})
        return cls(name=name, children=children, metadata=metadata)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        # Placeholder for actual implementation
        # This method should fetch data from a recipe source based on the name and language
        # and then create and return a RecursiveLevel instance
        data = {
            'name': name,
            'children': [],
            'metadata': {'lang': lang}
        }
        return cls.from_dict(data)
