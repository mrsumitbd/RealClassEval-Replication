from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MCPResource:
    """Represents an MCP resource."""
    id: str
    name: str
    type: str
    attributes: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        """Create a Resource from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=data.get("type", ""),
            attributes=data.get(
                "attributes", {}) if "attributes" in data else {}
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "attributes": self.attributes
        }
