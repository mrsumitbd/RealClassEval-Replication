class FieldIndex:

    def __init__(self, **kwargs):
        self.column_names = kwargs.pop('column_names', kwargs.pop('columnNames', None))
        self.unique = kwargs.pop('unique', None)

    def to_json(self, strip_none=True):
        data = {'columnNames': self.column_names, 'unique': self.unique}
        return strip_none_values(data, strip_none)