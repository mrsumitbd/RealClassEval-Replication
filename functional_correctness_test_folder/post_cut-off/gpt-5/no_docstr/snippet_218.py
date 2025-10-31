from typing import Any


class CBlock:

    def __init__(self, value: str | None, meta: dict[str, Any] | None = None):
        self._value: str | None = value
        self.meta: dict[str, Any] = {} if meta is None else dict(meta)

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        self._value = new_value

    def __str__(self):
        return "" if self._value is None else str(self._value)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self._value!r}, meta={self.meta!r})"
