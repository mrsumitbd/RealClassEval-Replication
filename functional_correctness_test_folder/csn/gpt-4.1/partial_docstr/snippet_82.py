
import abc


class Completer:

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        '''
        Calculate the subword in a ' '-separated list of substrings of
        `original` that `pos` is in.
        '''
        if pos < 0 or pos > len(original):
            raise ValueError("pos out of bounds")
        # Find the start of the word
        start = pos
        while start > 0 and original[start - 1] != ' ':
            start -= 1
        # Find the end of the word
        end = pos
        while end < len(original) and original[end] != ' ':
            end += 1
        return original[start:end]
