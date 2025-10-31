
import typing
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Alignment(Enum):
    LEFT = '<'
    CENTER = '^'
    RIGHT = '>'


class TableCell:

    def __init__(self, kind: str, value: typing.Any, *, alignment: Alignment = Alignment.LEFT) -> None:
        self.kind = kind
        self.value = value
        self.alignment = alignment

    def __repr__(self) -> str:
        return f'TableCell(kind={self.kind!r}, value={self.value!r}, alignment={self.alignment})'

    def __str__(self) -> str:
        return str(self.value)
