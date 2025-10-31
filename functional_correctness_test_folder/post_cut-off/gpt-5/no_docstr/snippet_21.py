from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPTool:
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        if not isinstance(data, dict):
            raise TypeError("data must be a dict")
        if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
            raise ValueError("data['name'] must be a non-empty string")
        name = data['name']
        description = data.get('description')
        input_schema = data.get('input_schema') or {}
        if not isinstance(input_schema, dict):
            raise TypeError("input_schema must be a dict if provided")

        # Ensure input_schema has minimal valid structure
        if 'type' not in input_schema:
            input_schema['type'] = 'object'
        if input_schema.get('type') == 'object' and 'properties' not in input_schema:
            input_schema['properties'] = {}

        return cls(name=name, description=description, input_schema=input_schema)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            'name': self.name,
            'input_schema': self.input_schema if self.input_schema else {'type': 'object', 'properties': {}},
        }
        if self.description is not None:
            data['description'] = self.description
        return data

    def to_tool_schema(self) -> Dict[str, Any]:
        schema: Dict[str, Any] = {
            'name': self.name,
            'input_schema': self.input_schema if self.input_schema else {'type': 'object', 'properties': {}},
        }
        if self.description is not None:
            schema['description'] = self.description
        return schema
