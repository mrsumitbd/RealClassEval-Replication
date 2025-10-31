from dataclasses import dataclass, fields
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
        # Allow writing only to dataclass fields during __post_init__
        return any(f.name == name for f in fields(self))

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        # After initialization, lock down attribute setting by replacing __setattr__
        object.__setattr__(self, '_locked', True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        # Allow setting during dataclass __init__ and __post_init__
        if not hasattr(self, '_locked') or not getattr(self, '_locked', False):
            object.__setattr__(self, name, value)
        elif self._can_write(name):
            # Allow dataclass machinery to set fields during __init__
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' on immutable HookEvent instance")
