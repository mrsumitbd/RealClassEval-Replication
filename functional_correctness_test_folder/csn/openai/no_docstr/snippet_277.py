
from typing import Any


class Immutable:
    def __init__(self, **kwargs: Any) -> None:
        # Set all provided attributes
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
        # Mark the instance as frozen
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting attributes only before the instance is frozen
        if getattr(self, "_frozen", False):
            raise AttributeError(f"Cannot modify immutable instance: {name}")
        object.__setattr__(self, name, value)
