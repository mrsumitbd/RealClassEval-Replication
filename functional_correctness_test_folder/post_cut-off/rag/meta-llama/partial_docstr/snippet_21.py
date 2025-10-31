
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    # Assuming the class has some attributes, for example:
    tool_id: str
    tool_name: str
    # Add other attributes as necessary

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        return asdict(self)

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        # Assuming the tool schema is similar to the dictionary representation
        # Modify as necessary to fit the actual tool schema
        tool_schema = self.to_dict()
        # Add or modify fields according to the tool schema requirements
        return tool_schema
