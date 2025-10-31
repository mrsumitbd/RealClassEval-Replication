from itertools import count

class Header:
    """
    Header of a table -- contains column names and a mapping from them
    to column indexes
    """

    def __init__(self, fields):
        self.set_fields(fields)

    def set_fields(self, fields):
        self.fields = fields
        self.field_to_column = dict(zip(fields, count()))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.fields[key]
        elif isinstance(key, str):
            if key in self.field_to_column:
                return key
        else:
            raise TypeError('field indices must be integers or strings')

    def __str__(self):
        return '#' + '\t'.join(self.fields)