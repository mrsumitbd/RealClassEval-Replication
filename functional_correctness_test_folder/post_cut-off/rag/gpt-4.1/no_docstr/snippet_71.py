from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    '''Base class for all hook events.
    Attributes:
        agent: The agent instance that triggered this event.
    '''
    agent: Any = field(default=None)

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
        # Allow writing only during __init__ for dataclass fields
        return name in self.__dataclass_fields__

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        # After initialization, prevent further attribute setting except for dataclass internals
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        # Allow setting during __init__ (before _frozen is set)
        if not hasattr(self, "_frozen") or (not getattr(self, "_frozen", False)):
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' on immutable HookEvent instance.")
