
import typing


class WebVTTStyleBlock:
    '''Representation of a style block.'''

    def __init__(self, text: str):
        '''
        Initialize.
        :param text: style text
        '''
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a style block.
        :param lines: the lines to be validated
        :returns: true for a matching style block
        '''
        return len(lines) > 0 and lines[0].strip().upper() == 'STYLE'

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        '''
        Create a `WebVTTStyleBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTStyleBlock` instance
        '''
        lines = list(lines)
        if cls.is_valid(lines):
            return cls('\n'.join(lines[1:]).strip())
        raise ValueError("Invalid style block")

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        '''
        Return the lines for a style block.
        :param lines: style lines
        :returns: list of lines for a style block
        '''
        return ['STYLE'] + lines + ['']
