from typing import Any, Dict, Optional


class CBlock:
    '''A `CBlock` is a block of content that can serve as input to or output from an LLM.'''

    def __init__(self, value: Optional[str] | None, meta: Optional[Dict[str, Any]] | None = None):
        '''Initializes the CBlock with a string and some metadata.'''
        self._value: Optional[str] = value
        self.meta: Dict[str, Any] = dict(meta) if meta is not None else {}

    @property
    def value(self) -> Optional[str] | None:
        return self._value

    @value.setter
    def value(self, value: Optional[str] | None) -> None:
        '''Sets the value of the block.'''
        self._value = value

    def __str__(self):
        '''Stringifies the block.'''
        return self._value if self._value is not None else ""

    def __repr__(self):
        '''Provides a python-parsable representation of the block (usually).'''
        return f"CBlock({repr(self._value)}, {repr(self.meta)})"
