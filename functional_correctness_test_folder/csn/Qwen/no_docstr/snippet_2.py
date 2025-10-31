
from typing import Iterable


class OcrQualityDictionary:

    def __init__(self, *, wordlist: Iterable[str]):
        self.word_set = set(wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        ocr_words = set(ocr_text.split())
        matched_words = self.word_set.intersection(ocr_words)
        return len(matched_words) / len(ocr_words) if ocr_words else 0.0
