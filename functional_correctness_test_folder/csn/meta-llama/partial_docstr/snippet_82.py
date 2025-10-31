
import abc
import re


class Completer(abc.ABC):

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        '''
        Calculate the subword in a ' '-separated list of substrings of
        `original` that `pos` is in.
        '''
        # Find the start and end of the word that `pos` is in
        start = pos
        while start > 0 and original[start-1] != ' ':
            start -= 1
        end = pos
        while end < len(original) and original[end] != ' ':
            end += 1

        # Return the word that `pos` is in
        return original[start:end]
