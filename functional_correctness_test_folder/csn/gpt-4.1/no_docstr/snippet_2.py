
from typing import Iterable


class OcrQualityDictionary:

    def __init__(self, *, wordlist: Iterable[str]):
        self.words = set(word.strip().lower()
                         for word in wordlist if word.strip())

    def measure_words_matched(self, ocr_text: str) -> float:
        import re
        ocr_words = re.findall(r'\b\w+\b', ocr_text.lower())
        if not ocr_words:
            return 0.0
        matched = sum(1 for word in ocr_words if word in self.words)
        return matched / len(ocr_words)
