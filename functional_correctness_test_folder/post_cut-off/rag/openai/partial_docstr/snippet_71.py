
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:
    """Base class for all hook events.

    Attributes:
        agent: The agent instance that triggered this event.
    """

    agent: Any

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
        # Only the ``agent`` attribute is allowed to be set after initialization.
        # ``_frozen`` is used to prevent further writes once the object is fully
        # constructed.
        return name == "agent" and not getattr(self, "_frozen", False)

    def __post_init__(self) -> None:
        """Disallow writes to non-approved properties."""
        # Mark the instance as frozen so that subsequent attribute assignments
        # are blocked by ``__setattr__``.
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent setting attributes on hook events.

        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        """
        # Allow setting ``agent`` during initialization (when ``_frozen`` is not yet set).
        if name == "agent" and not hasattr(self, "_frozen"):
            object.__setattr__(self, name, value)
            return
        raise AttributeError(
            f"Cannot set attribute '{name}' on HookEvent; "
            "hook events are immutable after creation."
        )
