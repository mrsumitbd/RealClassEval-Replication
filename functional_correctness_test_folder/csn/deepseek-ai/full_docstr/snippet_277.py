
class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        '''Initialize.'''
        super().__setattr__('_data', {})
        for key, value in kwargs.items():
            self._data[key] = value

    def __setattr__(self, name: str, value: Any) -> None:
        '''Prevent mutability.'''
        if '_data' not in self.__dict__:
            super().__setattr__(name, value)
        else:
            raise AttributeError("Cannot modify immutable instance")

    def __getattr__(self, name: str) -> Any:
        '''Get attribute.'''
        if name in self._data:
            return self._data[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")
