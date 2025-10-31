from typing import Any, Callable, AnyStr

class Immutable:
    """Immutable."""
    __slots__: tuple[Any, ...] = ()

    def __init__(self, **kwargs: Any) -> None:
        """Initialize."""
        for k, v in kwargs.items():
            super().__setattr__(k, v)

    def __setattr__(self, name: str, value: Any) -> None:
        """Prevent mutability."""
        raise AttributeError('Class is immutable!')