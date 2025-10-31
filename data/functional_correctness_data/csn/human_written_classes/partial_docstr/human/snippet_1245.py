class LazyProperty:
    """
    A lazy property is a cached_property which can also be set a value.

    A lazy property will remember the value once it has been accessed once.
    The code inside the property will run maximum 1 time per instance.
    When the property is given a value, the code inside will never run and
    the given value will be returned when retrieving the property.
    """

    def __init__(self, method):
        super().__init__()
        self.method = method
        self.cache_name = f'_cache_{self.method.__name__}'

    def __get__(self, instance, owner):
        try:
            return getattr(instance, self.cache_name)
        except AttributeError:
            value = self.method(instance)
            setattr(instance, self.cache_name, value)
            return value

    def __set__(self, instance, value):
        setattr(instance, self.cache_name, value)