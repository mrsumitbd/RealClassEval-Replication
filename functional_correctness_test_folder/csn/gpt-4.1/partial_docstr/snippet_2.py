
from typing import Iterable
import string


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.words = set()
        for word in wordlist:
            if all(c.isalpha() for c in word):
                self.words.add(word)

    def measure_words_matched(self, ocr_text: str) -> float:
        # Split text into words, strip punctuation, and match
        tokens = ocr_text.split()
        matched = 0
        total = 0
        for token in tokens:
            # Remove leading/trailing punctuation
            word = token.strip(string.punctuation)
            if not word or not word.isalpha():
                continue
            total += 1
            if word in self.words:
                matched += 1
        if total == 0:
            return 0.0
        return matched / total
