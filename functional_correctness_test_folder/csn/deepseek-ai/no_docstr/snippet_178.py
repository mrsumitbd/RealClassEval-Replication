
import typing
from typing import Any


class TableCell:

    def __init__(self, kind: str, value: typing.Any, *, alignment: 'Alignment' = '<') -> None:
        self.kind = kind
        self.value = value
        self.alignment = alignment

    def __repr__(self) -> str:
        return f"TableCell(kind={self.kind!r}, value={self.value!r}, alignment={self.alignment!r})"

    def __str__(self) -> str:
        return str(self.value)
