class BoyerMooreSearch:
    """
    his is a class that implements the Boyer-Moore algorithm for string searching, which is used to find occurrences of a pattern within a given text.
    """

    def __init__(self, text, pattern):
        """
        Initializes the BoyerMooreSearch class with the given text and pattern.
        :param text: The text to be searched, str.
        :param pattern: The pattern to be searched for, str.
        """
        self.text, self.pattern = text, pattern
        self.textLen, self.patLen = len(text), len(pattern)

    def match_in_pattern(self, char):
        """
        Finds the rightmost occurrence of a character in the pattern.
        :param char: The character to be searched for, str.
        :return: The index of the rightmost occurrence of the character in the pattern, int.
        >>> boyerMooreSearch = BoyerMooreSearch("ABAABA", "AB")
        >>> boyerMooreSearch.match_in_pattern("A")
        0

        """
        if self.patLen == 0 or not char:
            return -1
        return self.pattern.rfind(char)

    def mismatch_in_text(self, currentPos):
        """
        Determines the position of the first dismatch between the pattern and the text.
        :param currentPos: The current position in the text, int.
        :return: The position of the first dismatch between the pattern and the text, int,otherwise -1.
        >>> boyerMooreSearch = BoyerMooreSearch("ABAABA", "ABC")
        >>> boyerMooreSearch.mismatch_in_text(0)
        2

        """
        if self.patLen == 0:
            return -1
        j = self.patLen - 1
        while j >= 0:
            ti = currentPos + j
            if ti >= self.textLen:
                return j
            if self.pattern[j] != self.text[ti]:
                return j
            j -= 1
        return -1

    def bad_character_heuristic(self):
        """
        Finds all occurrences of the pattern in the text.
        :return: A list of all positions of the pattern in the text, list.
        >>> boyerMooreSearch = BoyerMooreSearch("ABAABA", "AB")
        >>> boyerMooreSearch.bad_character_heuristic()
        [0, 3]

        """
        if self.patLen == 0:
            return list(range(self.textLen + 1))
        result = []
        s = 0
        while s <= self.textLen - self.patLen:
            j = self.patLen - 1
            while j >= 0 and self.pattern[j] == self.text[s + j]:
                j -= 1
            if j < 0:
                result.append(s)
                s += 1
            else:
                bad_char = self.text[s + j]
                last = self.match_in_pattern(bad_char)
                shift = j - last if last != -1 else j + 1
                s += max(1, shift)
        return result
