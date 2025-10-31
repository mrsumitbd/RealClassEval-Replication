class _Parameter:
    """Represents a parameter to a capability"""

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @classmethod
    def from_string(cls, string):
        try:
            key, value = string.split('=')
        except ValueError:
            raise _InvalidParameter
        return cls(key, value)