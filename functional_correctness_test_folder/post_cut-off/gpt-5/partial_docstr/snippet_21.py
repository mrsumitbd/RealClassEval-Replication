from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        name = data.get('name')
        if not isinstance(name, str) or not name:
            raise ValueError("MCPTool requires a non-empty 'name' string")
        description = data.get('description')
        if description is not None and not isinstance(description, str):
            raise TypeError("'description' must be a string if provided")
        input_schema = data.get('input_schema', {})
        if input_schema is None:
            input_schema = {}
        if not isinstance(input_schema, dict):
            raise TypeError("'input_schema' must be a dict")
        return cls(name=name, description=description, input_schema=input_schema)

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            'name': self.name,
            'input_schema': self.input_schema or {},
        }
        if self.description is not None:
            result['description'] = self.description
        return result

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        schema: Dict[str, Any] = {
            'name': self.name,
            'input_schema': self.input_schema or {},
        }
        if self.description is not None:
            schema['description'] = self.description
        return schema
