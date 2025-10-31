
import typing
import re


class SRTCueBlock:

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        self.index = index
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a cue time block.
        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        '''
        if len(lines) < 3:
            return False

        # Check if the first line is a valid index
        if not re.match(r'^\d+$', lines[0].strip()):
            return False

        # Check if the second line is a valid timestamp
        timestamp_pattern = r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$'
        if not re.match(timestamp_pattern, lines[1].strip()):
            return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        index = lines[0].strip()
        start, end = lines[1].strip().split(' --> ')
        payload = [line.strip() for line in lines[2:] if line.strip()]
        return cls(index, start, end, payload)
