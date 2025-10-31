
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    # Example field that controls callback reversal
    reverse: bool = False
    # Internal flag set after initialization
    _initialized: bool = field(init=False, default=False, repr=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        """Return True if callbacks should be executed in reverse order."""
        return bool(getattr(self, "reverse", False))

    def _can_write(self, name: str) -> bool:
        """
        Determine whether an attribute can be written to.
        Disallow writing to private attributes after initialization.
        """
        # Allow setting during initialization
        if not getattr(self, "_initialized", False):
            return True
        # Disallow setting private attributes after init
        return not name.startswith("_")

    def __post_init__(self) -> None:
        """Mark the instance as initialized."""
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name: str, value: Any) -> None:
        """Custom attribute setting with write protection."""
        if self._can_write(name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' after initialization")
