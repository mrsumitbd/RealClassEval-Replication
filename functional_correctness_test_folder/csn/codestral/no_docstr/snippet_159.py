
import typing


class Style:

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        self._text = text

    @property
    def text(self):
        return self._text
