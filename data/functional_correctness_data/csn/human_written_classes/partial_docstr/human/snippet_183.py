import itertools

class _GroupConsecutive:
    """
    Used as a callable `key` for itertools.groupby to group
    characters that are consecutive:

    .. testcode::

       from itertools import groupby
       from pyparsing.util import _GroupConsecutive

       grouped = groupby("abcdejkmpqrs", key=_GroupConsecutive())
       for index, group in grouped:
           print(tuple([index, list(group)]))

    prints:

    .. testoutput::

       (0, ['a', 'b', 'c', 'd', 'e'])
       (1, ['j', 'k'])
       (2, ['m'])
       (3, ['p', 'q', 'r', 's'])
    """

    def __init__(self) -> None:
        self.prev = 0
        self.counter = itertools.count()
        self.value = -1

    def __call__(self, char: str) -> int:
        c_int = ord(char)
        self.prev, prev = (c_int, self.prev)
        if c_int - prev > 1:
            self.value = next(self.counter)
        return self.value