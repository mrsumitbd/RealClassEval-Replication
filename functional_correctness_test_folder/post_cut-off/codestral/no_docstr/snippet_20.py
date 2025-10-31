
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MCPResource:

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
