
import typing


class WebVTTCommentBlock:
    '''Representation of a comment block.'''

    def __init__(self, text: str):
        '''
        Initialize.
        :param text: comment text
        '''
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a comment block.
        :param lines: the lines to be validated
        :returns: true for a matching comment block
        '''
        if not lines:
            return False
        return lines[0].startswith('NOTE')

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid comment block lines")
        text = '\n'.join(lines[1:])
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        '''
        Return the lines for a comment block.
        :param lines: comment lines
        :returns: list of lines for a comment block
        '''
        formatted_lines = ['NOTE']
        formatted_lines.extend(lines.split('\n'))
        return formatted_lines
