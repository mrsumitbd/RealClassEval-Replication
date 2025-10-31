from sevenbridges.errors import ReadOnlyPropertyError, ValidationError

class Field:
    EMPTY = object()

    def __init__(self, name=None, read_only=True, validator=None):
        self.name = name
        self.read_only = read_only
        self.validator = validator

    def __set__(self, instance, value):
        if self.read_only and instance._data[self.name] is not Field.EMPTY:
            raise ReadOnlyPropertyError(f'Property {self.name} is marked as read only!')
        if self.name == 'metadata':
            instance._overwrite_metadata = True
            if value is None:
                raise ValidationError('Not a valid dictionary!')
        value = self.validate(value)
        try:
            current_value = instance._data[self.name]
            if current_value == value:
                return
        except KeyError:
            pass
        instance._dirty[self.name] = value
        instance._data[self.name] = value

    def __get__(self, instance, cls):
        try:
            data = instance._data[self.name]
            return data
        except (KeyError, AttributeError):
            return None

    def validate(self, value):
        if self.validator is not None:
            return self.validator(value)
        return value