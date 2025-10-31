class Attribute:
    __slots__ = ('name', 'default', 'nullable', 'user_defined', 'validator')

    def __init__(self, name, nullable=False, user_defined=False):
        self.name = '_{}_value'.format(name)
        self.nullable = nullable
        self.user_defined = user_defined
        self.validator = None
        self.default = NO_DEFAULT

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = getattr(instance, self.name)
        if value is not NOT_SET:
            return value
        if self.nullable:
            return None
        if self.default is not NO_DEFAULT:
            return self.default
        raise AttributeError("missing required field '{}'".format(public_name(self.name)))

    def __set__(self, instance, value):
        if self.nullable and value is None:
            setattr(instance, self.name, NOT_SET)
            return
        if self.user_defined:
            self.validator.validate_type_only(value)
        else:
            value = self.validator.validate(value)
        setattr(instance, self.name, value)

    def __delete__(self, instance):
        setattr(instance, self.name, NOT_SET)