
class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        super().__setattr__('_data', kwargs)

    def __setattr__(self, name: str, value: Any) -> None:
        raise AttributeError("Cannot modify immutable object")

    def __getattr__(self, name: str) -> Any:
        if name in self._data:
            return self._data[name]
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'")
