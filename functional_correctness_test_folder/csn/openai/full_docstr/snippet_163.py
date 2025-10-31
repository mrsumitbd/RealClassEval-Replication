
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
        if not lines:
            return False
        # Must start with "STYLE" (case-sensitive)
        if lines[0].strip() != "STYLE":
            return False
        # Must end with an empty line
        if lines[-1] != "":
            return False
        # Must have at least one style line between header and trailing empty line
        if len(lines) < 3:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        '''
        Create a `WebVTTStyleBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTStyleBlock` instance
        '''
        text = "\n".join(lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        '''
        Return the lines for a style block.
        :param lines: style lines
        :returns: list of lines for a style block
        '''
        return ["STYLE"] + lines + [""]
