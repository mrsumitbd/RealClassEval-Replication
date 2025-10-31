
from typing import Any, Dict


class CBlock:
    '''A `CBlock` is a block of content that can serve as input to or output from an LLM.'''

    def __init__(self, value: str | None, meta: Dict[str, Any] | None = None):
        '''Initializes the CBlock with a string and some metadata.'''
        self._value = value
        self.meta = meta or {}

    @property
    def value(self) -> str | None:
        '''Gets the value of the block.'''
        return self._value

    @value.setter
    def value(self, new_value: str | None):
        '''Sets the value of the block.'''
        self._value = new_value

    def __str__(self):
        '''Stringifies the block.'''
        return str(self._value) if self._value is not None else ''

    def __repr__(self):
        '''Provides a python-parsable representation of the block (usually).'''
        return f"{self.__class__.__name__}(value={self._value!r}, meta={self.meta!r})"
