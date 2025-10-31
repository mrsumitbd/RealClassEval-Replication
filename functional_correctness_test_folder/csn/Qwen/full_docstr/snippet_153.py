
import re
from typing import Match


class SelectorPattern:
    '''Selector pattern.'''

    def __init__(self, name: str, pattern: str) -> None:
        '''Initialize.'''
        self.name = name
        self.pattern = pattern
        self.regex = re.compile(pattern)

    def get_name(self) -> str:
        '''Get name.'''
        return self.name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        '''Match the selector.'''
        return self.regex.match(selector, index, flags)
