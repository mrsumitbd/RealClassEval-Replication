
from dataclasses import dataclass, field
from typing import List


@dataclass
class Doc:
    sentences: List[str] = field(default_factory=list)


@dataclass
class Sentence:
    content: str = ""

    def empty(self) -> bool:
        return self.content.strip() == ""

    def text(self, doc: Doc) -> str:
        return self.content if self.content in doc.sentences else ""
