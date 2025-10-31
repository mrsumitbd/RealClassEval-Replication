
from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:
    """
    Base class for hook events.  Instances are immutable after construction.
    """

    @property
    def should_reverse_callbacks(self) -> bool:
        """
        Determine if callbacks for this event should be invoked in reverse order.
        Returns:
            False by default. Override to return True for events that should
            invoke callbacks in reverse order (e.g., cleanup/teardown events).
        """
        return False

    def _can_write(self, name: str) -> bool:
        """
        Return True if the attribute name is a declared dataclass field.
        """
        return name in self.__class__.__dataclass_fields__

    def __post_init__(self) -> None:
        """
        Disallow writes to non-approved properties.
        """
        # Mark the instance as fully initialized so that subsequent
        # attribute assignments are blocked.
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevent setting attributes on hook events after initialization.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        """
        # Allow setting during initialization (i.e., before _initialized is set)
        if not hasattr(self, "_initialized") or not self._initialized:
            if self._can_write(name) or name.startswith("_"):
                object.__setattr__(self, name, value)
            else:
                raise AttributeError(
                    f"Cannot set attribute '{name}' on {self.__class__.__name__}")
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' on {self.__class__.__name__}")
