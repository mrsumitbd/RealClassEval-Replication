from dataclasses import dataclass
from typing import Optional, Dict, Any


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
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tag to a dictionary for API requests"""
        data: Dict[str, Any] = {'name': self.name}
        if self.id is not None:
            data['id'] = self.id
        if self.created_at is not None:
            data['createdAt'] = self.created_at
        if self.updated_at is not None:
            data['updatedAt'] = self.updated_at
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        """Create a Tag instance from API response data"""
        if data is None:
            raise ValueError("data must not be None")
        if 'name' not in data or data['name'] is None:
            raise ValueError("Tag 'name' is required in data")
        return cls(
            name=str(data['name']),
            id=data.get('id'),
            created_at=data.get('createdAt'),
            updated_at=data.get('updatedAt'),
        )
