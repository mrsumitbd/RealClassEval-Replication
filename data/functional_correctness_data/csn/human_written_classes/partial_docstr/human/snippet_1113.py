class Trigram:
    """
    This represents a "compiled" trigram object. It is able to compute its
    similarity with other trigram objects.
    """

    def __init__(self, string):
        self._string = string
        self._norm = normalize(string)
        self._words = make_words(self._norm)
        self._trigrams = {t for w in self._words for t in make_trigrams(w)}

    def __repr__(self):
        return f'Trigram({self._norm!r})'

    def similarity(self, other: 'Trigram') -> float:
        """
        Compute the similarity with the provided other trigram.
        """
        if not len(self._trigrams) or not len(other._trigrams):
            return 0
        count = float(len(self._trigrams & other._trigrams))
        len1 = float(len(self._trigrams))
        len2 = float(len(other._trigrams))
        return count / (len1 + len2 - count)

    def __mod__(self, other: 'Trigram') -> float:
        """
        Shortcut notation using modulo symbol.
        """
        return self.similarity(other)