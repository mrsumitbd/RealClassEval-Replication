
import re
from typing import Match


class SelectorPattern:
    '''Selector pattern.'''

    def __init__(self, name: str, pattern: str) -> None:
        '''Initialize.'''
        self._name = name
        self._pattern = pattern
        self._compiled = re.compile(pattern)

    def get_name(self) -> str:
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        return re.compile(self._pattern, flags).match(selector, index)
