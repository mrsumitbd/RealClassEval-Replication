
from dataclasses import dataclass, field
from typing import List
from spacy.tokens import Doc


@dataclass
class Sentence:
    phrases: List[slice] = field(default_factory=list)

    def empty(self) -> bool:
        '''
        Test whether this sentence includes any ranked phrases.
        returns:
        `True` if the `phrases` is not empty.
        '''
        return len(self.phrases) == 0

    def text(self, doc: Doc) -> str:
        return " ".join(doc[phrase].text for phrase in self.phrases)
