
from typing import Any, Dict, Optional


class CBlock:
    def __init__(self, value: Optional[str], meta: Optional[Dict[str, Any]] = None):
        self._value = value
        self.meta = meta or {}

    @property
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, new_value: Optional[str]) -> None:
        if new_value is not None and not isinstance(new_value, str):
            raise TypeError("value must be a string or None")
        self._value = new_value

    def __str__(self) -> str:
        return "" if self._value is None else self._value

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self._value!r}, meta={self.meta!r})"
