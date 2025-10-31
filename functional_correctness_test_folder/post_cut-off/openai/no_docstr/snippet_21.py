
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MCPTool:
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(data=data)

    def to_dict(self) -> Dict[str, Any]:
        return self.data

    def to_tool_schema(self) -> Dict[str, Any]:
        return self.data
