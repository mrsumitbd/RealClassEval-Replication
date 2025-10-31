
from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    description: str
    version: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
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
        '''Convert the tool to a tool schema.'''
        schema = {
            'tool_name': self.name,
            'tool_description': self.description,
            'tool_version': self.version,
            'tool_parameters': self.parameters
        }
        return schema
