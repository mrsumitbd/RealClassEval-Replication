
import typing


class Style:
    '''Representation of a style.'''

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        '''Initialize.
        :param: text: the style text
        '''
        if isinstance(text, str):
            self._text = [text]
        elif isinstance(text, list) and all(isinstance(item, str) for item in text):
            self._text = text
        else:
            raise TypeError("text must be a string or a list of strings")

    @property
    def text(self):
        if len(self._text) == 1:
            return self._text[0]
        return self._text
