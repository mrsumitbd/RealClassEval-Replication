
class OcrQualityDictionary:
    '''Manages a dictionary for simple OCR quality checks.'''

    def __init__(self, *, wordlist: Iterable[str]):
        '''Construct a dictionary from a list of words.
        Words for which capitalization is important should be capitalized in the
        dictionary. Words that contain spaces or other punctuation will never match.
        '''
        self.wordlist = set(wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        ocr_words = re.findall(r'\b\w+\b', ocr_text)
        matched_words = [word for word in ocr_words if word in self.wordlist]
        return len(matched_words) / len(ocr_words) if ocr_words else 0.0
