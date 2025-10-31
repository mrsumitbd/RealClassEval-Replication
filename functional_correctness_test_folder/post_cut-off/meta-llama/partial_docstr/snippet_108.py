
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class RecursiveLevel:
    name: str
    description: str
    lang: str
    parent: Optional['RecursiveLevel'] = None
    children: list['RecursiveLevel'] = None

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")
        if not isinstance(self.lang, str) or len(self.lang) != 2:
            raise ValueError("Lang must be a 2-character string")
        if self.parent is not None and not isinstance(self.parent, RecursiveLevel):
            raise ValueError("Parent must be a RecursiveLevel or None")
        if self.children is not None and not isinstance(self.children, list):
            raise ValueError("Children must be a list or None")
        if self.children is not None:
            for child in self.children:
                if not isinstance(child, RecursiveLevel):
                    raise ValueError(
                        "All children must be RecursiveLevel instances")

    def __post_init__(self) -> None:
        self._validate_fields()
        if self.children is None:
            self.children = []

    def __repr__(self) -> str:
        return f"RecursiveLevel(name='{self.name}', lang='{self.lang}')"

    def to_dict(self) -> dict:
        data = asdict(self)
        data['parent'] = self.parent.to_dict() if self.parent else None
        data['children'] = [child.to_dict() for child in self.children]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        parent = RecursiveLevel.from_dict(
            data['parent']) if data['parent'] else None
        children = [RecursiveLevel.from_dict(
            child) for child in data['children']]
        return cls(
            name=data['name'],
            description=data['description'],
            lang=data['lang'],
            parent=parent,
            children=children
        )

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        # For demonstration purposes, assume a simple recipe structure
        recipe_data = {
            'name': name,
            'description': f'Description of {name}',
            'lang': lang,
            'parent': None,
            'children': [
                {'name': f'{name}_child1', 'description': f'Description of {name}_child1',
                    'lang': lang, 'parent': None, 'children': []},
                {'name': f'{name}_child2', 'description': f'Description of {name}_child2',
                    'lang': lang, 'parent': None, 'children': []},
            ]
        }
        return cls.from_dict(recipe_data)
