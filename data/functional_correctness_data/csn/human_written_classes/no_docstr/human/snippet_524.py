from typing import Any, Callable, Dict, Generic, Optional, Tuple, TypeVar, Union
from bytecode.utils import PY311, PY312, PY313, PY314

class SetLineno:
    __slots__ = ('_lineno',)

    def __init__(self, lineno: int) -> None:
        _check_location(lineno, 'lineno', 0 if PY311 else 1)
        self._lineno: int = lineno

    @property
    def lineno(self) -> int:
        return self._lineno

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SetLineno):
            return False
        return self._lineno == other._lineno