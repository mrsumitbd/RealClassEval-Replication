
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
        if len(lines) < 3:
            return False
        try:
            int(lines[0])
            time_range = lines[1].split(' --> ')
            start_time, end_time = time_range
            re.match(r'\d{2}:\d{2}:\d{2},\d{3}', start_time)
            re.match(r'\d{2}:\d{2}:\d{2},\d{3}', end_time)
            return True
        except (ValueError, IndexError, AttributeError):
            return False

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block")
        index = lines[0]
        start, end = lines[1].split(' --> ')
        payload = lines[2:]
        return cls(index, start, end, payload)
