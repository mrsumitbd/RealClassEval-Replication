
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    '''Base class for all hook events.
    Attributes:
        agent: The agent instance that triggered this event.
    '''
    agent: Any = field(default=None)

    # internal flag to indicate that initialization is complete
    _initialized: bool = field(default=False, init=False, repr=False)

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
        # Allow writing to the agent attribute and any internal attributes
        return name == 'agent' or name.startswith('_')

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        # Mark the instance as fully initialized
        object.__setattr__(self, '_initialized', True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        # Allow setting during initialization or for internal attributes
        if not getattr(self, '_initialized', False) or self._can_write(name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(f"Cannot set attribute '{name}' on HookEvent")
