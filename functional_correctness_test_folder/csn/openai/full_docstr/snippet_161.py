
import re
import typing


class SRTCueBlock:
    '''Representation of a cue timing block.'''

    TIME_RE = re.compile(
        r'^\d{2}:\d{2}:\d{2},\d{3}\s*-->\s*\d{2}:\d{2}:\d{2},\d{3}$')
    INDEX_RE = re.compile(r'^\d+$')

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
        if len(lines) < 3:
            return False
        index_line = lines[0].strip()
        time_line = lines[1].strip()
        if not cls.INDEX_RE.match(index_line):
            return False
        if not cls.TIME_RE.match(time_line):
            return False
        # payload must contain at least one non‑empty line
        payload_lines = [l for l in lines[2:] if l.strip() != '']
        if not payload_lines:
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
            raise ValueError("Lines do not form a valid SRT cue block")
        index = lines[0].strip()
        time_line = lines[1].strip()
        start, end = [t.strip() for t in time_line.split('-->')]
        payload = [l.rstrip('\n') for l in lines[2:]]
        return cls(index, start, end, payload)
