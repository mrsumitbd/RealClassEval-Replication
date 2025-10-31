
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class MCPTool:
    '''Represents an MCP tool.'''
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPTool':
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_tool_schema(self) -> Dict[str, Any]:
        '''Convert the tool to a tool schema.'''
        return self.to_dict()
