
from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Any, Set


@dataclass
class HookEvent:
    """Base class for all hook events.

    Attributes:
        agent: The agent instance that triggered this event.
    """

    # Sub‑classes will declare their own fields.  The base class does not
    # declare any fields itself.

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
        # The set of allowed attributes is the set of dataclass fields
        # defined on the concrete subclass.
        allowed: Set[str] = {f.name for f in fields(self.__class__)}
        return name in allowed

    def __post_init__(self) -> None:
        """Disallow writes to non‑approved properties."""
        # After initialization, ensure that no unexpected attributes exist.
        allowed: Set[str] = {f.name for f in fields(self.__class__)}
        for name in list(self.__dict__.keys()):
            if name not in allowed:
                raise AttributeError(
                    f"Unexpected attribute '{name}' on {self.__class__.__name__}"
                )

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent setting attributes on hook events.

        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        """
        # Allow setting during initialization for declared fields.
        if self._can_write(name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' on {self.__class__.__name__}"
            )
