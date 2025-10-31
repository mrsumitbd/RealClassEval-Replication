class SchemaUpdateConflict:
    CONFLICT_TYPES = {'required_no_default': "Required field '{}' added without supplying a default value", 'incompatible_type': "Incompatible change in type of field '{}'", 'incompatible_choices': "Choices list for field '{}' doesn't include current field value"}

    def __init__(self, field, typ, **kwargs):
        if typ not in self.CONFLICT_TYPES:
            raise ValueError("Invalid type '{}' for SchemaUpdateConflict".format(typ))
        self.field = field
        self.typ = typ
        self.args = kwargs

    def message(self):
        return self.CONFLICT_TYPES[self.typ].format(self.field)

    def __eq__(self, other):
        return self.field == other.field and self.typ == other.typ