
import typing
import re


class SBVCueBlock:
    '''Representation of a cue timing block.'''

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        '''
        Initialize.
        :param start: start time
        :param end: end time
        :param payload: caption text
        '''
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
        if len(lines) < 2:
            return False
        timing_pattern = re.compile(
            r'^\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}$')
        return bool(timing_pattern.match(lines[0]))

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        timing = lines[0].split(' --> ')
        start = timing[0].strip()
        end = timing[1].strip()
        payload = [line.strip() for line in lines[1:] if line.strip()]
        return cls(start, end, payload)
