
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Any


@dataclass
class StatusBioDTO:
    """Status biography data transfer object"""

    id: Optional[int] = None
    status: Optional[str] = None
    biography: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_model(cls, model: Any) -> "StatusBioDTO":
        """
        Create DTO from database model

        Args:
            model (StatusBiography): database model object

        Returns:
            StatusBioDTO: data transfer object
        """
        # The model is expected to have attributes that match the DTO fields.
        # If an attribute is missing, it will default to None.
        return cls(
            id=getattr(model, "id", None),
            status=getattr(model, "status", None),
            biography=getattr(model, "biography", None),
            created_at=getattr(model, "created_at", None),
            updated_at=getattr(model, "updated_at", None),
        )

    def to_dict(self) -> dict:
        """
        Convert to dictionary format

        Returns:
            dict: dictionary format data
        """
        # Convert dataclass to dict, formatting datetime objects as ISO strings
        raw = asdict(self)
        for key, value in raw.items():
            if isinstance(value, datetime):
                raw[key] = value.isoformat()
        return raw
