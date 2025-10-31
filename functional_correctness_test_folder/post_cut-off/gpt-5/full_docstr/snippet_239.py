from dataclasses import dataclass
from typing import Optional, Dict, Any


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
    id: Optional[str] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def __post_init__(self):
        if self.name is None or not str(self.name).strip():
            raise ValueError("Tag 'name' is required and cannot be empty")
        self.name = str(self.name).strip()

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
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        '''Create a Tag instance from API response data'''
        if data is None:
            raise ValueError("data cannot be None")
        name = data.get('name')
        if name is None or not str(name).strip():
            raise ValueError("Tag 'name' is required in data")
        return cls(
            name=str(name).strip(),
            id=data.get('id') or data.get('ID') or data.get('tagId'),
            createdAt=data.get('createdAt') or data.get('created_at'),
            updatedAt=data.get('updatedAt') or data.get('updated_at'),
        )
