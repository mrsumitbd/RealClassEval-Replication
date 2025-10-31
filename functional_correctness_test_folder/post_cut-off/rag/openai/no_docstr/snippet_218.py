
from __future__ import annotations
from typing import Any, Dict, Optional


class CBlock:
    '''A `CBlock` is a block of content that can serve as input to or output from an LLM.'''

    def __init__(self, value: Optional[str], meta: Optional[Dict[str, Any]] = None):
        '''Initializes the CBlock with a string and some metadata.'''
        self._value: Optional[str] = value
        self._meta: Dict[str, Any] = meta if meta is not None else {}

    @property
    def value(self) -> Optional[str]:
        '''Gets the value of the block.'''
        return self._value

    @value.setter
    def value(self, new_value: Optional[str]) -> None:
        '''Sets the value of the block.'''
        self._value = new_value

    def __str__(self) -> str:
        '''Stringifies the block.'''
        return '' if self._value is None else str(self._value)

    def __repr__(self) -> str:
        '''Provides a python-parsable representation of the block (usually).'''
        return f"{self.__class__.__name__}(value={repr(self._value)}, meta={repr(self._meta)})"
