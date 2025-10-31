
from dataclasses import dataclass, fields
from typing import Any


@dataclass
class HookEvent:
    '''Base class for all hook events.
    Attributes:
        agent: The agent instance that triggered this event.
    '''
    agent: Any  # Assuming 'agent' is defined elsewhere

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
        return name in [f.name for f in fields(self)]

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        for name, value in self.__dict__.items():
            if not self._can_write(name):
                raise AttributeError(f"Cannot set attribute {name}")

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        if not self._can_write(name):
            raise AttributeError(f"Cannot set attribute {name}")
        super().__setattr__(name, value)
