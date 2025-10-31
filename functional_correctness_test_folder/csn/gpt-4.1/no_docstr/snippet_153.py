
import re
from re import Match


class SelectorPattern:

    def __init__(self, name: str, pattern: str) -> None:
        self._name = name
        self._pattern = pattern
        self._compiled = re.compile(pattern)

    def get_name(self) -> str:
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        if flags != self._compiled.flags:
            compiled = re.compile(self._pattern, flags)
        else:
            compiled = self._compiled
        return compiled.match(selector, index)
