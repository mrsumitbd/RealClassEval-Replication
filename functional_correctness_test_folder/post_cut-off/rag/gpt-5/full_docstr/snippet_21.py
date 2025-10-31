from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(
        default_factory=lambda: {"type": "object", "properties": {}}
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        name: Optional[str] = None
        description: Optional[str] = None
        schema: Dict[str, Any] = {}

        if isinstance(data.get("function"), dict):
            fn = data["function"]
            name = fn.get("name")
            description = fn.get("description")
            schema = fn.get("parameters") or fn.get("input_schema") or {}
        else:
            name = data.get("name")
            description = data.get("description")
            schema = data.get("input_schema") or data.get("parameters") or {}

        if not name:
            raise ValueError("Tool 'name' is required")

        schema = cls._ensure_schema(schema)
        return cls(name=name, description=description, input_schema=schema)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        out: Dict[str, Any] = {
            "name": self.name,
            "input_schema": self._ensure_schema(self.input_schema),
        }
        if self.description:
            out["description"] = self.description
        return out

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        fn: Dict[str, Any] = {
            "name": self.name,
            "parameters": self._ensure_schema(self.input_schema),
        }
        if self.description:
            fn["description"] = self.description
        return {"type": "function", "function": fn}

    @staticmethod
    def _ensure_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
        s = dict(schema) if schema else {}
        if "type" not in s:
            s["type"] = "object"
        if s.get("type") == "object" and "properties" not in s:
            s["properties"] = {}
        return s
