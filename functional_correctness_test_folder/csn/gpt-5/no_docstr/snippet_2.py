from typing import Iterable, Set
import re
import unicodedata


class OcrQualityDictionary:
    def __init__(self, *, wordlist: Iterable[str]):
        self._dict: Set[str] = set()
        for w in wordlist:
            if w is None:
                continue
            nw = self._normalize_word(str(w))
            if nw:
                self._dict.add(nw)

        # precompile regex for tokenization (unicode word chars + apostrophes)
        self._token_re = re.compile(r"\b[\w']+\b", re.UNICODE)

    def _normalize_word(self, w: str) -> str:
        w = unicodedata.normalize("NFKC", w).casefold().strip()
        # strip leading/trailing apostrophes commonly appearing in OCR
        w = w.strip("'’`")
        return w

    def _tokenize(self, text: str):
        for m in self._token_re.finditer(text):
            tok = self._normalize_word(m.group(0))
            if not tok:
                continue
            # consider tokens that include at least one letter to avoid counting pure numbers/underscores
            if any(c.isalpha() for c in tok):
                yield tok

    def measure_words_matched(self, ocr_text: str) -> float:
        tokens = list(self._tokenize(ocr_text))
        if not tokens or not self._dict:
            return 0.0
        matched = sum(1 for t in tokens if t in self._dict)
        return matched / len(tokens)
