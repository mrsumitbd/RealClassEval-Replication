from typing import Dict, List
from attacut import Tokenizer

class AttacutTokenizer:

    def __init__(self, model='attacut-sc'):
        self._MODEL_NAME = 'attacut-sc'
        if model == 'attacut-c':
            self._MODEL_NAME = 'attacut-c'
        self._tokenizer = Tokenizer(model=self._MODEL_NAME)

    def tokenize(self, text: str) -> List[str]:
        return self._tokenizer.tokenize(text)