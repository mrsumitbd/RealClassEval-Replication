
from dataclasses import dataclass
from typing import List


@dataclass
class Sentence:
    phrases: List[str] = None

    def empty(self) -> bool:
        return not self.phrases

    def text(self, doc: 'Doc') -> str:
        if not self.phrases:
            return ""
        return " ".join(self.phrases)
