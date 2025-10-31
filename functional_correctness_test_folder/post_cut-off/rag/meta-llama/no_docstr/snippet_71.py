
from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:
    """Base class for all hook events.

    Attributes:
        agent: The agent instance that triggered this event.

    """
    agent: Any  # Assuming agent is of type Any for this example

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
        return name in self.__dataclass_fields__

    def __post_init__(self) -> None:
        """Disallow writes to non-approved properties."""
        pass  # The actual implementation is in __setattr__

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent setting attributes on hook events.

        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.

        """
        if not self._can_write(name):
            raise AttributeError(
                f"can't set attribute '{name}' on immutable instance of {self.__class__.__name__}")
        super().__setattr__(name, value)
