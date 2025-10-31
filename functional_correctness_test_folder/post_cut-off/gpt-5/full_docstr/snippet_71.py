from dataclasses import dataclass
from typing import Any


@dataclass
class HookEvent:
    '''Base class for all hook events.
    Attributes:
        agent: The agent instance that triggered this event.
    '''
    @property
    def should_reverse_callbacks(self) -> bool:
        '''Determine if callbacks for this event should be invoked in reverse order.
        Returns:
            False by default. Override to return True for events that should
            invoke callbacks in reverse order (e.g., cleanup/teardown events).
        '''
        return False

    def _can_write(self, name: str) -> bool:
        '''Check if the given property can be written to.
        Args:
            name: The name of the property to check.
        Returns:
            True if the property can be written to, False otherwise.
        '''
        # Allow writes to internal/private attributes only
        return name.startswith('_')

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        # Allow writes during initialization before freezing, and for internal attrs
        if name == "_frozen" or not getattr(self, "_frozen", False):
            object.__setattr__(self, name, value)
            return
        if self._can_write(name):
            object.__setattr__(self, name, value)
            return
        raise AttributeError(
            f"Cannot set attribute '{name}' on immutable HookEvent instances.")
