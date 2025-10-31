from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MCPResource:
    '''Represents an MCP resource.'''
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        if not isinstance(data, dict):
            raise TypeError(
                f"from_dict expects a dict, got {type(data).__name__}")
        return cls(data=dict(data))

    def to_dict(self) -> Dict[str, Any]:
        return dict(self.data)
