import abc
from typing import List, Tuple, Optional


class CompletionError(Exception):
    pass


class Completer(abc.ABC):
    '''base class for completers'''
    @abc.abstractmethod
    def complete(self, original: str, pos: int) -> List[Tuple[str, int]]:
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

    def relevant_part(self, original: Optional[str], pos: Optional[int]) -> Tuple[str, int, int]:
        '''
        Calculate the subword in a ' '-separated list of substrings of
        `original` that `pos` is in.

        Returns a tuple: (substring, start_index, end_index)
        where start_index and end_index delimit the substring within original.
        '''
        if original is None:
            original = ''
        if not isinstance(original, str):
            raise TypeError("original must be a string")

        n = len(original)
        if pos is None:
            pos = n
        if not isinstance(pos, int):
            raise TypeError("pos must be an int")

        if pos < 0:
            pos = 0
        if pos > n:
            pos = n

        if n == 0:
            return '', 0, 0

        # If position is on a space, move to the start of the next token
        i = pos
        if i < n and original[i] == ' ':
            while i < n and original[i] == ' ':
                i += 1
            start = i
        else:
            # Find start of the current token
            start = original.rfind(' ', 0, pos) + 1

        if start >= n:
            return '', n, n

        # Find end of the current token
        space_idx = original.find(' ', start)
        end = n if space_idx == -1 else space_idx

        part = original[start:end]
        return part, start, end
