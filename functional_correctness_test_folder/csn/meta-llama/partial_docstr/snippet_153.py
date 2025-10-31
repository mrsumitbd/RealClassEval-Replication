
import re
from typing import Match


class SelectorPattern:
    '''Selector pattern.'''

    def __init__(self, name: str, pattern: str) -> None:
        '''Initialize.'''
        self.name = name
        self.pattern = re.compile(pattern)

    def get_name(self) -> str:
        return self.name

    def match(self, selector: str, index: int, flags: int = 0) -> Match[str] | None:
        return self.pattern.match(selector, index, flags)
