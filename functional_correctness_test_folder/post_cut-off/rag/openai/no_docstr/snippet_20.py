
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MCPResource:
    """Represents an MCP resource."""
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPResource":
        """Create a Resource from a dictionary."""
        # Make a shallow copy to avoid accidental mutation of the input dict
        return cls(data=dict(data))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        # Return a copy to prevent external mutation of the internal state
        return dict(self.data)
