
from dataclasses import dataclass
from typing import List, Optional
from spacy.tokens import Doc


@dataclass
class Sentence:
    start: int
    end: int

    def empty(self) -> bool:
        return self.start == self.end

    def text(self, doc: Doc) -> str:
        return doc[self.start:self.end].text
