
class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        for key, value in kwargs.items():
            object.__setattr__(self, key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        raise AttributeError("Cannot modify immutable object")
