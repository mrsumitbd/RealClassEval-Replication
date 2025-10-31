from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    """Base class for all hook events.
    Attributes:
        agent: The agent instance that triggered this event.
    """
    agent: Any
    _frozen: bool = field(init=False, default=False, repr=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        """Determine if callbacks for this event should be invoked in reverse order.
        Returns:
            False by default. Override to return True for events that should
            invoke callbacks in reverse order (e.g., cleanup/teardown events).
        """
        return False

    def _can_write(self, name: str) -> bool:
        """Check if the given property can be written to.
        Args:
            name: The name of the property to check.
        Returns:
            True if the property can be written to, False otherwise.
        """
        # Allow writes only during initialization (before frozen).
        return not getattr(self, "_frozen", False)

    def __post_init__(self) -> None:
        """Disallow writes to non-approved properties."""
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        """
        if self._can_write(name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' on immutable HookEvent instances.")
