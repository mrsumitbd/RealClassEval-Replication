class _ScopedValueOverrideContext:

    def __init__(self, target, value):
        self._target = target
        self._value = value
        self._old_value = None

    def __enter__(self):
        self._old_value = self._target._value
        self._target._value = self._value

    def __exit__(self, exc_type, exc_value, tb):
        self._target._value = self._old_value