from typing import Any


class Immutable:
    def __init__(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            object.__setattr__(self, k, v)
        object.__setattr__(self, '_Immutable__frozen', True)

    def __setattr__(self, name: str, value: Any) -> None:
        if getattr(self, '_Immutable__frozen', False):
            raise AttributeError(
                "Immutable instances do not support attribute assignment")
        object.__setattr__(self, name, value)
