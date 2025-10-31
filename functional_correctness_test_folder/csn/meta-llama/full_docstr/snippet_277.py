
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        for key, value in kwargs.items():
            super().__setattr__(key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        if hasattr(self, name):
            raise AttributeError("can't modify immutable instance")
        super().__setattr__(name, value)
