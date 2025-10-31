
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class InputInterval:
    """Input interval values to query."""
    time_window: str = None
    relative_time: str = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create from a dictionary."""
        return cls(**data)

    def __post_init__(self):
        """Validate that only one of `time_window` or `relative_time` is set."""
        if (self.time_window is not None) == (self.relative_time is not None):
            raise ValueError(
                "Exactly one of 'time_window' or 'relative_time' must be set")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a dictionary."""
        return asdict(self)
