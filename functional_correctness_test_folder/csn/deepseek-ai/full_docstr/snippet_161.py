
import typing


class SRTCueBlock:
    '''Representation of a cue timing block.'''

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
        time_line = lines[1].strip()
        if '-->' not in time_line:
            return False
        time_parts = time_line.split('-->')
        if len(time_parts) != 2:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        '''
        Create a `SRTCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SRTCueBlock` instance
        '''
        index = lines[0].strip()
        time_line = lines[1].strip()
        start, end = map(str.strip, time_line.split('-->'))
        payload = [line.strip() for line in lines[2:] if line.strip()]
        return cls(index, start, end, payload)
