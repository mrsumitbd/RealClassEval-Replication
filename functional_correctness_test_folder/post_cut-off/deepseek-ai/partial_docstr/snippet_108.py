
from dataclasses import dataclass, asdict
from typing import Optional, Any, Dict
import json
import requests


@dataclass
class RecursiveLevel:
    def _validate_fields(self) -> None:
        pass

    def __post_init__(self) -> None:
        self._validate_fields()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({json.dumps(self.to_dict(), indent=2)})"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'RecursiveLevel':
        return cls(**data)

    @classmethod
    def from_recipe(cls, name: str, lang: Optional[str] = 'en') -> 'RecursiveLevel':
        url = f"https://some-api.example.com/recipes/{name}?lang={lang}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return cls.from_dict(data)
