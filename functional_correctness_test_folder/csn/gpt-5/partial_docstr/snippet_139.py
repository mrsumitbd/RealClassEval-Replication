from typing import Any, Type, Tuple, Dict


class LazyField:
    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        self._klass = klass
        self._args: Tuple[Any, ...] = ()
        self._kwargs: Dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        new = LazyField(self._klass)
        new._args = self._args + args
        merged_kwargs = dict(self._kwargs)
        merged_kwargs.update(kwargs)
        new._kwargs = merged_kwargs
        return new

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        new = LazyField(self._klass)
        new._args = self._args
        merged_kwargs = dict(self._kwargs)
        merged_kwargs.update(kwargs)
        new._kwargs = merged_kwargs
        return new

    def create(self) -> 'Field[Any, Any]':
        return self._klass(*self._args, **self._kwargs)
