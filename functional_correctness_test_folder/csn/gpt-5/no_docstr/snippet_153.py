import re
from typing import Match, Pattern


class SelectorPattern:

    def __init__(self, name: str, pattern: str) -> None:
        self._name = name
        self._pattern_str = pattern
        self._compiled_cache: dict[int, Pattern[str]] = {}

    def get_name(self) -> str:
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        if flags not in self._compiled_cache:
            self._compiled_cache[flags] = re.compile(self._pattern_str, flags)
        return self._compiled_cache[flags].match(selector, pos=index)
