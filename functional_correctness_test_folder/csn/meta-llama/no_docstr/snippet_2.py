
from typing import Iterable


class OcrQualityDictionary:

    def __init__(self, *, wordlist: Iterable[str]):
        self.word_set = set(wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        ocr_words = ocr_text.split()
        matched_words = sum(
            1 for word in ocr_words if word.lower() in self.word_set)
        return matched_words / len(ocr_words) if ocr_words else 0.0
