
import re
from typing import Match


class SelectorPattern:

    def __init__(self, name: str, pattern: str) -> None:
        self.name = name
        self.pattern = pattern

    def get_name(self) -> str:
        return self.name

    def match(self, selector: str, index: int, flags: int) -> Match[str] | None:
        return re.match(self.pattern, selector, flags=flags)
