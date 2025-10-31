
import string


class Completer:
    """
    A simple word completer that suggests completions based on a predefined
    dictionary of words. The `complete` method returns all words that start
    with the relevant part of the input string at the given cursor position.
    """

    # A small sample dictionary of words for completion suggestions.
    _dictionary = [
        "apple", "application", "apricot", "banana", "band", "bandana",
        "cherry", "date", "dragonfruit", "fig", "grape", "grapefruit",
        "kiwi", "lemon", "lime", "mango", "nectarine", "orange",
        "papaya", "peach", "pear", "pineapple", "plum", "raspberry",
        "strawberry", "tangerine", "watermelon"
    ]

    def relevant_part(self, original: str, pos: int) -> str:
        """
        Return the substring of `original` that is relevant for completion
        at the cursor position `pos`. This is the word fragment that starts
        at the last whitespace before `pos` (or the beginning of the string)
        and ends at `pos`.

        Parameters
        ----------
        original : str
            The full input string.
        pos : int
            The cursor position within `original`.

        Returns
        -------
        str
            The relevant word fragment.
        """
        if not original:
            return ""

        # Clamp pos to the bounds of the string
        pos = max(0, min(pos, len(original)))

        # Find the start of the word by scanning leftwards until a whitespace
        start = pos
        while start > 0 and not original[start - 1].isspace():
            start -= 1

        return original[start:pos]

    def complete(self, original: str, pos: int) -> list[str]:
        """
        Return a list of completion suggestions based on the relevant part
        of the input string at the cursor position `pos`.

        Parameters
        ----------
        original : str
            The full input string.
        pos : int
            The cursor position within `original`.

        Returns
        -------
        list[str]
            A list of words from the dictionary that start with the relevant
            part. The comparison is case-insensitive.
        """
        fragment = self.relevant_part(original, pos).lower()
        if not fragment:
            # If there's no fragment, return the entire dictionary
            return sorted(self._dictionary)

        # Filter dictionary for words that start with the fragment
        matches = [
            word for word in self._dictionary if word.lower().startswith(fragment)]
        return sorted(matches)
