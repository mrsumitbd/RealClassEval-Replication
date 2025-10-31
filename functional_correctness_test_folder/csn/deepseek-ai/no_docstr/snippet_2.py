
from typing import Iterable


class OcrQualityDictionary:

    def __init__(self, *, wordlist: Iterable[str]):
        self.word_set = set(word.lower() for word in wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        words = ocr_text.lower().split()
        if not words:
            return 0.0
        matched = sum(1 for word in words if word in self.word_set)
        return matched / len(words)
