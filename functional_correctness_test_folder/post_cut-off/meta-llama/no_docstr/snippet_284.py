
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class UpdateFeedModel:
    """Model representing an update feed."""

    def __post_init__(self):
        """Validate the object after initialization."""
        for key, value in self.__dict__.items():
            if value is None:
                raise ValueError(f"Field '{key}' cannot be None")

    def to_dict(self) -> Dict[str, Any]:
        """Convert the object to a dictionary."""
        return asdict(self)
