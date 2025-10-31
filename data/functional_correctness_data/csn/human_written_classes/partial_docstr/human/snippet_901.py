from typing import IO, Dict, Generator, Iterable, Iterator, List, Mapping, Optional, Sequence, Set, Tuple, Union, cast as typing_cast

class Field:
    """
    A tuple describing a column in a TSDB database relation.

    Args:
        name (str): column name
        datatype (str): `":string"`, `":integer"`, `":date"`,
            or `":float"`
        flags (list): List of additional flags
        comment (str): description of the column
    Attributes:
        is_key (bool): `True` if the column is a key in the database.

        default (str): The default formatted value (see
            :func:`format`) when the value it describes is `None`.
    """
    __slots__ = ('name', 'datatype', 'flags', 'comment', 'is_key', 'default')

    def __init__(self, name: str, datatype: str, flags: Optional[Iterable[str]]=None, comment: Optional[str]=None) -> None:
        self.name = name
        self.datatype = datatype
        self.flags = tuple(flags or [])
        self.comment = comment
        self.is_key = False
        for flag in self.flags:
            if flag in (':key', ':primary') or flag.startswith(':foreign'):
                self.is_key = True
        self.default: str = TSDB_CODED_ATTRIBUTES.get(name, '-1' if datatype == ':integer' else '')

    def __str__(self):
        parts = [self.name, self.datatype]
        parts.extend(self.flags)
        s = '  ' + ' '.join(parts)
        if self.comment:
            s = '{}# {}'.format(s.ljust(40), self.comment)
        return s

    def __eq__(self, other):
        if not isinstance(other, Field):
            return NotImplemented
        return self.name == other.name and self.datatype == other.datatype and (self.flags == other.flags)