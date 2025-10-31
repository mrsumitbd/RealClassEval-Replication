
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MCPResource:
    '''Represents an MCP resource.'''
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        """Create an MCPResource instance from a dictionary."""
        return cls(data=data)

    def to_dict(self) -> Dict[str, Any]:
        """Return the underlying dictionary representation."""
        return self.data
