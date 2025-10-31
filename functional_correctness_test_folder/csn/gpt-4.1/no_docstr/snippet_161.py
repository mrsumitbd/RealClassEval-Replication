
import typing
import re


class SRTCueBlock:

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        self.index = index
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines or len(lines) < 3:
            return False
        # First line: index (should be integer)
        if not lines[0].strip().isdigit():
            return False
        # Second line: timecode
        timecode_line = lines[1].strip()
        timecode_pattern = r"^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$"
        if not re.match(timecode_pattern, timecode_line):
            return False
        # At least one payload line
        if len(lines[2:]) < 1:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block")
        index = lines[0].strip()
        timecode_line = lines[1].strip()
        start, end = [t.strip() for t in timecode_line.split('-->')]
        payload = [line.rstrip('\n') for line in lines[2:]]
        return cls(index, start, end, payload)
