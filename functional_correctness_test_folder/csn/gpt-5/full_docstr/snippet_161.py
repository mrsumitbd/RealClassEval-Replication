import re
import typing


class SRTCueBlock:
    '''Representation of a cue timing block.'''

    _TIME_RE = r'(?P<h>\d{2}):(?P<m>[0-5]\d):(?P<s>[0-5]\d),(?P<ms>\d{3})'
    _CUE_RE = re.compile(r'^\s*(?P<start>' + _TIME_RE +
                         r')\s*-->\s*(?P<end>' + _TIME_RE + r')\s*$')

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        '''
        Initialize.
        :param start: start time
        :param end: end time
        :param payload: caption text
        '''
        self.index = str(index).strip()
        self.start = start.strip()
        self.end = end.strip()
        self.payload = [str(line).rstrip('\r\n') for line in payload]

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        '''
        Validate the lines for a match of a cue time block.
        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        '''
        if not lines or len(lines) < 2:
            return False
        try:
            idx = str(lines[0]).strip()
            if not idx.isdigit():
                return False
            cue_line = str(lines[1]).strip()
            return cls._CUE_RE.match(cue_line) is not None
        except Exception:
            return False

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        '''
        Create a `SRTCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SRTCueBlock` instance
        '''
        if not cls.is_valid(lines):
            raise ValueError('Invalid SRT cue block')
        index = str(lines[0]).strip()
        m = cls._CUE_RE.match(str(lines[1]).strip())
        assert m is not None
        start = m.group('start')
        end = m.group('end')
        payload = [str(l).rstrip('\r\n') for l in lines[2:]]
        return cls(index=index, start=start, end=end, payload=payload)
