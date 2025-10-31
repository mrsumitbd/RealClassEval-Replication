
from typing import Iterable


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.word_set = set(wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Returns the fraction of words in the OCR text that are in the dictionary.'''
        words = ocr_text.split()
        if not words:
            return 0.0
        matched = 0
        for word in words:
            if word in self.word_set:
                matched += 1
        return matched / len(words)
