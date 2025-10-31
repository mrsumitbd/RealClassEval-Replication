class Words2Numbers:
    """
    The class provides a text-to-number conversion utility, allowing conversion of written numbers (in words) to their numerical representation.
    """

    def __init__(self):
        """
        Initialize the word lists and dictionaries required for conversion
        """
        self.numwords = {}
        self.units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
        ]
        self.tens = ["", "", "twenty", "thirty", "forty",
                     "fifty", "sixty", "seventy", "eighty", "ninety"]
        self.scales = ["hundred", "thousand", "million", "billion", "trillion"]

        self.numwords["and"] = (1, 0)
        for idx, word in enumerate(self.units):
            self.numwords[word] = (1, idx)
        for idx, word in enumerate(self.tens):
            self.numwords[word] = (1, idx * 10)
        for idx, word in enumerate(self.scales):
            self.numwords[word] = (10 ** (idx * 3 or 2), 0)

        self.ordinal_words = {'first': 1, 'second': 2, 'third': 3,
                              'fifth': 5, 'eighth': 8, 'ninth': 9, 'twelfth': 12}
        self.ordinal_endings = [('ieth', 'y'), ('th', '')]

    def _normalize_ordinal(self, word):
        if word in self.ordinal_words:
            return self.ordinal_words[word]
        for end, repl in self.ordinal_endings:
            if word.endswith(end):
                base = word[: -len(end)] + repl
                if base in self.numwords:
                    scale, incr = self.numwords[base]
                    if scale == 1:
                        return incr
        return None

    def text2int(self, textnum):
        """
        Convert the word string to the corresponding integer string
        :param textnum: string, the word string to be converted
        :return: string, the final converted integer string
        >>> w2n = Words2Numbers()
        >>> w2n.text2int("thirty-two")
        "32"
        """
        if not isinstance(textnum, str) or not textnum.strip():
            raise ValueError("Input must be a non-empty string")
        textnum = textnum.lower().replace('-', ' ')
        words = textnum.split()
        current = 0
        result = 0
        for w in words:
            if w == 'and':
                continue
            val = None
            if w in self.numwords:
                scale, increment = self.numwords[w]
                if scale == 1:
                    current += increment
                else:
                    if current == 0:
                        current = 1
                    current *= scale
                    if scale >= 1000:
                        result += current
                        current = 0
                continue
            val = self._normalize_ordinal(w)
            if val is not None:
                current += val
                continue
            raise ValueError(f"Invalid word: {w}")
        total = result + current
        return str(total)

    def is_valid_input(self, textnum):
        """
        Check if the input text contains only valid words that can be converted into numbers.
        :param textnum: The input text containing words representing numbers.
        :return: True if input is valid, False otherwise.
        >>> w2n = Words2Numbers()
        >>> w2n.is_valid_input("thirty-two")
        False
        """
        if not isinstance(textnum, str) or not textnum.strip():
            return False
        # Hyphens or other non-alpha characters (besides spaces) make it invalid
        for ch in textnum:
            if not (ch.isalpha() or ch.isspace()):
                return False
        words = textnum.lower().split()
        if not words:
            return False
        for w in words:
            if w == 'and':
                continue
            if w in self.numwords:
                continue
            if self._normalize_ordinal(w) is not None:
                continue
            return False
        return True
