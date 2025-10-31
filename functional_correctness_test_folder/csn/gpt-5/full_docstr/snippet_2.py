from typing import Iterable
import re


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self._case_insensitive = set()
        self._case_sensitive = set()
        word_re = re.compile(r'^[A-Za-z]+$')

        for w in wordlist:
            if not isinstance(w, str):
                continue
            if not word_re.match(w):
                continue
            if w.islower():
                self._case_insensitive.add(w)
            else:
                self._case_sensitive.add(w)

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Check how many unique words in the OCR text match a dictionary.
        Words with mixed capitalized are only considered a match if the test word
        matches that capitalization.
        Returns:
            number of words that match / number
        '''
        if not isinstance(ocr_text, str):
            return 0.0

        tokens = set(re.findall(r'[A-Za-z]+', ocr_text))
        if not tokens:
            return 0.0

        matched = 0
        for tok in tokens:
            if tok in self._case_sensitive:
                matched += 1
            elif tok.lower() in self._case_insensitive:
                matched += 1

        return matched / len(tokens)
