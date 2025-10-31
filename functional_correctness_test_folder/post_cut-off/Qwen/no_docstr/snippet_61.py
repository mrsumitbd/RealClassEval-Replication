
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class Program:
    name: str
    version: str
    author: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        return cls(**data)
