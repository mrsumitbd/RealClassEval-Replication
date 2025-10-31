
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Program:

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        return cls(**data)
