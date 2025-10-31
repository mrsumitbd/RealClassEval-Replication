class RawPacket:

    def __init__(self, packet):
        self._packet = packet

    def __getattr__(self, fieldname):
        try:
            value = self._packet[fieldname]
        except Exception as e:
            raise AttributeError(
                f"{self.__class__.__name__!s} has no attribute {fieldname!r}") from e
        return self._wrap(value)

    def _wrap(self, value):
        if isinstance(value, dict):
            return RawPacket(value)
        if isinstance(value, list):
            return [self._wrap(v) for v in value]
        return value
