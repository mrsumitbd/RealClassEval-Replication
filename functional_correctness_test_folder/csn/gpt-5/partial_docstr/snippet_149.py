class TorConfigType:
    '''
    Base class for all configuration types, which function as parsers
    and un-parsers.
    '''

    def parse(self, s):
        if s is None:
            return None
        if isinstance(s, str):
            return s
        return str(s)

    def validate(self, s, instance, name):
        try:
            value = self.parse(s)
        except Exception as e:
            raise ValueError(
                f"Invalid value for {name} on {instance}: {s!r}. Error: {e}") from e
        if value is not None and not isinstance(value, str):
            raise ValueError(
                f"Parse did not produce a string for {name} on {instance}: got {type(value).__name__}")
        return value
