from collections.abc import Awaitable, Callable, Collection, Iterable, Iterator, Mapping, MutableMapping
from operator import attrgetter
from typing import IO, TYPE_CHECKING, Any, AnyStr, Generic, NoReturn, Optional, TypeVar, Union, overload

class UnboundLocalProxy:
    """Repr stand-in for an unbound LocalProxy."""

    def __init__(self, local: Any, getter: Callable) -> None:
        self.local = local
        self.name: Optional[str] = None
        if getter.__closure__:
            internal_callable = getter.__closure__[0].cell_contents
            if isinstance(internal_callable, attrgetter):
                self.name = repr(internal_callable).split('(', 1)[1][1:].rsplit(')', 1)[0][:-1]

    def __repr__(self) -> str:
        if self.name:
            return f'LocalProxy({self.local!r}, {self.name!r})'
        return f'LocalProxy({self.local!r})'

    def __rich_repr__(self) -> Iterable[tuple[Any, Any]]:
        """Build a rich repr."""
        yield (None, self.local)
        if self.name:
            yield (None, self.name)