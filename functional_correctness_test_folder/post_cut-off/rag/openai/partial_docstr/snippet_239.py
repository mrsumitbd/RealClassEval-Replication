
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
        updatedAt: Update timestamp (optional)
    """
    name: str
    id: Optional[int] = None
    createdAt: Optional[str] = None
    updatedAt: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tag to a dictionary for API requests.
        Only non‑None fields are included.
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
    def from_dict(cls, data: Optional[Dict[str, Any]]) -> Optional["Tag"]:
        """
        Create a Tag instance from API response data.
        Returns None if data is None.
        """
        if data is None:
            return None
        return cls(
            name=str(data["name"]),
            id=int(
                data["id"]) if "id" in data and data["id"] is not None else None,
            createdAt=str(data["createdAt"]) if "createdAt" in data else None,
            updatedAt=str(data["updatedAt"]) if "updatedAt" in data else None,
        )
