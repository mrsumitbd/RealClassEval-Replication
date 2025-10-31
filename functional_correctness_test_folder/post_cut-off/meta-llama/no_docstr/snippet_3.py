
from dataclasses import dataclass, asdict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Replace 'your_module' with the actual module name
    from your_module import StatusBiography


@dataclass
class StatusBioDTO:
    """Data Transfer Object for StatusBiography model."""

    id: int
    status: str
    biography: str

    @classmethod
    def from_model(cls, model: 'StatusBiography') -> 'StatusBioDTO':
        """Creates a StatusBioDTO instance from a StatusBiography model."""
        return cls(
            id=model.id,
            status=model.status,
            biography=model.biography
        )

    def to_dict(self) -> dict:
        """Converts the StatusBioDTO instance to a dictionary."""
        return asdict(self)
