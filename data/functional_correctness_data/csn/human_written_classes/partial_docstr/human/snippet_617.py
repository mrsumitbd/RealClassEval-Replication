class TableRow:
    """A single row within a table.

    Attributes:
        columns: the table row's columns.
        cell_separator: string used for separating columns from each other.
    """
    __slots__ = ('cell_separator', 'columns')

    def __init__(self, cell_separator: str):
        self.columns: list[TableCell] = []
        self.cell_separator = cell_separator

    def __len__(self):
        return len(self.columns)

    def get_text(self) -> str:
        """Return a text representation of the TableRow."""
        row_lines = [self.cell_separator.join(line) for line in zip(*[column.blocks for column in self.columns], strict=False)]
        return '\n'.join(row_lines)

    @property
    def width(self) -> int:
        """Compute and return the width of the current row."""
        if not self.columns:
            return 0
        return sum((cell.width for cell in self.columns)) + len(self.cell_separator) * (len(self.columns) - 1)