from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    version: str
    description: str = ""
    parameters: Dict[str, Any] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        return cls(
            name=data.get("name", ""),
            version=data.get("version", ""),
            description=data.get("description", ""),
            parameters=data.get("parameters", {}) if data.get(
                "parameters") is not None else {}
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "parameters": self.parameters if self.parameters is not None else {}
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        return {
            "type": "object",
            "title": self.name,
            "description": self.description,
            "properties": self.parameters if self.parameters is not None else {},
            "required": list(self.parameters.keys()) if self.parameters else []
        }
