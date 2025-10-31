
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
        if not lines or len(lines) < 2:
            return False
        if lines[0].strip() != "NOTE":
            return False
        # A comment block ends at the first blank line or at the end of lines
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        '''
        Create a `WebVTTCommentBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        '''
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid comment block")
        # Remove the first line ("NOTE")
        comment_lines = lines[1:]
        # Remove trailing blank lines
        while comment_lines and comment_lines[-1].strip() == "":
            comment_lines.pop()
        text = "\n".join(comment_lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        '''
        Return the lines for a comment block.
        :param lines: comment lines
        :returns: list of lines for a comment block
        '''
        result = ["NOTE"]
        if lines:
            result.extend(lines.splitlines())
        return result
