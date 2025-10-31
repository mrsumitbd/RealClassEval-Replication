class StructRecord:
    """A record with level name and number, and info structured in different fields."""

    def __init__(self, *, levelname, levelno, event_dict):
        self.levelname = levelname
        self.levelno = levelno
        data = event_dict.copy()
        self.message = data.pop('event')
        self.extra_fields = data

    @property
    def repr_content(self):
        """Representation of the content to show in messages."""
        result = repr(self.message)
        if self.extra_fields:
            result += f' {self.extra_fields}'
        return result

    def __str__(self):
        return f'<StructRecord [{self.levelname}] {self.message!r} {self.extra_fields}>'