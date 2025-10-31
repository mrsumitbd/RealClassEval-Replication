from dataclasses import dataclass, field
from typing import Any, List
from spacy.tokens import Doc


@dataclass
class Sentence:
    start: int = 0
    end: int = 0
    phrases: List[Any] = field(default_factory=list)

    def empty(self) -> bool:
        '''
Test whether this sentence includes any ranked phrases.
    returns:
`True` if the `phrases` is not empty.
        '''
        return bool(self.phrases)

    def text(self, doc: Doc) -> str:
        s = max(0, min(self.start, len(doc)))
        e = max(s, min(self.end, len(doc)))
        return doc[s:e].text
