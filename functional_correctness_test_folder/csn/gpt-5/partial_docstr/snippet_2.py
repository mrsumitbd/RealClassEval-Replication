from typing import Iterable, Set
import re


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''
    _word_re = re.compile(r"[A-Za-z]+")

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self._insensitive: Set[str] = set()
        self._sensitive: Set[str] = set()

        for w in wordlist:
            if not isinstance(w, str):
                continue
            if not re.fullmatch(self._word_re, w):
                continue
            if w.islower():
                self._insensitive.add(w)
            else:
                self._sensitive.add(w)

    def measure_words_matched(self, ocr_text: str) -> float:
        tokens = re.findall(self._word_re, ocr_text or "")
        if not tokens:
            return 0.0
        matched = 0
        for t in tokens:
            if t in self._sensitive or t.lower() in self._insensitive:
                matched += 1
        return matched / len(tokens)
