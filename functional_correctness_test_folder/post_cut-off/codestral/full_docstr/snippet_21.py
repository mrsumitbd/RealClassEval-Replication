
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        '''Create a Tool from a dictionary.'''
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tool to a dictionary.'''
        return self.__dict__

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        return {
            'type': 'function',
            'function': {
                'name': self.__class__.__name__,
                'description': self.__doc__,
                'parameters': self.to_dict()
            }
        }
