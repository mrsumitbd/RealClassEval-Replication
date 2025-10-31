
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
        first_line = lines[0].strip()
        return first_line.startswith('NOTE') and (len(first_line) == 4 or first_line[4] in (' ', '\t'))

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        lines_list = list(lines)
        if not cls.is_valid(lines_list):
            raise ValueError("Invalid comment block lines")
        text = '\n'.join(line.strip() for line in lines_list[1:])
        return cls(text)

    @staticmethod
    def format_lines(text: str) -> typing.List[str]:
        '''
        Return the lines for a comment block.
        :param text: comment lines
        :returns: list of lines for a comment block
        '''
        lines = ['NOTE']
        if text:
            lines.extend(text.split('\n'))
        return lines
