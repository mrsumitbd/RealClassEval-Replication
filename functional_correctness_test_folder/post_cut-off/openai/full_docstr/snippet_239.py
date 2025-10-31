
from __future__ import annotations

from dataclasses import dataclass, field, asdict
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
    id: Optional[int] = field(default=None)
    createdAt: Optional[str] = field(default=None)
    updatedAt: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tag to a dictionary for API requests.
        Only includes fields that are not None.
        """
        return {k: v for k, v in asdict(self).items() if v is not None}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Tag":
        """
        Create a Tag instance from API response data.
        """
        # Map API keys to dataclass fields
        mapping = {
            "name": "name",
            "id": "id",
            "createdAt": "createdAt",
            "updatedAt": "updatedAt",
        }
        kwargs = {field_name: data.get(api_key)
                  for api_key, field_name in mapping.items()}
        return cls(**kwargs)
