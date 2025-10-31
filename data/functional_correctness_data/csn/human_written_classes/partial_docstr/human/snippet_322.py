from typing import Collection, List

class BaseTokenizer:
    """Basic class for a tokenizer function. (codes from `fastai`)"""

    def __init__(self, lang: str):
        self.lang = lang

    def tokenizer(self, t: str) -> List[str]:
        return t.split(' ')

    def add_special_cases(self, toks: Collection[str]):
        pass