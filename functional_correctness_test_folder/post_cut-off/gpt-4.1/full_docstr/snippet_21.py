
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    description: Optional[str] = None
    version: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(
            name=data.get('name', ''),
            description=data.get('description'),
            version=data.get('version'),
            parameters=data.get('parameters', {})
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'parameters': self.parameters
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        schema = {
            'type': 'object',
            'properties': {
                'name': {'type': 'string', 'description': 'Tool name'},
                'description': {'type': 'string', 'description': 'Tool description'},
                'version': {'type': 'string', 'description': 'Tool version'},
                'parameters': {'type': 'object', 'description': 'Tool parameters'}
            },
            'required': ['name']
        }
        return schema
