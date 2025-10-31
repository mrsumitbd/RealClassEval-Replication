class ReSTTable:

    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows
        self.widths = [len(header) for header in self.headers]
        for row in self.rows:
            for column, cell in enumerate(row):
                self.widths[column] = max(self.widths[column], len(cell))

    def _render_line(self, char='-'):
        parts = ['']
        for width in self.widths:
            parts.append(char * (width + 2))
        parts.append('')
        return '+'.join(parts)

    def _render_row(self, row):
        parts = ['']
        for width, cell in zip(self.widths, row):
            parts.append(' %s ' % cell.ljust(width))
        parts.append('')
        return '|'.join(parts)

    def render(self, write_line):
        write_line(self._render_line('-'))
        write_line(self._render_row(self.headers))
        write_line(self._render_line('='))
        for row in self.rows:
            write_line(self._render_row(row))
            write_line(self._render_line('-'))