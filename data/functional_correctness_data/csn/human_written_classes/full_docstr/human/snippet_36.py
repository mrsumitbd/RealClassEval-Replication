import typing
from spacy.tokens import Doc, Span, Token
from dataclasses import dataclass

@dataclass
class Sentence:
    """
A data class representing the distance measure for one sentence.
    """
    start: int
    end: int
    sent_id: int
    phrases: typing.Set[int]
    distance: float

    def empty(self) -> bool:
        """
Test whether this sentence includes any ranked phrases.

    returns:
`True` if the `phrases` is not empty.
        """
        return len(self.phrases) == 0

    def text(self, doc: Doc) -> str:
        """
Accessor for the text slice of the `spaCy` [`Doc`](https://spacy.io/api/doc)
document represented by this sentence.

    doc:
source document

    returns:
the sentence text
        """
        return doc[self.start:self.end]