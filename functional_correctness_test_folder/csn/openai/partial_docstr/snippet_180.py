
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        # Set initial attributes directly, bypassing __setattr__
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
        # Mark the instance as initialized
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting attributes only before initialization
        if getattr(self, "_initialized", False):
            raise AttributeError(f"Cannot modify immutable attribute '{name}'")
        object.__setattr__(self, name, value)
