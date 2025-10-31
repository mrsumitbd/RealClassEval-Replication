from dataclasses import dataclass
from typing import Optional, Union, Dict, Any


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
    id: Optional[Union[int, str]] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        '''Convert the tag to a dictionary for API requests'''
        data: Dict[str, Any] = {'name': self.name}
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
        if data is None:
            return None
        if isinstance(data, Tag):
            return data
        if not isinstance(data, dict):
            raise TypeError('Tag.from_dict expects a dict')
        if 'name' not in data or data['name'] is None:
            raise ValueError('Tag "name" is required')
        return cls(
            name=str(data['name']),
            id=data.get('id'),
            createdAt=data.get('createdAt'),
            updatedAt=data.get('updatedAt'),
        )
