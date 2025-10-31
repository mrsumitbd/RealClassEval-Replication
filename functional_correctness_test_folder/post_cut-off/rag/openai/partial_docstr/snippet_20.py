
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MCPResource:
    """Represents an MCP resource."""
    resource_id: str
    resource_type: str
    resource_name: str
    properties: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPResource":
        """Create a Resource from a dictionary."""
        return cls(
            resource_id=data.get("resource_id", ""),
            resource_type=data.get("resource_type", ""),
            resource_name=data.get("resource_name", ""),
            properties=data.get("properties", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the resource to a dictionary."""
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "resource_name": self.resource_name,
            "properties": self.properties,
        }
