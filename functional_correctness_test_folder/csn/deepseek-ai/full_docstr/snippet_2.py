
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
        '''Check how many unique words in the OCR text match a dictionary.
        Words with mixed capitalized are only considered a match if the test word
        matches that capitalization.
        Returns:
            number of words that match / number
        '''
        words = ocr_text.split()
        unique_words = set(words)
        matched = 0
        for word in unique_words:
            if word in self.word_set:
                matched += 1
        return matched / len(unique_words) if unique_words else 0.0
