
from dataclasses import dataclass, field
from typing import List


class Doc:
    # Assuming Doc is a class with a 'text' attribute or a method to get text
    def __init__(self, text):
        self.text = text


@dataclass
class Phrase:
    start: int
    end: int


@dataclass
class Sentence:
    phrases: List[Phrase] = field(default_factory=list)

    def empty(self) -> bool:
        '''
        Test whether this sentence includes any ranked phrases.
        returns:
        `True` if the `phrases` is not empty.
        '''
        return len(self.phrases) == 0

    def text(self, doc: Doc) -> str:
        if not self.phrases:
            return ""

        # Assuming phrases are non-overlapping and sorted by start index
        start = min(phrase.start for phrase in self.phrases)
        end = max(phrase.end for phrase in self.phrases)

        return doc.text[start:end]


# Example usage:
if __name__ == "__main__":
    doc = Doc("This is an example sentence for testing.")
    sentence = Sentence([Phrase(0, 4), Phrase(10, 18)])
    print(sentence.empty())  # False
    print(sentence.text(doc))  # "This is an"
