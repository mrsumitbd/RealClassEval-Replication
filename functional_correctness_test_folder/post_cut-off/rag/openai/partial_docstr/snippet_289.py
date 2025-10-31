
from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass
class UpdateRuleDeployment:
    """Model for updating rule deployment."""

    def __post_init__(self) -> None:
        """Post‑initialisation for validating/converting attributes."""
        # No specific attributes to validate in this generic implementation.
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        # Convert the dataclass to a dict and drop any keys with a value of None.
        return {k: v for k, v in asdict(self).items() if v is not None}
