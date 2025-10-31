
class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.dictionary = set(wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        '''Check how many unique words in the OCR text match a dictionary.
        Words with mixed capitalized are only considered a match if the test word
        matches that capitalization.
        Returns:
            number of words that match / number
        '''
        words = set(re.findall(r'\b\w+\b', ocr_text))
        matches = words & self.dictionary
        return len(matches) / len(words) if words else 0.0
