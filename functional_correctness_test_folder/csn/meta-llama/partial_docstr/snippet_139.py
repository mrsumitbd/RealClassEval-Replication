
from typing import Type, Any, Callable


class Field:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


class LazyField:
    def __init__(self, klass: 'Type[Field]') -> None:
        self.klass = klass
        self.args: tuple[Any, ...] = ()
        self.kwargs: dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        self.args = args
        self.kwargs.update(kwargs)
        return self

    def update(self, **kwargs: Any) -> 'LazyField':
        self.kwargs.update(kwargs)
        return self

    def create(self) -> 'Field':
        return self.klass(*self.args, **self.kwargs)
