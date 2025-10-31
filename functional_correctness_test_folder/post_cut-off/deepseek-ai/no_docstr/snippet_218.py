
class CBlock:

    def __init__(self, value: str | None, meta: dict[str, object] | None = None):
        self._value = value
        self._meta = meta if meta is not None else {}

    @property
    def value(self) -> str | None:
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        self._value = new_value

    def __str__(self) -> str:
        return f"CBlock(value={self._value}, meta={self._meta})"

    def __repr__(self) -> str:
        return f"CBlock(value={self._value!r}, meta={self._meta!r})"
