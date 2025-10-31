
from dataclasses import dataclass, field
from typing import List


@dataclass
class Phrase:
    rank: int
    content: str


@dataclass
class Doc:
    sentences: List['Sentence']


@dataclass
class Sentence:
    phrases: List[Phrase] = field(default_factory=list)

    def empty(self) -> bool:
        return not self.phrases

    def text(self, doc: Doc) -> str:
        return ' '.join(phrase.content for phrase in sorted(self.phrases, key=lambda p: p.rank))
