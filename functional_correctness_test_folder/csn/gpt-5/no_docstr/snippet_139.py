from typing import Any, Dict, Tuple, Type


class LazyField:

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        self._klass = klass
        self._args: Tuple[Any, ...] = ()
        self._kwargs: Dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        self._args = args
        self._kwargs = dict(kwargs)
        return self

    def update(self, **kwargs: Any) -> 'LazyField':
        self._kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        return self._klass(*self._args, **self._kwargs)
