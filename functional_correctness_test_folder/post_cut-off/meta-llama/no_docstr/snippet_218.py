
from typing import Any


class CBlock:

    def __init__(self, value: str | None, meta: dict[str, Any] | None = None):
        self._value = value
        self.meta = meta if meta is not None else {}

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, value: str | None):
        self._value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"CBlock(value={repr(self.value)}, meta={repr(self.meta)})"
