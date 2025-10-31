from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Sentence:
    start: int = 0
    end: int = 0

    def empty(self) -> bool:
        return self.start >= self.end

    def text(self, doc: 'Doc') -> str:
        if self.empty():
            return ""
        try:
            return doc[self.start:self.end].text
        except Exception:
            return ""
