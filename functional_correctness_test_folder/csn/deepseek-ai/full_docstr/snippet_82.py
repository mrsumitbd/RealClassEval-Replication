
import abc


class Completer:
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
        if not original:
            return ''

        parts = original.split(' ')
        current_pos = 0
        for part in parts:
            part_len = len(part)
            if current_pos <= pos <= current_pos + part_len:
                return part
            current_pos += part_len + 1  # +1 for the space

        return ''
