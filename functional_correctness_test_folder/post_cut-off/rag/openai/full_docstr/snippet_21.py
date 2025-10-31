
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    tool_id: str
    description: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MCPTool":
        """Create a Tool from a dictionary."""
        return cls(
            name=data.get("name", ""),
            tool_id=data.get("tool_id", ""),
            description=data.get("description", ""),
            parameters=data.get("parameters", {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        return {
            "name": self.name,
            "tool_id": self.tool_id,
            "description": self.description,
            "parameters": self.parameters,
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "title": "MCPTool",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "tool_id": {"type": "string"},
                "description": {"type": "string"},
                "parameters": {"type": "object"},
            },
            "required": ["name", "tool_id"],
            "additionalProperties": False,
        }
