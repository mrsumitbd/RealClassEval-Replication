
from dataclasses import dataclass, field
from typing import Any


@dataclass
class HookEvent:
    # List of attribute names that can be written to (for internal use)
    _allowed_writes: set = field(default_factory=lambda: {
                                 '_allowed_writes'}, init=False, repr=False)

    @property
    def should_reverse_callbacks(self) -> bool:
        '''Determine if callbacks for this event should be invoked in reverse order.
        Returns:
            False by default. Override to return True for events that should
            invoke callbacks in reverse order (e.g., cleanup/teardown events).
        '''
        return False

    def _can_write(self, name: str) -> bool:
        return name in self._allowed_writes

    def __post_init__(self) -> None:
        '''Disallow writes to non-approved properties.'''
        # After initialization, prevent further writes except to _allowed_writes
        pass

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent setting attributes on hook events.
        Raises:
            AttributeError: Always raised to prevent setting attributes on hook events.
        '''
        if self._can_write(name):
            object.__setattr__(self, name, value)
        else:
            raise AttributeError(
                f"Cannot set attribute '{name}' on {self.__class__.__name__} (immutable event object)")
