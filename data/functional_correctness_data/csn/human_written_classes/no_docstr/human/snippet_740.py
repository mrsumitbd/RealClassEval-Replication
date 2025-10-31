class SettableProperty:

    def __init__(self, get_default):
        self.get_default = get_default
        self.internal_field_name = '_' + get_default.__name__
        self.__doc__ = get_default.__doc__

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if hasattr(instance, self.internal_field_name):
            return getattr(instance, self.internal_field_name)
        else:
            return self.get_default(instance)

    def __set__(self, instance, value):
        setattr(instance, self.internal_field_name, value)

    def __delete__(self, instance):
        try:
            delattr(instance, self.internal_field_name)
        except AttributeError:
            pass