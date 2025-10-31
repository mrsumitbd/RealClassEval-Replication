
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPResource:
    '''Represents an MCP resource.'''
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
