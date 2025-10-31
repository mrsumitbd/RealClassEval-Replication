
import re
from typing import Iterable, Set


class OcrQualityDictionary:
    def __init__(self, *, wordlist: Iterable[str]):
        # Store the dictionary words in a set for fast lookup, normalised to lowercase
        self._dict_set: Set[str] = {word.lower() for word in wordlist}

    def measure_words_matched(self, ocr_text: str) -> float:
        """
        Return the fraction of words in `ocr_text` that are present in the dictionary.
        Words are extracted using a simple word boundary regex and compared case‑insensitively.
        If the input contains no words, 0.0 is returned.
        """
        # Extract words (alphanumeric sequences) from the OCR text
        words = re.findall(r"\b\w+\b", ocr_text)
        if not words:
            return 0.0

        # Count matches
        matched = sum(1 for w in words if w.lower() in self._dict_set)
        return matched / len(words)
