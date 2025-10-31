
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        # Set initial attributes directly bypassing __setattr__
        for key, value in kwargs.items():
            super().__setattr__(key, value)
        # Mark the instance as fully initialized
        super().__setattr__('_initialized', True)

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting attributes only before initialization
        if getattr(self, '_initialized', False):
            raise AttributeError(f"Cannot modify immutable instance: {name}")
        super().__setattr__(name, value)
