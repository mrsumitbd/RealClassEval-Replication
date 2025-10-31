
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPTool:

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_tool_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {field: {"type": type(value).__name__} for field, value in self.to_dict().items()},
            "required": list(self.to_dict().keys())
        }
