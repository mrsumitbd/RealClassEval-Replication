
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Tag:
    """
    Represents a tag in the N8n system.
    Attributes:
        name: Tag name (required)
        id: Tag identifier (optional)
        createdAt: Creation timestamp (optional)
        updatedAt: Last update timestamp (optional)
    """
    name: str
    id: Optional[str] = field(default=None)
    createdAt: Optional[str] = field(default=None)
    updatedAt: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tag to a dictionary for API requests.
        Only non-None values are included.
        """
        result: Dict[str, Any] = {"name": self.name}
        if self.id is not None:
            result["id"] = self.id
        if self.createdAt is not None:
            result["createdAt"] = self.createdAt
        if self.updatedAt is not None:
            result["updatedAt"] = self.updatedAt
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        """
        Create a Tag instance from API response data.
        """
        if data is None:
            raise ValueError("data must not be None")
        return cls(
            name=str(data.get("name")),
            id=str(data.get("id")) if data.get("id") is not None else None,
            createdAt=str(data.get("createdAt")) if data.get(
                "createdAt") is not None else None,
            updatedAt=str(data.get("updatedAt")) if data.get(
                "updatedAt") is not None else None,
        )
