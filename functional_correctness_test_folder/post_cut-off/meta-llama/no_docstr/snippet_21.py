
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPTool:
    """Class representing an MCP Tool."""
    name: str
    description: str
    parameters: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_tool_schema(self) -> Dict[str, Any]:
        tool_schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }
        return tool_schema
