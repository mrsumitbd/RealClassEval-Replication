class AccessEnumMixin:
    '''Mixin for enum functionalities.'''
    @classmethod
    def validate(cls, level):
        '''Validate a string against the enum values.'''
        if isinstance(level, cls):
            return level

        # Try matching by name/value with case-insensitive handling for strings
        if isinstance(level, str):
            lvl_lower = level.lower()
            for member in cls:
                name_match = member.name.lower() == lvl_lower
                value_match = isinstance(
                    member.value, str) and member.value.lower() == lvl_lower
                if name_match or value_match:
                    return member

        # Fallback: try exact value match for non-strings or unmatched strings
        for member in cls:
            if member.value == level:
                return member

        valid = [m.name for m in cls]
        raise ValueError(
            f"Invalid {cls.__name__} value: {level!r}. Expected one of: {', '.join(valid)}")

    def __str__(self):
        '''Return its value.'''
        return str(self.value)
