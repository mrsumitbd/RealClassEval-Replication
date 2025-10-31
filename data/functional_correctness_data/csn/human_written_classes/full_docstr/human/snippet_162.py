import typing
import re

class WebVTTCommentBlock:
    """Representation of a comment block."""
    COMMENT_PATTERN = re.compile('NOTE\\s(.*?)\\Z', re.DOTALL)

    def __init__(self, text: str):
        """
        Initialize.

        :param text: comment text
        """
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate the lines for a match of a comment block.

        :param lines: the lines to be validated
        :returns: true for a matching comment block
        """
        return bool(lines and lines[0].startswith('NOTE'))

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        """
        Create a `WebVTTCommentBlock` from lines of text.

        :param lines: the lines of text
        :returns: `WebVTTCommentBlock` instance
        """
        match = cls.COMMENT_PATTERN.match('\n'.join(lines))
        return cls(text=match.group(1).strip() if match else '')

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        """
        Return the lines for a comment block.

        :param lines: comment lines
        :returns: list of lines for a comment block
        """
        list_of_lines = lines.split('\n')
        if len(list_of_lines) == 1:
            return [f'NOTE {lines}']
        return ['NOTE', *list_of_lines]