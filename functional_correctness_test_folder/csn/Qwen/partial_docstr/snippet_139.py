
from typing import Type, Any, Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Field(Generic[T, U]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


class LazyField:

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        self.klass = klass
        self.options = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        self.options.update(kwargs)
        return self

    def update(self, **kwargs: Any) -> 'LazyField':
        self.options.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        return self.klass(**self.options)
