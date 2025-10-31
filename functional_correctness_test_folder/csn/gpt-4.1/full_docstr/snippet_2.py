
import string
from typing import Iterable


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.words = set()
        for word in wordlist:
            if all(c.isalnum() for c in word):
                self.words.add(word)

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Check how many unique words in the OCR text match a dictionary.
        Words with mixed capitalized are only considered a match if the test word
        matches that capitalization.
        Returns:
            number of words that match / number
        '''
        # Split text into words, remove punctuation, and filter out empty words
        table = str.maketrans('', '', string.punctuation)
        words_in_text = set()
        for w in ocr_text.split():
            w_clean = w.translate(table)
            if w_clean and w_clean.isalnum():
                words_in_text.add(w_clean)
        if not words_in_text:
            return 0.0
        matched = sum(1 for w in words_in_text if w in self.words)
        return matched / len(words_in_text)
