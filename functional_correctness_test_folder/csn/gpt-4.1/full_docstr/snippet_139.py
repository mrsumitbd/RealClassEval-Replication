
from typing import Any, Type, Dict


class LazyField:
    '''A Field that can be later customized until it is binded to the final Model'''

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        '''Instantiate the field type'''
        self._klass = klass
        self._args = ()
        self._kwargs: Dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        new = LazyField(self._klass)
        new._args = args
        new._kwargs = kwargs.copy()
        return new

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        self._kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        '''Create a normal field from the lazy field'''
        return self._klass(*self._args, **self._kwargs)
