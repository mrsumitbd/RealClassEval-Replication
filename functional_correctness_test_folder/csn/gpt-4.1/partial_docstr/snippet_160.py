
import typing
import re


class SBVCueBlock:
    '''Representation of a cue timing block.'''
    TIMING_RE = re.compile(
        r'^(\d{2}:\d{2}:\d{2}\.\d{3}),(\d{2}:\d{2}:\d{2}\.\d{3})$')

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines or len(lines) < 2:
            return False
        m = cls.TIMING_RE.match(lines[0].strip())
        return m is not None

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBVCueBlock lines")
        m = cls.TIMING_RE.match(lines[0].strip())
        start, end = m.group(1), m.group(2)
        payload = [line.rstrip('\n') for line in lines[1:]]
        return cls(start, end, payload)
