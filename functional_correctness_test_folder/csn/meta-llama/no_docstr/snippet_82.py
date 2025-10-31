
import abc
import re


class Completer(abc.ABC):

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        """Extract the relevant part of the input string for completion.

        This method is used to determine the part of the input string that is relevant for completion.
        It is assumed that the relevant part is the word preceding the cursor position.

        Args:
            original (str): The original input string.
            pos (int): The cursor position in the input string.

        Returns:
            str: The relevant part of the input string.
        """
        # Find the start of the word preceding the cursor position
        start = pos
        while start > 0 and re.match(r'\w', original[start - 1]):
            start -= 1

        # Extract the relevant part
        return original[start:pos]
