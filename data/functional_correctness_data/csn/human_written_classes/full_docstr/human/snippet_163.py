import re
import typing

class WebVTTStyleBlock:
    """Representation of a style block."""
    STYLE_PATTERN = re.compile('STYLE\\s(.*?)\\Z', re.DOTALL)

    def __init__(self, text: str):
        """
        Initialize.

        :param text: style text
        """
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate the lines for a match of a style block.

        :param lines: the lines to be validated
        :returns: true for a matching style block
        """
        return len(lines) >= 2 and lines[0] == 'STYLE' and (not any((line.strip() == '' or '-->' in line for line in lines)))

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        """
        Create a `WebVTTStyleBlock` from lines of text.

        :param lines: the lines of text
        :returns: `WebVTTStyleBlock` instance
        """
        match = cls.STYLE_PATTERN.match('\n'.join(lines))
        return cls(text=match.group(1).strip() if match else '')

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        """
        Return the lines for a style block.

        :param lines: style lines
        :returns: list of lines for a style block
        """
        return ['STYLE', *lines]