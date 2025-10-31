
import abc


class Completer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def complete(self, original, pos):
        pass

    def relevant_part(self, original, pos):
        '''
        Calculate the subword in a ' '-separated list of substrings of
        `original` that `pos` is in.
        '''
        parts = original.split(' ')
        current_pos = 0
        for part in parts:
            if current_pos <= pos <= current_pos + len(part):
                return part
            current_pos += len(part) + 1
        return ''
