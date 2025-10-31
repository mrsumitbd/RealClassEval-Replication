
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

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
            "tool_parameters": self.parameters,
            "tool_tags": self.tags
        }
