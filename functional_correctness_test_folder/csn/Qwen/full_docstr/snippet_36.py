
from dataclasses import dataclass, field
from typing import List, Optional
from spacy.tokens import Doc, Span


@dataclass
class Sentence:
    '''
    A data class representing the distance measure for one sentence.
    '''
    phrases: List[Span] = field(default_factory=list)
    start: int = 0
    end: int = 0

    def empty(self) -> bool:
        '''
        Test whether this sentence includes any ranked phrases.
        returns:
        `True` if the `phrases` is not empty.
        '''
        return not bool(self.phrases)

    def text(self, doc: Doc) -> str:
        '''
        Accessor for the text slice of the `spaCy` [`Doc`](https://spacy.io/api/doc)
        document represented by this sentence.
        doc:
        source document
        returns:
        the sentence text
        '''
        return doc[self.start:self.end].text
