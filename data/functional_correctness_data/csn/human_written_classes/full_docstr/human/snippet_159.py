import typing

class Style:
    """Representation of a style."""

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        """Initialize.

        :param: text: the style text
        """
        self.lines = text.splitlines() if isinstance(text, str) else text
        self.comments: typing.List[str] = []

    @property
    def text(self):
        """Return the text of the style."""
        return '\n'.join(self.lines)