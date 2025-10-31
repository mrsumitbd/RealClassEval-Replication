
import typing
import re


class SRTCueBlock:
    '''Representation of a cue timing block.'''

    TIME_PATTERN = re.compile(
        r'(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})'
    )

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        '''
        Initialize.
        :param start: start time
        :param end: end time
        :param payload: caption text
        '''
        self.index = index
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a cue time block.
        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        '''
        if not lines or len(lines) < 3:
            return False
        if not lines[0].strip().isdigit():
            return False
        if not cls.TIME_PATTERN.match(lines[1].strip()):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        '''
        Create a `SRTCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SRTCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block lines")
        index = lines[0].strip()
        match = cls.TIME_PATTERN.match(lines[1].strip())
        start = f"{match.group(1)}:{match.group(2)}:{match.group(3)},{match.group(4)}"
        end = f"{match.group(5)}:{match.group(6)}:{match.group(7)},{match.group(8)}"
        payload = lines[2:]
        return cls(index, start, end, payload)
