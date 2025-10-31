
import typing

Alignment = str  # simple alias for alignment specifier


class TableCell:
    """
    Represents a single cell in a table.

    Parameters
    ----------
    kind : str
        The kind of the cell (e.g., 'header', 'data', etc.).
    value : Any
        The value stored in the cell.
    alignment : Alignment, optional
        Alignment specifier for the cell content. Defaults to '<' (left).
    """

    def __init__(self, kind: str, value: typing.Any, *, alignment: Alignment = "<") -> None:
        self.kind = kind
        self.value = value
        self.alignment = alignment

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"kind={self.kind!r}, "
            f"value={self.value!r}, "
            f"alignment={self.alignment!r})"
        )

    def __str__(self) -> str:
        return str(self.value)
