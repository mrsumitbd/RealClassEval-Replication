class _TimestampTokens:
    """Holds the individual numeric tokens (as strings) that compose a `Timestamp`."""

    def __init__(self, year=None):
        fld = []
        for i in iter(_TimestampState):
            fld.append(None)
        if year is not None:
            fld[_TimestampState.YEAR] = year
        self._fields = fld

    def transition(self, state):
        val = bytearray()
        self._fields[state] = val
        return val

    def __getitem__(self, item):
        return self._fields[item]