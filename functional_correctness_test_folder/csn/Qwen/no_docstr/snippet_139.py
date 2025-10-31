
from typing import Type, Any, Generic, TypeVar

T = TypeVar('T')
U = TypeVar('U')


class Field(Generic[T, U]):
    def __init__(self, **kwargs: Any) -> None:
        self.__dict__.update(kwargs)


class LazyField:

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        self.klass = klass
        self.kwargs = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        self.kwargs.update(kwargs)
        return self

    def update(self, **kwargs: Any) -> 'LazyField':
        self.kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        return self.klass(**self.kwargs)
