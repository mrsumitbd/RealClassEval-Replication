
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Tag:
    """
    Represents a tag in the N8n system.
    Attributes:
        name: Tag name (required)
        id
        createdAt
        updatedAt
    """
    name: str
    id: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        data = {
            'name': self.name,
        }
        if self.id is not None:
            data['id'] = self.id
        if self.createdAt is not None:
            data['createdAt'] = self.createdAt.isoformat()
        if self.updatedAt is not None:
            data['updatedAt'] = self.updatedAt.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(
            name=data['name'],
            id=data.get('id'),
            createdAt=datetime.fromisoformat(
                data['createdAt']) if 'createdAt' in data else None,
            updatedAt=datetime.fromisoformat(
                data['updatedAt']) if 'updatedAt' in data else None,
        )
