
import typing


class Style:

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        if isinstance(text, list):
            self._text = ' '.join(text)
        else:
            self._text = text

    @property
    def text(self):
        return self._text
