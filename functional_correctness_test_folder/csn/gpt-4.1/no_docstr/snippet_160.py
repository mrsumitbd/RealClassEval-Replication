
import typing
import re


class SBVCueBlock:

    TIMESTAMP_RE = re.compile(
        r'^(\d{1,2}):([0-5]\d):([0-5]\d)\.(\d{3}),(\d{1,2}):([0-5]\d):([0-5]\d)\.(\d{3})$'
    )

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines or len(lines) < 2:
            return False
        ts_line = lines[0].strip()
        if not cls.TIMESTAMP_RE.match(ts_line):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBV cue block")
        ts_line = lines[0].strip()
        m = cls.TIMESTAMP_RE.match(ts_line)
        start = f"{m.group(1)}:{m.group(2)}:{m.group(3)}.{m.group(4)}"
        end = f"{m.group(5)}:{m.group(6)}:{m.group(7)}.{m.group(8)}"
        payload = [line.rstrip('\n') for line in lines[1:]]
        return cls(start, end, payload)
