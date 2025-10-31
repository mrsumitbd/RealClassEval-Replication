
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a comment block.
        :param lines: the lines to be validated
        :returns: true for a matching comment block
        '''
        return len(lines) > 0 and lines[0].strip() == 'NOTE'

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        text = '\n'.join(line.rstrip() for line in lines[1:] if line.strip())
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
