
import typing
import re
from datetime import datetime


class SBVCueBlock:
    '''Representation of a cue timing block.'''

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 3:
            return False
        match = re.match(
            r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', lines[0])
        if not match:
            return False
        try:
            datetime.strptime(match.group(1), '%H:%M:%S.%f')
            datetime.strptime(match.group(2), '%H:%M:%S.%f')
        except ValueError:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        match = re.match(
            r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})', lines[0])
        start = match.group(1)
        end = match.group(2)
        payload = [line.strip() for line in lines[1:] if line.strip()]
        return cls(start, end, payload)
