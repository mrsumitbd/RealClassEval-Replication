
import typing


class Style:
    '''Representation of a style.'''

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        '''Initialize.
        :param: text: the style text
        '''
        if isinstance(text, list):
            self._text = ' '.join(str(t) for t in text)
        else:
            self._text = str(text)

    @property
    def text(self):
        return self._text
