import re
import typing


class SRTCueBlock:

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        if not isinstance(index, str):
            raise TypeError("index must be a string")
        if not isinstance(start, str) or not isinstance(end, str):
            raise TypeError("start and end must be strings")
        if not isinstance(payload, typing.Sequence):
            raise TypeError("payload must be a sequence of strings")
        self.index = index.strip()
        self.start = start.strip()
        self.end = end.strip()
        self.payload = [str(line) for line in payload]

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not isinstance(lines, typing.Sequence):
            return False
        if len(lines) < 3:
            return False
        idx_line = lines[0]
        time_line = lines[1]
        if not isinstance(idx_line, str) or not isinstance(time_line, str):
            return False
        if not re.match(r'^\s*\d+\s*$', idx_line):
            return False
        m = re.match(
            r'^\s*(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*$', time_line)
        if not m:
            return False
        # No strict validation on payload content; allow empty strings
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block lines")
        index = lines[0].strip()
        time_line = lines[1]
        m = re.match(
            r'^\s*(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*$', time_line)
        start, end = m.group(1), m.group(2)
        payload = list(lines[2:])
        return cls(index=index, start=start, end=end, payload=payload)
