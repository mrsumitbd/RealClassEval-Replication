from typing import Any, Dict, List, Optional
from dataclasses import dataclass

@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: str
    parameters: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        return cls(name=data.get('name', ''), description=data.get('description', ''), parameters=data.get('parameters', {}))

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        return {'name': self.name, 'description': self.description, 'parameters': self.parameters}

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        return {'type': 'function', 'function': self.to_dict()}