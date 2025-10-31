
import abc


class Completer(abc.ABC):
    '''base class for completers'''
    @abc.abstractmethod
    def complete(self, original, pos):
        '''returns a list of completions and cursor positions for the string
        `original` from position `pos` on.
        :param original: the string to complete
        :type original: str
        :param pos: starting position to complete from
        :type pos: int
        :returns: pairs of completed string and cursor position in the
                  new string
        :rtype: list of (str, int)
        :raises: :exc:`CompletionError`
        '''
        pass

    def relevant_part(self, original, pos):
        '''
        Calculate the subword in a ' '-separated list of substrings of
        `original` that `pos` is in.
        '''
        start = original.rfind(' ', 0, pos)
        if start == -1:
            start = 0
        else:
            start += 1

        end = original.find(' ', pos)
        if end == -1:
            end = len(original)

        return original[start:end], start, end
