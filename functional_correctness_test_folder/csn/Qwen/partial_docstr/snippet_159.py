
import typing


class Style:
    '''Representation of a style.'''

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        '''Initialize.
        :param: text: the style text
        '''
        if isinstance(text, list):
            self._text = ' '.join(text)
        else:
            self._text = text

    @property
    def text(self) -> str:
        return self._text
