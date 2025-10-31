
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MCPTool:

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_tool_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                key: {"type": "string"} for key in self.__dict__.keys()
            },
            "required": list(self.__dict__.keys())
        }
