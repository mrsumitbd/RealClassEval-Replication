import typing

class TableCell:
    """
    General definition of a table cell.

    :param kind: Kind of the cell (used for styling purposes, see :class:`~TableDesign`).
    :param value: Exact content of the cell.
    :param alignment: How text should be aligned in the cell.
    """
    __slots__ = ('alignment', 'kind', 'value')

    def __init__(self, kind: str, value: typing.Any, *, alignment: 'Alignment'='<') -> None:
        """Initialize new :class:`~TableCell` instance."""
        if value is None:
            value = ''
        self.alignment: 'Alignment' = alignment
        self.kind: str = kind
        self.value: str = str(value)

    def __repr__(self) -> str:
        """Prepare a string representation of the instance."""
        return f'{type(self).__name__}(kind={self.kind!r}, value={self.value!r}, alignment={self.alignment!r})'

    def __str__(self) -> str:
        """Prepare a string representation of the instance."""
        return self.value