
from typing import Any, Optional


class CBlock:

    def __init__(self, value: Optional[str] = None, meta: Optional[dict[str, Any]] = None):
        self._value = value
        self.meta = meta if meta is not None else {}

    @property
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, value: Optional[str]):
        self._value = value

    def __str__(self):
        return f"CBlock(value={self._value}, meta={self.meta})"

    def __repr__(self):
        return f"CBlock(value={self._value!r}, meta={self.meta!r})"
