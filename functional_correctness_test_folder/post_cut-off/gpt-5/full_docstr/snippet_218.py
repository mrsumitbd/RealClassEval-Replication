from typing import Any


class CBlock:
    '''A `CBlock` is a block of content that can serve as input to or output from an LLM.'''

    def __init__(self, value: str | None, meta: dict[str, Any] | None = None):
        '''Initializes the CBlock with a string and some metadata.'''
        if meta is not None and not isinstance(meta, dict):
            raise TypeError("meta must be a dict[str, Any] or None")
        self._value: str | None = value
        self.meta: dict[str, Any] | None = dict(
            meta) if meta is not None else None

    @property
    def value(self) -> str | None:
        '''Gets the value of the block.'''
        return self._value

    @value.setter
    def value(self, new_value: str | None) -> None:
        '''Sets the value of the block.'''
        self._value = new_value

    def __str__(self):
        '''Stringifies the block.'''
        return "" if self._value is None else str(self._value)

    def __repr__(self):
        '''Provides a python-parsable representation of the block (usually).'''
        return f"CBlock(value={self._value!r}, meta={self.meta!r})"
