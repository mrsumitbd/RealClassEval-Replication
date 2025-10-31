
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class MCPTool:
    name: str
    description: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    version: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(
            name=data.get('name', ''),
            description=data.get('description', ''),
            parameters=data.get('parameters', {}),
            version=data.get('version')
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters,
            'version': self.version
        }

    def to_tool_schema(self) -> Dict[str, Any]:
        schema = {
            'name': self.name,
            'description': self.description,
            'parameters': self.parameters
        }
        if self.version is not None:
            schema['version'] = self.version
        return schema
