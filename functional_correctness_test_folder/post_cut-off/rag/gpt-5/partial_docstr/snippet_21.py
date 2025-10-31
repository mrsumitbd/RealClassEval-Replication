from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPTool:
    """Represents an MCP tool."""
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(default_factory=dict)
    output_schema: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        """Create a Tool from a dictionary."""
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')

        name = data.get('name')
        if not name or not isinstance(name, str):
            raise ValueError("field 'name' must be a non-empty string")

        description = data.get('description')

        input_schema = data.get('input_schema', {})
        if not input_schema and 'parameters' in data:
            input_schema = data['parameters']
        if not isinstance(input_schema, dict):
            raise ValueError("field 'input_schema' must be a dict")

        output_schema = data.get('output_schema')
        if output_schema is not None and not isinstance(output_schema, dict):
            raise ValueError(
                "field 'output_schema' must be a dict if provided")

        metadata = data.get('metadata') or {}
        if not isinstance(metadata, dict):
            raise ValueError("field 'metadata' must be a dict")

        return cls(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            metadata=metadata,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tool to a dictionary."""
        result: Dict[str, Any] = {
            'name': self.name,
            'description': self.description,
            'input_schema': self.input_schema or {},
        }
        if self.output_schema is not None:
            result['output_schema'] = self.output_schema
        if self.metadata:
            result['metadata'] = self.metadata
        return result

    def to_tool_schema(self) -> Dict[str, Any]:
        """Convert the tool to a tool schema."""
        return {
            'name': self.name,
            'description': self.description or '',
            'input_schema': self.input_schema or {
                'type': 'object',
                'properties': {},
                'additionalProperties': False,
            },
        }
