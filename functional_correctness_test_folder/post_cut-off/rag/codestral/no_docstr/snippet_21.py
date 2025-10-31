
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    data: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        '''Create a Tool from a dictionary.'''
        return cls(data)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tool to a dictionary.'''
        return self.data

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        return {
            'tool': self.data
        }
