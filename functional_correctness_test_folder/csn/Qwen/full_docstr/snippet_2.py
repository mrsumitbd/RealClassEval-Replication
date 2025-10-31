
from typing import Iterable
import re


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.dictionary = set(
            word for word in wordlist if re.match(r'^\w+$', word))

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Check how many unique words in the OCR text match a dictionary.
        Words with mixed capitalized are only considered a match if the test word
        matches that capitalization.
        Returns:
            number of words that match / number
        '''
        words_in_text = set(re.findall(r'\b\w+\b', ocr_text))
        matched_words = words_in_text.intersection(self.dictionary)
        return len(matched_words) / len(words_in_text) if words_in_text else 0.0
