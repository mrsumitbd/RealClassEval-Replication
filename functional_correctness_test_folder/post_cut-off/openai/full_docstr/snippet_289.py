
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    """Model for updating rule deployment."""

    def __post_init__(self) -> None:
        """Post initialization for validating/converting attributes."""
        # Placeholder for future validation logic.
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        # Include all public attributes, excluding callables and private ones.
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_") and not callable(value)
        }
