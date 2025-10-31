
from dataclasses import dataclass, asdict, fields
from typing import Optional, List


@dataclass
class RecursiveLevel:
    name: str
    description: Optional[str] = None
    sub_levels: Optional[List['RecursiveLevel']] = None

    def _validate_fields(self) -> None:
        if not isinstance(self.name, str):
            raise TypeError("Name must be a string")
        if self.description is not None and not isinstance(self.description, str):
            raise TypeError("Description must be a string or None")
        if self.sub_levels is not None:
            if not isinstance(self.sub_levels, list):
                raise TypeError("Sub levels must be a list or None")
            for sub_level in self.sub_levels:
                if not isinstance(sub_level, RecursiveLevel):
                    raise TypeError(
                        "All sub levels must be RecursiveLevel instances")

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return f"RecursiveLevel(name={self.name}, description={self.description}, sub_levels={self.sub_levels})"

    def to_dict(self) -> dict:
        data = asdict(self)
        if self.sub_levels is not None:
            data['sub_levels'] = [sub_level.to_dict()
                                  for sub_level in self.sub_levels]
        return data

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        if 'sub_levels' in data and data['sub_levels'] is not None:
            data['sub_levels'] = [cls.from_dict(
                sub_level) for sub_level in data['sub_levels']]
        return cls(**data)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        # For demonstration purposes, assume we have a recipe dictionary
        recipe = {
            'en': {
                'level1': {
                    'name': 'Level 1',
                    'description': 'This is level 1',
                    'sub_levels': [
                        {'name': 'Level 1.1', 'description': 'This is level 1.1'},
                        {'name': 'Level 1.2', 'description': 'This is level 1.2'}
                    ]
                }
            }
        }
        if lang not in recipe or name not in recipe[lang]:
            raise ValueError(
                f"Recipe not found for name '{name}' and language '{lang}'")
        return cls.from_dict(recipe[lang][name])
