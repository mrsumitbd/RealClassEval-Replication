from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:

    @property
    def should_reverse_callbacks(self) -> bool:
        '''Determine if callbacks for this event should be invoked in reverse order.
        Returns:
            False by default. Override to return True for events that should
            invoke callbacks in reverse order (e.g., cleanup/teardown events).
        '''
        return False

    def _can_write(self, name: str) -> bool:
        # Allow writes only during initialization (before _frozen is set).
        return not getattr(self, "_frozen", False)

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        if self._can_write(name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                "HookEvent instances are immutable; setting attributes is not allowed.")
