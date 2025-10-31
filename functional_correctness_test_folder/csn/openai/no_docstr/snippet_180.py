
from typing import Any


class Immutable:
    def __init__(self, **kwargs: Any) -> None:
        # Set all provided attributes directly, bypassing __setattr__
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)
        # Mark the instance as frozen
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting the _frozen flag itself
        if name == "_frozen":
            object.__setattr__(self, name, value)
            return

        # If the instance is frozen, disallow any further attribute changes
        if getattr(self, "_frozen", False):
            raise AttributeError(f"Cannot modify immutable instance: {name}")

        # Otherwise, allow setting the attribute
        object.__setattr__(self, name, value)
