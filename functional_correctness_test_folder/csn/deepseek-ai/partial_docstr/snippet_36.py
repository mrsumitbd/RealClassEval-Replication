
from dataclasses import dataclass
from typing import List, Dict, Optional
from spacy.tokens import Doc


@dataclass
class Sentence:
    phrases: List[Dict]  # Assuming phrases is a list of dictionaries

    def empty(self) -> bool:
        '''
        Test whether this sentence includes any ranked phrases.
        returns:
            `True` if the `phrases` is not empty.
        '''
        return not bool(self.phrases)

    def text(self, doc: Doc) -> str:
        '''
        Returns the text of the sentence from the spaCy Doc object.
        '''
        return doc.text
