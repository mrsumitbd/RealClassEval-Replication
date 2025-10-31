
import abc


class Completer:

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        """
        Returns the part of the string 'original' that is relevant for completion,
        i.e., the word fragment immediately before position 'pos'.
        """
        if pos > len(original):
            pos = len(original)
        left = original[:pos]
        # Find the start of the word fragment
        i = len(left)
        while i > 0 and (left[i-1].isalnum() or left[i-1] == '_'):
            i -= 1
        return left[i:pos]
