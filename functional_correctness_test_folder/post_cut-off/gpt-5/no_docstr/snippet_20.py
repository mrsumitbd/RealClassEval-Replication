from dataclasses import dataclass
from typing import Any, Dict
from copy import deepcopy


@dataclass
class MCPResource:
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        return cls(deepcopy(data))

    def to_dict(self) -> Dict[str, Any]:
        return deepcopy(self.data)
