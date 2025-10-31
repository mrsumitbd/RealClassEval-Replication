
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
            return ""

        left = original.rfind(' ', 0, pos) + 1
        right = original.find(' ', pos)
        if right == -1:
            right = len(original)

        return original[left:right]
