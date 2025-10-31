
import re
from typing import Match, Optional


class SelectorPattern:
    '''Selector pattern.'''

    def __init__(self, name: str, pattern: str) -> None:
        '''Initialize.'''
        self._name = name
        self._pattern_str = pattern
        self._compiled = re.compile(pattern)

    def get_name(self) -> str:
        '''Get name.'''
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Optional[Match[str]]:
        '''Match the selector.'''
        # Compile with the provided flags if any
        compiled = re.compile(self._pattern_str, flags)
        return compiled.match(selector, pos=index)
