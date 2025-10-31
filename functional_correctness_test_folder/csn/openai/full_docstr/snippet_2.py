
import re
from collections.abc import Iterable


class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        # Keep only words that consist solely of alphabetic characters.
        self._words = {w for w in wordlist if isinstance(
            w, str) and w.isalpha()}

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Check how many unique words in the OCR text match a dictionary.
        Words with mixed capitalized are only considered a match if the test word
        matches that capitalization.
        Returns:
            number of words that match / number
        '''
        # Extract words (alphanumeric + underscore) from the OCR text.
        # This automatically ignores punctuation and spaces.
        words = re.findall(r'\b\w+\b', ocr_text)
        unique_words = set(words)

        if not unique_words:
            return 0.0

        matched = sum(1 for w in unique_words if w in self._words)
        return matched / len(unique_words)
