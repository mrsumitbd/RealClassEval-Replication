from dataclasses import dataclass

@dataclass
class Range:
    start: int = 0
    end: int = 0

    @property
    def length(self) -> int:
        return self.end - self.start

    @property
    def is_empty(self) -> bool:
        return self.start == 0 and self.end == 0

    def cut(self, s: str) -> str:
        return s[self.start:self.end]