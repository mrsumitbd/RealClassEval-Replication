from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class MCPResource:
    '''Represents an MCP resource.'''
    data: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        '''Create a Resource from a dictionary.'''
        if not isinstance(data, dict):
            raise TypeError("data must be a dictionary")
        return cls(data=dict(data))

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the resource to a dictionary.'''
        return dict(self.data)
