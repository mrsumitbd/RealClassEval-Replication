
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    version: str
    description: str
    parameters: Dict[str, Any]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        '''Create a Tool from a dictionary.'''
        return cls(
            name=data['name'],
            version=data['version'],
            description=data['description'],
            parameters=data.get('parameters', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tool to a dictionary.'''
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'parameters': self.parameters
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        return {
            'name': self.name,
            'version': self.version,
            'description': self.description,
            'parameters': self.parameters
        }
