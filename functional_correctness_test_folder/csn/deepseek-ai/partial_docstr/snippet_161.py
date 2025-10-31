
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
        if len(lines) < 2:
            return False
        index_line = lines[0].strip()
        time_line = lines[1].strip()
        if not index_line.isdigit():
            return False
        time_pattern = r'^\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}$'
        if not re.match(time_pattern, time_line):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block format")
        index = lines[0].strip()
        time_line = lines[1].strip()
        start, end = time_line.split(' --> ')
        payload = [line.strip() for line in lines[2:] if line.strip()]
        return cls(index, start, end, payload)
