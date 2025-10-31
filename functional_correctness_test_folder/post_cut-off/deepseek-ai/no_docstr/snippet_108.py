
from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict
import requests


@dataclass
class RecursiveLevel:
    def _validate_fields(self) -> None:
        pass

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}={v!r}' for k, v in asdict(self).items())})"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        return cls(**data)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={name}"
        response = requests.get(url)
        data = response.json()
        if data.get('meals') is None:
            raise ValueError(f"No recipe found for {name}")
        meal = data['meals'][0]
        return cls.from_dict(meal)
