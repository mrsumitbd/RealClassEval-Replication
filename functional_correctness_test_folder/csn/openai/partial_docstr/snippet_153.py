
import re
from typing import Match


class SelectorPattern:
    '''Selector pattern.'''

    def __init__(self, name: str, pattern: str) -> None:
        '''Initialize.'''
        self._name = name
        self._pattern = pattern

    def get_name(self) -> str:
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        '''Return a regex match object if the pattern matches the selector
        starting at the given index, otherwise None.'''
        regex = re.compile(self._pattern, flags)
        return regex.match(selector, index)
