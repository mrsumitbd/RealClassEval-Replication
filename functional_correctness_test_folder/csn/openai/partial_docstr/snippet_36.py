
from dataclasses import dataclass, field
from typing import Any, List


@dataclass
class Sentence:
    start: int = 0
    end: int = 0
    phrases: List[Any] = field(default_factory=list)

    def empty(self) -> bool:
        """
        Test whether this sentence includes any ranked phrases.
        returns:
            True if the `phrases` is empty.
        """
        return not bool(self.phrases)

    def text(self, doc: Any) -> str:
        """
        Return the raw text of the sentence from the provided document.
        """
        # Assume `doc` has a `text` attribute that is a string.
        return doc.text[self.start: self.end]
