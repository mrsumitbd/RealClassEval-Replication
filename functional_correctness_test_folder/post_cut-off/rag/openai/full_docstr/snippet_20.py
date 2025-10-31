
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict
import copy


@dataclass
class MCPResource:
    """Represents an MCP resource."""

    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPResource":
        """Create a Resource from a dictionary."""
        # Make a shallow copy to avoid accidental mutation of the input dict
        return cls(copy.copy(data))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        # Return a copy to prevent external mutation of the internal state
        return copy.copy(self.data)
