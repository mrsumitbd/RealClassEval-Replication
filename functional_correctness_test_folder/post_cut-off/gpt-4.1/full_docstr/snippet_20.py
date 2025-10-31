
from dataclasses import dataclass, asdict, fields
from typing import Dict, Any


@dataclass
class MCPResource:
    '''Represents an MCP resource.'''

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MCPResource':
        '''Create a Resource from a dictionary.'''
        field_names = {f.name for f in fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        return cls(**filtered_data)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the resource to a dictionary.'''
        return asdict(self)
