
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
        ocr_words = set(word.strip('.,!?"\'').lower()
                        for word in ocr_text.split())
        matched_words = ocr_words.intersection(
            {word.lower() for word in self.word_set if word.isalnum()})
        case_sensitive_matches = sum(
            1 for word in ocr_words if word in self.word_set)
        return case_sensitive_matches / len(ocr_words) if ocr_words else 0.0
