from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, Union

class _Variable:
    __slots__ = ('name',)

    def __init__(self, name: str) -> None:
        self.name: str = name

    def __eq__(self, other: Any) -> bool:
        if type(self) is not type(other):
            return False
        return self.name == other.name

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return '<%s %r>' % (self.__class__.__name__, self.name)