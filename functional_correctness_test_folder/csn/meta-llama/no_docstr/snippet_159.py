
import typing


class Style:

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        if isinstance(text, str):
            self._text = [text]
        elif isinstance(text, list) and all(isinstance(item, str) for item in text):
            self._text = text
        else:
            raise TypeError("Input must be a string or a list of strings")

    @property
    def text(self):
        return self._text
