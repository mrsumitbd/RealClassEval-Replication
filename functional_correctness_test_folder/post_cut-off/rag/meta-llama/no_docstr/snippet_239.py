
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        data = asdict(self)
        if self.created_at:
            data['createdAt'] = self.created_at.isoformat()
        if self.updated_at:
            data['updatedAt'] = self.updated_at.isoformat()
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        created_at = data.get('createdAt')
        updated_at = data.get('updatedAt')
        return cls(
            id=data.get('id'),
            name=data['name'],
            created_at=datetime.fromisoformat(
                created_at) if created_at else None,
            updated_at=datetime.fromisoformat(
                updated_at) if updated_at else None,
        )
