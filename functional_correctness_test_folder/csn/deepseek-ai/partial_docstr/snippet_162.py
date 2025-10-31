
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
        if not lines:
            return False
        return lines[0].strip() == 'NOTE' and (len(lines) == 1 or all(not line.strip().startswith('NOTE') for line in lines[1:]))

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
        text = '\n'.join(line.strip()
                         for line in lines_list[1:]) if len(lines_list) > 1 else ''
        return cls(text)

    @staticmethod
    def format_lines(comment: str) -> typing.List[str]:
        '''
        Return the lines for a comment block.
        :param comment: comment text
        :returns: list of lines for a comment block
        '''
        lines = ['NOTE']
        if comment:
            lines.extend(comment.split('\n'))
        return lines
