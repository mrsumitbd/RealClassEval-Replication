
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Tag:
    '''
    Represents a tag in the N8n system.
    Attributes:
        name: Tag name (required)
        id
        createdAt
        updatedAt
    '''
    name: str
    id: Optional[str] = field(default=None)
    createdAt: Optional[datetime] = field(default=None)
    updatedAt: Optional[datetime] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tag to a dictionary for API requests'''
        result = {
            'name': self.name
        }
        if self.id is not None:
            result['id'] = self.id
        if self.createdAt is not None:
            result['createdAt'] = self.createdAt.isoformat()
        if self.updatedAt is not None:
            result['updatedAt'] = self.updatedAt.isoformat()
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tag':
        '''Create a Tag instance from API response data'''
        return cls(
            name=data['name'],
            id=data.get('id'),
            createdAt=datetime.fromisoformat(
                data['createdAt']) if 'createdAt' in data else None,
            updatedAt=datetime.fromisoformat(
                data['updatedAt']) if 'updatedAt' in data else None
        )
