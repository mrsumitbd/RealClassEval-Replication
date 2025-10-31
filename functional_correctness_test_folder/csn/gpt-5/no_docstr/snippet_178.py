import typing

Alignment = typing.Literal['<', '>', '^']


class TableCell:
    __slots__ = ("kind", "value", "alignment")

    def __init__(self, kind: str, value: typing.Any, *, alignment: Alignment = '<') -> None:
        if alignment not in ('<', '>', '^'):
            raise ValueError(
                f"Invalid alignment: {alignment!r}. Expected one of '<', '>', '^'.")
        self.kind = str(kind)
        self.value = value
        self.alignment = alignment

    def __repr__(self) -> str:
        return f"TableCell(kind={self.kind!r}, value={self.value!r}, alignment={self.alignment!r})"

    def __str__(self) -> str:
        return '' if self.value is None else str(self.value)
