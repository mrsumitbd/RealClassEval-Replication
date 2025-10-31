
import typing
import re


class SBVCueBlock:
    '''Representation of a cue timing block.'''

    TIME_PATTERN = re.compile(
        r'^\d{1,2}:\d{2}:\d{2}\.\d{3},\d{1,2}:\d{2}:\d{2}\.\d{3}$')

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        '''
        Initialize.
        :param start: start time
        :param end: end time
        :param payload: caption text
        '''
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
        if not lines or len(lines) < 2:
            return False
        first = lines[0].strip()
        if not cls.TIME_PATTERN.match(first):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBV cue block lines")
        times = lines[0].strip().split(',')
        start = times[0].strip()
        end = times[1].strip()
        payload = [line.rstrip('\n') for line in lines[1:]]
        return cls(start, end, payload)
