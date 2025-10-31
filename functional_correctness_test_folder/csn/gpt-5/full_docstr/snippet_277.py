from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        object.__setattr__(self, "_Immutable__locked", False)
        for name, value in kwargs.items():
            object.__setattr__(self, name, value)
        object.__setattr__(self, "_Immutable__locked", True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        if getattr(self, "_Immutable__locked", False):
            raise AttributeError(f"{self.__class__.__name__} is immutable")
        object.__setattr__(self, name, value)
