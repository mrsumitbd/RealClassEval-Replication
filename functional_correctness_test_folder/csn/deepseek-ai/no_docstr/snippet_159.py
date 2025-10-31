
import typing


class Style:

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        if isinstance(text, str):
            self._text = [text]
        elif isinstance(text, list):
            self._text = text.copy()
        else:
            raise TypeError("Text must be a string or a list of strings")

    @property
    def text(self):
        return self._text.copy()
