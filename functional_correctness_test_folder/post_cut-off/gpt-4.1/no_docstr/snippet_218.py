
from typing import Any


class CBlock:

    def __init__(self, value: str | None, meta: dict[str, Any] | None = None):
        self._value = value
        self.meta = meta if meta is not None else {}

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, val: str | None):
        self._value = val

    def __str__(self):
        return str(self._value)

    def __repr__(self):
        return f"CBlock(value={self._value!r}, meta={self.meta!r})"
