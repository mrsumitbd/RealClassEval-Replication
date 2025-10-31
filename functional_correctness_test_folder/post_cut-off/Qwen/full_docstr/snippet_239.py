
from dataclasses import dataclass, field
from typing import Optional
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
    id: Optional[int] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        return {
            'name': self.name,
            'id': self.id,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        }

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(
            name=data.get('name'),
            id=data.get('id'),
            createdAt=datetime.fromisoformat(
                data['createdAt']) if data.get('createdAt') else None,
            updatedAt=datetime.fromisoformat(
                data['updatedAt']) if data.get('updatedAt') else None
        )
