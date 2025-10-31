
from dataclasses import dataclass
from typing import List


class Doc:
    def __init__(self, words: List[str]):
        self.words = words


@dataclass
class Sentence:
    start: int = 0
    end: int = 0

    def empty(self) -> bool:
        return self.start >= self.end

    def text(self, doc: Doc) -> str:
        return " ".join(doc.words[self.start:self.end])
