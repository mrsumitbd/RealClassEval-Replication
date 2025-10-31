import re
import typing


class SBVCueBlock:
    _TIMECODE_RE = re.compile(
        r'^\s*(\d+):([0-5]?\d):([0-5]?\d)\.(\d{1,3})\s*,\s*(\d+):([0-5]?\d):([0-5]?\d)\.(\d{1,3})\s*$'
    )

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        if not isinstance(start, str) or not isinstance(end, str):
            raise TypeError("start and end must be strings")
        if not isinstance(payload, typing.Sequence):
            raise TypeError("payload must be a sequence of strings")
        for line in payload:
            if not isinstance(line, str):
                raise TypeError("all payload lines must be strings")
        # Validate timecodes format
        header = f"{start},{end}"
        if not self._TIMECODE_RE.match(header):
            raise ValueError("Invalid SBV timecode format for start/end")
        self.start = start.strip()
        self.end = end.strip()
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not isinstance(lines, typing.Sequence):
            return False
        if len(lines) < 2:
            return False
        header = lines[0]
        if not isinstance(header, str):
            return False
        if not cls._TIMECODE_RE.match(header):
            return False
        # Ensure remaining are strings
        for line in lines[1:]:
            if not isinstance(line, str):
                return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBV cue block")
        header = lines[0].strip()
        m = cls._TIMECODE_RE.match(header)
        assert m is not None
        # Reconstruct start and end exactly as in header groups to preserve formatting
        start = f"{m.group(1)}:{m.group(2)}:{m.group(3)}.{m.group(4)}"
        end = f"{m.group(5)}:{m.group(6)}:{m.group(7)}.{m.group(8)}"
        payload = list(lines[1:])
        return cls(start, end, payload)
