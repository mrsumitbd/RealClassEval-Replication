
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
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        data = {'name': self.name}
        if self.id is not None:
            data['id'] = self.id
        if self.createdAt is not None:
            data['createdAt'] = self.createdAt
        if self.updatedAt is not None:
            data['updatedAt'] = self.updatedAt
        return data

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(
            name=data.get('name', ''),
            id=data.get('id'),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt')
        )
