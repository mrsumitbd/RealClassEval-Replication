
from typing import Iterable


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.word_set = set(word for word in wordlist if word.isalpha())

    def measure_words_matched(self, ocr_text: str) -> float:
        words_in_text = set(
            word for word in ocr_text.split() if word.isalpha())
        matched_words = words_in_text.intersection(self.word_set)
        return len(matched_words) / len(words_in_text) if words_in_text else 0.0
