from typing import Match, Optional
import re


class SelectorPattern:
    '''Selector pattern.'''

    def __init__(self, name: str, pattern: str) -> None:
        '''Initialize.'''
        self._name = name
        self._pattern_str = pattern
        self._regex: re.Pattern[str] | None = None
        self._compiled_flags: int | None = None

    def get_name(self) -> str:
        '''Get name.'''
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        '''Match the selector.'''
        if self._regex is None or self._compiled_flags != flags:
            self._regex = re.compile(self._pattern_str, flags)
            self._compiled_flags = flags
        return self._regex.match(selector, pos=index)
