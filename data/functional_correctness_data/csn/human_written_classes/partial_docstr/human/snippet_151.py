from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, Iterable, List, NoReturn, Sequence, Set, Sized, Tuple, Type, TypeVar, Union, cast

class Use:
    """
    For more general use cases, you can use the Use class to transform
    the data while it is being validated.
    """

    def __init__(self, callable_: Callable[[Any], Any], error: Union[str, None]=None) -> None:
        if not callable(callable_):
            raise TypeError(f'Expected a callable, not {callable_!r}')
        self._callable: Callable[[Any], Any] = callable_
        self._error: Union[str, None] = error

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._callable!r})'

    def validate(self, data: Any, **kwargs: Any) -> Any:
        try:
            return self._callable(data)
        except SchemaError as x:
            raise SchemaError([None] + x.autos, [self._error.format(data) if self._error else None] + x.errors)
        except BaseException as x:
            f = _callable_str(self._callable)
            raise SchemaError('%s(%r) raised %r' % (f, data, x), self._error.format(data) if self._error else None)