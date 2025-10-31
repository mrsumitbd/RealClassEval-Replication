import typing


class Style:
    '''Representation of a style.'''

    def __init__(self, text: typing.Union[str, typing.List[str]]):
        '''Initialize.
        :param: text: the style text
        '''
        if isinstance(text, str):
            self._text = text
        elif isinstance(text, list):
            if not all(isinstance(item, str) for item in text):
                raise TypeError("All items in the list must be strings.")
            self._text = "\n".join(text)
        else:
            raise TypeError("text must be a string or a list of strings.")

    @property
    def text(self):
        return self._text
