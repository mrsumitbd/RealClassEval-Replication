
from typing import Any, Type


class LazyField:
    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        self._klass = klass
        self._args = ()
        self._kwargs = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        new = LazyField(self._klass)
        new._args = args
        new._kwargs = kwargs.copy()
        return new

    def update(self, **kwargs: Any) -> 'LazyField':
        self._kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        return self._klass(*self._args, **self._kwargs)
