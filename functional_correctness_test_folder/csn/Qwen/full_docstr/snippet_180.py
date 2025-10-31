
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        self.__dict__.update(kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        if hasattr(self, name):
            raise AttributeError(
                f"Cannot modify attribute {name} of immutable instance")
        self.__dict__[name] = value
