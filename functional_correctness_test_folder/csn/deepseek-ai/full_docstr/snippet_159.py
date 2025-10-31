
import typing


class Style:
    '''Representation of a style.'''

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        '''Initialize.
        :param: text: the style text
        '''
        if isinstance(text, str):
            self._text = [text]
        else:
            self._text = list(text)

    @property
    def text(self):
        '''Return the text of the style.'''
        return self._text
