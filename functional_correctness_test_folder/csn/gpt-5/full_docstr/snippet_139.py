from typing import Any, Type, Tuple, Dict


class LazyField:
    '''A Field that can be later customized until it is binded to the final Model'''

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        '''Instantiate the field type'''
        self.klass: 'Type[Field[Any, Any]]' = klass
        self._args: Tuple[Any, ...] = ()
        self._kwargs: Dict[str, Any] = {}

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        '''Instantiate a new field with options'''
        new = LazyField(self.klass)
        # carry over existing options and apply new ones
        new._args = self._args + tuple(args)
        merged = dict(self._kwargs)
        merged.update(kwargs)
        new._kwargs = merged
        return new

    def update(self, **kwargs: Any) -> 'LazyField':
        '''Customize the lazy field'''
        self._kwargs.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        '''Create a normal field from the lazy field'''
        return self.klass(*self._args, **self._kwargs)
