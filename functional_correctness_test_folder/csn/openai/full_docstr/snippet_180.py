
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        # Allow setting attributes during initialization
        for key, value in kwargs.items():
            super().__setattr__(key, value)
        # Mark the instance as initialized
        super().__setattr__('_initialized', True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        # Allow setting the _initialized flag during __init__
        if name == '_initialized' or not hasattr(self, '_initialized'):
            super().__setattr__(name, value)
        else:
            raise AttributeError(
                f"Cannot modify immutable instance: attempted to set '{name}'")
