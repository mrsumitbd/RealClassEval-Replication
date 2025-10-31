
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
        self.kind = kind
        self.value = value
        self.alignment = alignment

    def __repr__(self) -> str:
        '''Prepare a string representation of the instance.'''
        return (f"TableCell(kind={self.kind!r}, value={self.value!r}, "
                f"alignment={self.alignment!r})")

    def __str__(self) -> str:
        '''Prepare a string representation of the instance.'''
        return str(self.value)
