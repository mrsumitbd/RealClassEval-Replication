import re
import typing


class SBVCueBlock:
    '''Representation of a cue timing block.'''

    _TIME_RE = re.compile(
        r'^\s*(?P<start>(?:\d+:)?\d{1,2}:\d{2}\.\d{3})\s*,\s*(?P<end>(?:\d+:)?\d{1,2}:\d{2}\.\d{3})\s*$'
    )

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        '''
        Initialize.
        :param start: start time
        :param end: end time
        :param payload: caption text
        '''
        if not isinstance(start, str) or not isinstance(end, str):
            raise TypeError("start and end must be strings")
        if not isinstance(payload, typing.Sequence) or isinstance(payload, (str, bytes)):
            raise TypeError("payload must be a sequence of strings")
        self.start: str = start
        self.end: str = end
        self.payload: typing.List[str] = [str(line) for line in payload]

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a cue time block.
        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        '''
        if not isinstance(lines, typing.Sequence) or isinstance(lines, (str, bytes)):
            return False
        if len(lines) < 2:
            return False
        first = str(lines[0]).rstrip('\r\n')
        m = cls._TIME_RE.fullmatch(first)
        if not m:
            return False
        # Require at least one non-empty payload line
        for l in lines[1:]:
            if str(l).strip() != '':
                return True
        return False

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        '''
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError("Lines do not form a valid SBV cue block")
        first = str(lines[0]).rstrip('\r\n')
        m = cls._TIME_RE.fullmatch(first)
        assert m is not None
        start = m.group('start')
        end = m.group('end')
        payload = [str(l).rstrip('\r\n') for l in lines[1:]]
        return cls(start, end, payload)
