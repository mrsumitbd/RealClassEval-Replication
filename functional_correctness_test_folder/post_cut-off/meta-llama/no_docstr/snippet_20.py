
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any


@dataclass
class MCPResource:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        valid_keys = {field.name for field in fields(cls)}
        filtered_data = {key: value for key,
                         value in data.items() if key in valid_keys}
        return cls(**filtered_data)
