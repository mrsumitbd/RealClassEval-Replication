
from dataclasses import dataclass, asdict, fields
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
    id: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    def to_dict(self):
        '''Convert the tag to a dictionary for API requests'''
        data = asdict(self)
        # Remove None values to avoid sending unnecessary data
        data = {k: v for k, v in data.items() if v is not None}
        # Convert datetime objects to ISO format strings
        for k, v in data.items():
            if isinstance(v, datetime):
                data[k] = v.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        '''Create a Tag instance from API response data'''
        # Filter data to only include valid attributes
        valid_fields = [f.name for f in fields(cls)]
        data = {k: v for k, v in data.items() if k in valid_fields}
        # Convert datetime strings to datetime objects
        for k, v in data.items():
            if k in ['createdAt', 'updatedAt'] and isinstance(v, str):
                data[k] = datetime.fromisoformat(v.replace('Z', '+00:00'))
        return cls(**data)
