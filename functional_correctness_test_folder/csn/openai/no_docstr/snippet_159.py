
import typing


class Style:
    def __init__(self, text: typing.Union[str, typing.List[str]]):
        if not isinstance(text, (str, list)):
            raise TypeError("text must be a str or a list of str")
        # Store the original value
        self._text = text

    @property
    def text(self) -> typing.Union[str, typing.List[str]]:
        """Return the stored text value."""
        return self._text
