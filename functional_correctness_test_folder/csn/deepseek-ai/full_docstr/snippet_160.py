
import typing


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
        time_line = lines[0].strip()
        if '-->' not in time_line:
            return False
        times = time_line.split('-->')
        if len(times) != 2:
            return False
        start, end = times[0].strip(), times[1].strip()
        return len(start) > 0 and len(end) > 0

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Invalid cue block lines")
        time_line = lines[0].strip()
        start, end = [t.strip() for t in time_line.split('-->')]
        payload = [line.strip() for line in lines[1:] if line.strip()]
        return cls(start, end, payload)
