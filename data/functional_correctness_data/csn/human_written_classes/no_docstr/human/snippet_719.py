class _PropertyOverrideContext:

    def __init__(self, target, property_name, value):
        self._target = target
        self._property_name = property_name
        self._value = value
        self._old_value = None

    def __enter__(self):
        self._old_value = getattr(self._target, self._property_name)
        setattr(self._target, self._property_name, self._value)

    def __exit__(self, exc_type, exc_value, tb):
        setattr(self._target, self._property_name, self._old_value)