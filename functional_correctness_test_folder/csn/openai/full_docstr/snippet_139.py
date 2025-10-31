
from typing import Any, Type


class LazyField:
    '''A Field that can be later customized until it is binded to the final Model'''

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        '''Instantiate the field type'''
        self.klass = klass
        self.args: tuple[Any, ...] = ()
        self.kwargs: dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        new = LazyField(self.klass)
        new.args = args
        new.kwargs = kwargs
        return new

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        new = LazyField(self.klass)
        new.args = self.args
        new.kwargs = {**self.kwargs, **kwargs}
        return new

    def create(self) -> 'Field[Any, Any]':
        '''Create a normal field from the lazy field'''
        return self.klass(*self.args, **self.kwargs)
