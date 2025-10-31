class PropertyValidator:

    def __init__(self, **kwargs):
        self.description = kwargs.pop('description', None)
        self.error_message = kwargs.pop('error_message', kwargs.pop('errorMessage', None))
        self.expression = kwargs.pop('expression', None)
        self.name = kwargs.pop('name', None)
        self.new = kwargs.pop('new', None)
        self.properties = kwargs.pop('properties', None)
        self.row_id = kwargs.pop('row_id', kwargs.pop('rowId', None))
        self.type = kwargs.pop('type', None)

    def to_json(self, strip_none=True):
        data = {'description': self.description, 'errorMessage': self.error_message, 'expression': self.expression, 'name': self.name, 'new': self.new, 'properties': self.properties, 'rowId': self.row_id, 'type': self.type}
        return strip_none_values(data, strip_none)