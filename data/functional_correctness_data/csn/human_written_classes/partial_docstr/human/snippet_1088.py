class SimpleRecord:
    """A record with simply level name and number, and just a string message."""

    def __init__(self, *, levelname, levelno, message):
        self.levelname = levelname
        self.levelno = levelno
        self.message = message
        self.extra_fields = {}

    @property
    def repr_content(self):
        """Representation of the content to show in messages."""
        return repr(self.message)

    def __str__(self):
        return f'<SimpleRecord [{self.levelname}] {self.message!r}>'