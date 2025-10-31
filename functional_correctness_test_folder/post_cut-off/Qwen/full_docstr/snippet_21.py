
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    description: str
    parameters: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        '''Create a Tool from a dictionary.'''
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tool to a dictionary.'''
        return asdict(self)

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        return {
            "tool_name": self.name,
            "tool_description": self.description,
            "tool_parameters": self.parameters
        }
