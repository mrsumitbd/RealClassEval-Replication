class Handler:
    """Handler for a specific detail of an event."""
    fieldnames: list[str] = []

    @classmethod
    def get(cls, event):
        """Return simple string representation for columnar output."""
        raise NotImplementedError

    @classmethod
    def data(cls, event):
        """Return plain data for formatted output."""
        return NotImplementedError

    @classmethod
    def patch(cls, cal, event, fieldname, value):
        """Patch event from value."""
        raise NotImplementedError