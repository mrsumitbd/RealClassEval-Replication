
import re
from typing import Match


class SelectorPattern:
    def __init__(self, name: str, pattern: str) -> None:
        self._name = name
        self._pattern = pattern

    def get_name(self) -> str:
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        regex = re.compile(self._pattern, flags)
        return regex.match(selector, pos=index)
