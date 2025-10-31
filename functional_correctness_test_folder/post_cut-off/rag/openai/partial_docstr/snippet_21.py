
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPTool":
        """Create a Tool from a dictionary."""
        # Ensure we store a copy to avoid accidental mutation
        return cls(data=dict(data))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        # Return a shallow copy to protect internal state
        return dict(self.data)

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        # Build a minimal schema that includes the most common fields.
        # If a field is missing, provide a sensible default.
        schema: Dict[str, Any] = {
            "name": self.data.get("name", ""),
            "type": self.data.get("type", ""),
            "parameters": self.data.get("parameters", {}),
        }
        # Include any additional keys that are not part of the core schema
        for key, value in self.data.items():
            if key not in schema:
                schema[key] = value
        return schema
