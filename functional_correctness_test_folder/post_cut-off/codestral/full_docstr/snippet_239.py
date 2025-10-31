
from dataclasses import dataclass


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
    id: str = None
    createdAt: str = None
    updatedAt: str = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        return {
            'name': self.name,
            'id': self.id,
            'createdAt': self.createdAt,
            'updatedAt': self.updatedAt
        }

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(
            name=data.get('name'),
            id=data.get('id'),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt')
        )
