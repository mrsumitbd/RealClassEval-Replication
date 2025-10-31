
import re
from typing import Iterable, Set


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        # Keep only words that consist solely of alphabetic characters
        self._words: Set[str] = {
            w for w in wordlist
            if isinstance(w, str) and re.fullmatch(r"[A-Za-z]+", w)
        }

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Return the fraction of words in `ocr_text` that are present in the dictionary.'''
        # Find all word tokens (letters, digits, underscore)
        tokens = re.findall(r"\b\w+\b", ocr_text)
        if not tokens:
            return 0.0
        matched = sum(1 for t in tokens if t in self._words)
        return matched / len(tokens)
