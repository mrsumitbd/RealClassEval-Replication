import typing


class TableCell:
    '''
    General definition of a table cell.
    :param kind: Kind of the cell (used for styling purposes, see :class:`~TableDesign`).
    :param value: Exact content of the cell.
    :param alignment: How text should be aligned in the cell.
    '''

    def __init__(self, kind: str, value: typing.Any, *, alignment: 'Alignment' = '<') -> None:
        '''Initialize new :class:`~TableCell` instance.'''
        if not isinstance(kind, str):
            raise TypeError("kind must be a string")
        if not isinstance(alignment, str):
            raise TypeError("alignment must be a string")
        if alignment not in ('<', '^', '>'):
            raise ValueError("alignment must be one of '<', '^', '>'")

        self.kind: str = kind
        self.value: typing.Any = value
        self.alignment: str = alignment

    def __repr__(self) -> str:
        '''Prepare a string representation of the instance.'''
        return f"TableCell(kind={self.kind!r}, value={self.value!r}, alignment={self.alignment!r})"

    def __str__(self) -> str:
        '''Prepare a string representation of the instance.'''
        return str(self.value)
