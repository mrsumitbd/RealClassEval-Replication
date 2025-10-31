
from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        # Temporarily allow setting attributes during initialization
        super().__setattr__('_initialized', False)
        for key, value in kwargs.items():
            super().__setattr__(key, value)
        # Mark the instance as fully initialized
        super().__setattr__('_initialized', True)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        # Allow setting the internal flag during initialization
        if not getattr(self, '_initialized', False) or name == '_initialized':
            super().__setattr__(name, value)
        else:
            raise AttributeError(f"Cannot modify immutable instance: {name}")
