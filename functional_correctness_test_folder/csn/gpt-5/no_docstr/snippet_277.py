from typing import Any


class Immutable:

    def __init__(self, **kwargs: Any) -> None:
        object.__setattr__(self, '_locked', False)
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
        object.__setattr__(self, '_locked', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, '_locked', False):
            raise AttributeError(
                f"{self.__class__.__name__} is immutable; cannot set attribute '{name}'")
        object.__setattr__(self, name, value)
