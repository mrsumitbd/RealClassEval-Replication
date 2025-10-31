import re
import typing


class SRTCueBlock:
    _TIMELINE_RE = re.compile(
        r'^\s*(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})(?:\s*.*)?$'
    )

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        self.index = str(index).strip()
        self.start = str(start).strip()
        self.end = str(end).strip()
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines or len(lines) < 3:
            return False
        idx = lines[0].strip()
        if not idx.isdigit():
            return False
        m = cls._TIMELINE_RE.match(lines[1].rstrip("\n"))
        if not m:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block lines")
        index = lines[0].strip()
        m = cls._TIMELINE_RE.match(lines[1].rstrip("\n"))
        start, end = m.group(1), m.group(2)
        payload = list(lines[2:])
        # Remove a trailing empty line if present (common separator)
        while payload and payload[-1].strip() == '':
            payload.pop()
        return cls(index=index, start=start, end=end, payload=payload)
