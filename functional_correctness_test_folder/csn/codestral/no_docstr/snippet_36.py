
from dataclasses import dataclass


@dataclass
class Sentence:
    words: list[str]

    def empty(self) -> bool:
        return not self.words

    def text(self, doc: Doc) -> str:
        return ' '.join(self.words)
