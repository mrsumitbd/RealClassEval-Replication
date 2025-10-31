from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        object.__setattr__(self, '_Immutable__locked', False)
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
        object.__setattr__(self, '_Immutable__locked', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == '_Immutable__locked':
            object.__setattr__(self, name, value)
            return
        if getattr(self, '_Immutable__locked', False):
            raise AttributeError(
                f"{self.__class__.__name__} is immutable; cannot set attribute '{name}'")
        object.__setattr__(self, name, value)
