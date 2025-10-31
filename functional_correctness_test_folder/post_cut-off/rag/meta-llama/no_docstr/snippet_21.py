
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    # Assuming the following fields are part of the MCPTool dataclass
    # If not, replace these with actual fields
    id: str
    name: str
    description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        return asdict(self)

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        # Assuming the tool schema is the same as the dictionary representation
        # If not, modify this method accordingly
        return self.to_dict()
