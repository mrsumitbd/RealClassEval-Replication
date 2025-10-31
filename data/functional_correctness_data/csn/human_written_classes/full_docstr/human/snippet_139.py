from typing import Any, Callable, Dict, Tuple, Type
from inspect import signature

class LazyField:
    """A Field that can be later customized until it is binded to the final Model"""
    counter = 0

    def __init__(self, klass: 'Type[Field[Any, Any]]') -> None:
        """Instantiate the field type"""
        self.klass = klass
        self.kw = {}
        self.args = ()
        self.called = False
        self.counter = self.counter

    def __call__(self, *args: Any, **kwargs: Any) -> 'LazyField':
        """Instantiate a new field with options"""
        assert not self.called
        bound_args = signature(self.klass.__init__).bind(self, *args, **kwargs)
        obj = type(self)(self.klass)
        obj.args = bound_args.args[1:]
        obj.kw = bound_args.kwargs
        setattr(type(self), 'counter', getattr(type(self), 'counter') + 1)
        return obj

    def update(self, **kwargs: Any) -> 'LazyField':
        """Customize the lazy field"""
        assert not self.called
        self.kw.update(kwargs)
        return self

    def create(self) -> 'Field[Any, Any]':
        """Create a normal field from the lazy field"""
        assert not self.called
        return self.klass(*self.args, **self.kw)