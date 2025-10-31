from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def _empty_object_schema() -> Dict[str, Any]:
    return {"type": "object", "properties": {}}


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    name: str
    description: Optional[str] = None
    input_schema: Dict[str, Any] = field(default_factory=_empty_object_schema)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        '''Create a Tool from a dictionary.'''
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        if "name" not in data or not isinstance(data["name"], str) or not data["name"]:
            raise ValueError("data must contain a non-empty 'name' string")
        name = data["name"]
        description = data.get("description")
        input_schema = data.get("input_schema")

        if input_schema is None or not isinstance(input_schema, dict):
            input_schema = _empty_object_schema()

        # Ensure at minimum it's an object schema
        if "type" not in input_schema:
            input_schema = {**_empty_object_schema(), **input_schema}

        return cls(name=name, description=description, input_schema=input_schema)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tool to a dictionary.'''
        out: Dict[str, Any] = {
            "name": self.name,
            "input_schema": self.input_schema or _empty_object_schema(),
        }
        if self.description is not None:
            out["description"] = self.description
        return out

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        schema: Dict[str, Any] = {
            "name": self.name,
            "input_schema": self.input_schema or _empty_object_schema(),
        }
        if self.description is not None:
            schema["description"] = self.description
        return schema
