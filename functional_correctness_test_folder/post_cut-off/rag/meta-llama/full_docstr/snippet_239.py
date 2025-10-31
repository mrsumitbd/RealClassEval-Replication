
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
        data = {k.replace('_', ''): v for k, v in data.items()}
        if self.created_at:
            data['createdAt'] = self.created_at.isoformat()
        if self.updated_at:
            data['updatedAt'] = self.updated_at.isoformat()
        return {k: v for k, v in data.items() if v is not None}

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            created_at=datetime.fromisoformat(
                data['createdAt']) if 'createdAt' in data else None,
            updated_at=datetime.fromisoformat(
                data['updatedAt']) if 'updatedAt' in data else None,
        )
