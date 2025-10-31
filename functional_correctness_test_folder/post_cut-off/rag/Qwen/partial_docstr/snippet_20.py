
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any


@dataclass
class MCPResource:
    '''Represents an MCP resource.'''
    resource_id: str
    resource_type: str
    resource_name: str
    resource_description: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        '''Create a Resource from a dictionary.'''
        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the resource to a dictionary.'''
        return asdict(self)
