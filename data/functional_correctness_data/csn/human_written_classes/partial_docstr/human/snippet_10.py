class _ValidateTypeDescriptor:
    """Base Class Descriptor which validates type of any subclass attribute."""

    def __init__(self, name, expected_type: type):
        self.name = name
        self.expected_type = expected_type

    def __get__(self, obj, cls):
        return obj._print_options.get(self.name, None)

    def __set__(self, obj, value) -> None:
        if not isinstance(value, self.expected_type):
            raise ValueError(f'{self.name} should be of type {self.expected_type.__name__}')
        obj._print_options[self.name] = value