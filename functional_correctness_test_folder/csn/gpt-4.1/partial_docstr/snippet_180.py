
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        object.__setattr__(self, '_initialized', False)
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
        object.__setattr__(self, '_initialized', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, '_initialized', False):
            raise AttributeError(f"Cannot modify immutable instance: '{name}'")
        object.__setattr__(self, name, value)
