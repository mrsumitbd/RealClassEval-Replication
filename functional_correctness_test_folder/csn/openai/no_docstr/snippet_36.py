
from dataclasses import dataclass
from spacy.tokens import Doc


@dataclass
class Sentence:
    """
    Represents a sentence by its start and end token indices in a spaCy Doc.
    """
    start: int
    end: int

    def empty(self) -> bool:
        """
        Returns True if the sentence contains no tokens.
        """
        return self.start == self.end

    def text(self, doc: Doc) -> str:
        """
        Returns the raw text of the sentence from the given spaCy Doc.
        """
        # Ensure indices are within bounds
        if self.start < 0 or self.end > len(doc):
            raise ValueError(
                "Sentence indices are out of bounds for the provided Doc.")
        return doc[self.start: self.end].text
