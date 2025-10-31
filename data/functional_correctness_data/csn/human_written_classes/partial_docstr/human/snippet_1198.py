class InnerFieldTypeMixin:

    def __init__(self, field_type=None, **kwargs):
        self._field_type = None
        if isinstance(field_type, tuple):
            field_type = field_type[0](**field_type[1])
        self.field_type = field_type if field_type else BaseField()
        super(InnerFieldTypeMixin, self).__init__(**kwargs)

    def export_definition(self):
        result = super(InnerFieldTypeMixin, self).export_definition()
        result['field_type'] = (self.field_type.__class__, self.field_type.export_definition())
        return result

    @property
    def field_type(self):
        """field_type getter: field type used on array or hashmap"""
        return self._field_type

    @field_type.setter
    def field_type(self, value):
        """Model_class setter: field type used on array or hashmap"""
        self._field_type = value