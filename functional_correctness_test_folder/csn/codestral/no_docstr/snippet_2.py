
class OcrQualityDictionary:

    def __init__(self, *, wordlist: Iterable[str]):
        self.wordlist = set(wordlist)

    def measure_words_matched(self, ocr_text: str) -> float:
        ocr_words = set(ocr_text.split())
        matched_words = self.wordlist.intersection(ocr_words)
        return len(matched_words) / len(ocr_words) if ocr_words else 0.0
