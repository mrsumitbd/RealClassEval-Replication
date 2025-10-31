
from __future__ import annotations
from typing import Any, Tuple


class QuilAtom:
    """Abstract base class for atomic elements of Quil."""

    def out(self) -> str:
        """Return the element as a valid Quil string."""
        raise NotImplementedError("Subclasses must implement `out`.")

    def __str__(self) -> str:
        """Get a string representation of the element, possibly not valid Quil."""
        raise NotImplementedError("Subclasses must implement `__str__`.")

    def __eq__(self, other: object) -> bool:
        """Return True if the other object is equal to this one."""
        if self is other:
            return True
        if not isinstance(other, QuilAtom):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Return a hash of the object."""
        def _make_hashable(value: Any) -> Any:
            if isinstance(value, (list, tuple)):
                return tuple(_make_hashable(v) for v in value)
            if isinstance(value, dict):
                return tuple(sorted((k, _make_hashable(v)) for k, v in value.items()))
            if isinstance(value, set):
                return tuple(sorted(_make_hashable(v) for v in value))
            return value

        items = tuple(sorted((k, _make_hashable(v))
                      for k, v in self.__dict__.items()))
        return hash(items)
