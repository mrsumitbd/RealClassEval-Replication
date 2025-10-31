from typing import Any


class Immutable:
    '''Immutable.'''

    def __init__(self, **kwargs: Any) -> None:
        object.__setattr__(self, "_Immutable__frozen", False)
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
        object.__setattr__(self, "_Immutable__frozen", True)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_Immutable__frozen":
            object.__setattr__(self, name, value)
            return
        if getattr(self, "_Immutable__frozen", False):
            raise AttributeError(f"{self.__class__.__name__} is immutable")
        object.__setattr__(self, name, value)
