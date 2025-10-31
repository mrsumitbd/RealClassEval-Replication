from typing import Any, Optional


class CBlock:
    """A `CBlock` is a block of content that can serve as input to or output from an LLM."""

    def __init__(self, value: str | None, meta: dict[str, Any] | None = None):
        """Initializes the CBlock with a string and some metadata."""
        self._value: Optional[str] = None
        self.value = value
        if meta is None:
            self.meta: dict[str, Any] = {}
        elif isinstance(meta, dict):
            self.meta = dict(meta)
        else:
            raise TypeError("meta must be a dict[str, Any] or None")

    @property
    def value(self) -> str | None:
        """Gets the value of the block."""
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        """Sets the value of the block."""
        if new_value is not None and not isinstance(new_value, str):
            raise TypeError("value must be a str or None")
        self._value = new_value

    def __str__(self):
        """Stringifies the block."""
        return self._value or ""

    def __repr__(self):
        """Provides a python-parsable representation of the block (usually)."""
        return f"CBlock(value={self._value!r}, meta={self.meta!r})"
