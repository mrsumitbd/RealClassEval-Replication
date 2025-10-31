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
    id: Optional[Any] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert the tag to a dictionary for API requests"""
        data: Dict[str, Any] = {'name': self.name}
        if self.id is not None:
            data['id'] = self.id
        if self.createdAt is not None:
            data['createdAt'] = self.createdAt
        if self.updatedAt is not None:
            data['updatedAt'] = self.updatedAt
        return data

    @classmethod
    def from_dict(cls, data: Optional[Dict[str, Any]]):
        """Create a Tag instance from API response data"""
        if data is None:
            return None
        if not isinstance(data, dict):
            raise TypeError('data must be a dict')
        name = data.get('name')
        if name is None:
            raise ValueError("Missing required field 'name'")
        created_at = data.get('createdAt', data.get('created_at'))
        updated_at = data.get('updatedAt', data.get('updated_at'))
        return cls(
            name=str(name),
            id=data.get('id'),
            createdAt=created_at,
            updatedAt=updated_at,
        )
