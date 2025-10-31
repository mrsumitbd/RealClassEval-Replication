class TableRow:
    """
    A row of a table
    """

    def __init__(self, reader, fields):
        self.reader = reader
        self.fields = fields

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.fields[key]
        elif isinstance(key, str):
            if self.reader.header:
                return self.fields[self.reader.header.field_to_column[key]]
            else:
                raise TypeError('column names only supported for files with headers')
        else:
            raise TypeError('field indices must be integers or strings')

    @property
    def fieldnames(self):
        return self.reader.header.fields

    def __str__(self):
        return '\t'.join(self.fields)