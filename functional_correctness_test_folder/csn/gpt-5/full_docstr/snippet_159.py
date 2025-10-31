import typing


class Style:
    '''Representation of a style.'''

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        '''Initialize.
        :param: text: the style text
        '''
        if isinstance(text, list):
            if not all(isinstance(t, str) for t in text):
                raise TypeError("All items in the text list must be strings.")
            self._text = "\n".join(text)
        elif isinstance(text, str):
            self._text = text
        else:
            raise TypeError("text must be a string or a list of strings.")

    @property
    def text(self):
        '''Return the text of the style.'''
        return self._text
