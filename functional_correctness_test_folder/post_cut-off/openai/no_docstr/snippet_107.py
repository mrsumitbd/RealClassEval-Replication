
from dataclasses import dataclass, field
from typing import Any, Dict, Mapping


@dataclass
class Context:
    """
    A simple context container that stores arbitrary key/value pairs.
    """
    data: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        # Ensure that `data` is always a dictionary
        if not isinstance(self.data, Mapping):
            raise TypeError(
                f"data must be a mapping, got {type(self.data).__name__}")
        # Convert to a plain dict to avoid accidental mutation of external mapping
        self.data = dict(self.data)

    def __len__(self) -> int:
        """Return the number of key/value pairs in the context."""
        return len(self.data)

    def __str__(self) -> str:
        """Return a human‑readable string representation of the context."""
        items = ", ".join(f"{k!r}: {v!r}" for k, v in self.data.items())
        return f"Context({{{items}}})"

    def __repr__(self) -> str:
        """Return an unambiguous representation of the context."""
        return f"{self.__class__.__name__}(data={self.data!r})"

    def to_dict(self) -> Dict[str, Any]:
        """Return a shallow copy of the context data as a plain dictionary."""
        return dict(self.data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Context":
        """Create a new Context instance from a dictionary."""
        return cls(data=data)
