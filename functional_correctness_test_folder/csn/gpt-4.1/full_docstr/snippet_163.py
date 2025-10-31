
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
        if lines[0].strip().upper() != "STYLE":
            return False
        # Must have at least one line after "STYLE"
        if len(lines) < 2:
            return False
        # All lines after "STYLE" should be non-empty or whitespace (CSS can be empty)
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        '''
        Create a `WebVTTStyleBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTStyleBlock` instance
        '''
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid style block")
        # Join all lines after the first ("STYLE") as the style text
        style_text = "\n".join(lines[1:]).rstrip('\n')
        return cls(style_text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        '''
        Return the lines for a style block.
        :param lines: style lines
        :returns: list of lines for a style block
        '''
        return ["STYLE"] + lines
