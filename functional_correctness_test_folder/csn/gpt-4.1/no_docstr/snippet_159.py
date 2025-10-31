
import typing


class Style:

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        if isinstance(text, str):
            self._text = text
        elif isinstance(text, list):
            self._text = ''.join(str(t) for t in text)
        else:
            raise TypeError("text must be a string or a list of strings")

    @property
    def text(self):
        return self._text
