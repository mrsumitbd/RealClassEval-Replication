
import abc


class Completer(abc.ABC):
    @abc.abstractmethod
    def complete(self, original, pos):
        """
        Abstract method to be implemented by subclasses.
        Should return a list of completion candidates for the word
        at the given position `pos` in the string `original`.
        """
        pass

    def relevant_part(self, original, pos):
        """
        Return the subword in a space-separated list of substrings of
        `original` that contains the character at index `pos`.

        Parameters
        ----------
        original : str
            The original string containing space-separated words.
        pos : int
            The index (0‑based) of the character whose word should be
            extracted.

        Returns
        -------
        str
            The word that contains the character at `pos`. If `pos`
            is out of bounds or the character is a space, an empty
            string is returned.
        """
        if not isinstance(original, str):
            raise TypeError("original must be a string")
        if not isinstance(pos, int):
            raise TypeError("pos must be an integer")
        if pos < 0 or pos >= len(original):
            return ""

        # If the character at pos is a space, there's no word.
        if original[pos].isspace():
            return ""

        # Find the start of the word.
        start = pos
        while start > 0 and not original[start - 1].isspace():
            start -= 1

        # Find the end of the word.
        end = pos
        while end < len(original) - 1 and not original[end + 1].isspace():
            end += 1

        return original[start:end + 1]
