
import typing
import re


class SBVCueBlock:

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 3:
            return False
        time_pattern = re.compile(
            r'\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}')
        if not time_pattern.match(lines[0]):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid lines for SBVCueBlock")
        start, end = lines[0].split(' --> ')
        payload = lines[1:]
        return cls(start, end, payload)
