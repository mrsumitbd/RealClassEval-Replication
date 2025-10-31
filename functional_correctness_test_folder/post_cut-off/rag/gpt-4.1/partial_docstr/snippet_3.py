from dataclasses import dataclass
from typing import Optional


@dataclass
class StatusBioDTO:
    """Status biography data transfer object"""
    id: int
    user_id: int
    bio: Optional[str]
    created_at: str
    updated_at: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        """Create DTO from database model
        Args:
            model (StatusBiography): database model object
        Returns:
            StatusBioDTO: data transfer object
        """
        return cls(
            id=model.id,
            user_id=model.user_id,
            bio=getattr(model, 'bio', None),
            created_at=str(model.created_at),
            updated_at=str(model.updated_at)
        )

    def to_dict(self) -> dict:
        """Convert to dictionary format
        Returns:
            dict: dictionary format data
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bio": self.bio,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
