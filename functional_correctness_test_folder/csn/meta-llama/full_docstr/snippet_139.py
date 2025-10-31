
from typing import Type, Any


class Field:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.args = args
        self.kwargs = kwargs


class LazyField:
    '''A Field that can be later customized until it is binded to the final Model'''

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        '''Instantiate the field type'''
        self.klass = klass
        self.args: Any = ()
        self.kwargs: Any = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        self.args = args
        self.kwargs = kwargs
        return self

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        self.kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        '''Create a normal field from the lazy field'''
        return self.klass(*self.args, **self.kwargs)
