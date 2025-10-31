
from typing import Any, Type, Generic


class Field(Generic[Any, Any]):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass


class LazyField:
    '''A Field that can be later customized until it is binded to the final Model'''

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        '''Instantiate the field type'''
        self.klass = klass
        self.options = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        new_options = self.options.copy()
        new_options.update(kwargs)
        new_instance = LazyField(self.klass)
        new_instance.options = new_options
        return new_instance

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        self.options.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        '''Create a normal field from the lazy field'''
        return self.klass(**self.options)
