from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")

        name = data.get("name")
        if not name or not isinstance(name, str):
            raise ValueError("Tool 'name' is required and must be a string")

        description = data.get("description")
        schema = data.get("input_schema") or data.get("schema") or {}
        if not isinstance(schema, dict):
            raise TypeError("input_schema must be a dict")

        schema = dict(schema)
        if "type" not in schema:
            schema["type"] = "object"
        if schema.get("type") == "object" and "properties" not in schema:
            schema["properties"] = {}

        return cls(name=name, description=description, input_schema=schema)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        out: Dict[str, Any] = {
            "name": self.name,
            "input_schema": self.input_schema or {"type": "object", "properties": {}},
        }
        if self.description is not None:
            out["description"] = self.description
        return out

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        return self.to_dict()
