from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class Program:
    '''Represents a program in the database'''
    id: Optional[int] = field(default=None)
    name: Optional[str] = field(default=None)
    description: Optional[str] = field(default=None)
    version: Optional[str] = field(default=None)
    metadata: Optional[Dict[str, Any]] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert to dictionary representation'''
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Program':
        '''Create from dictionary representation'''
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            description=data.get('description'),
            version=data.get('version'),
            metadata=data.get('metadata')
        )
