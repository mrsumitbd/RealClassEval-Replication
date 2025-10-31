
import re
import typing


class SBVCueBlock:
    '''Representation of a cue timing block.'''

    _TIME_RE = re.compile(
        r'^\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*,\s*(\d{2}:\d{2}:\d{2}\.\d{3})\s*$')

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
        if not lines:
            return False
        return bool(cls._TIME_RE.match(lines[0]))

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Lines do not start with a valid SBV time cue")

        match = cls._TIME_RE.match(lines[0])
        start, end = match.group(1), match.group(2)

        # payload is everything after the first line until a blank line or end of list
        payload = []
        for line in lines[1:]:
            if line.strip() == '':
                break
            payload.append(line.rstrip('\n'))

        return cls(start, end, payload)
