
import re
from typing import Match, Optional


class SelectorPattern:

    def __init__(self, name: str, pattern: str) -> None:
        self._name = name
        self._pattern = re.compile(pattern)

    def get_name(self) -> str:
        return self._name

    def match(self, selector: str, index: int, flags: int) -> Optional[Match[str]]:
        return self._pattern.match(selector, index, flags)
