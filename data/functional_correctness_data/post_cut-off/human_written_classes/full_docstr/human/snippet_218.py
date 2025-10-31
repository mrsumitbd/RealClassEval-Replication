from typing import Any, Protocol, runtime_checkable

class CBlock:
    """A `CBlock` is a block of content that can serve as input to or output from an LLM."""

    def __init__(self, value: str | None, meta: dict[str, Any] | None=None):
        """Initializes the CBlock with a string and some metadata."""
        if value is not None and (not isinstance(value, str)):
            raise TypeError('value to a Cblock should always be a string or None')
        self._underlying_value = value
        if meta is None:
            meta = {}
        self._meta = meta

    @property
    def value(self) -> str | None:
        """Gets the value of the block."""
        return self._underlying_value

    @value.setter
    def value(self, v: str):
        """Sets the value of the block."""
        self._underlying_value = v

    def __str__(self):
        """Stringifies the block."""
        return self.value if self.value else ''

    def __repr__(self):
        """Provides a python-parsable representation of the block (usually)."""
        return f'CBlock({self.value}, {self._meta.__repr__()})'