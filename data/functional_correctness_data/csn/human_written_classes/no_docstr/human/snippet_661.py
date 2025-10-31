class UserDefinedField:

    def __init__(self, name, label, example, field_type, choices=None):
        self.name = name
        self.label = label
        self.example = example
        self.field_type = field_type
        self.choices = choices

    def __repr__(self):
        return '{}({}): {}'.format(self.label, self.field_type.name, self.example)