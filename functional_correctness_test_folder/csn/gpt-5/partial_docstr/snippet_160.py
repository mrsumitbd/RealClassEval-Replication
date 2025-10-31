import re
import typing


class SBVCueBlock:
    '''Representation of a cue timing block.'''
    _TIMING_RE = re.compile(
        r'^\s*(?P<start>\d+:\d{2}:\d{2}\.\d{3})\s*,\s*(?P<end>\d+:\d{2}:\d{2}\.\d{3})\s*$'
    )

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        first = lines[0].lstrip("\ufeff")  # handle BOM if present
        return cls._TIMING_RE.match(first) is not None

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not lines:
            raise ValueError("No lines provided for SBV cue block")
        timing_line = lines[0].lstrip("\ufeff")
        m = cls._TIMING_RE.match(timing_line)
        if not m:
            raise ValueError(f"Invalid SBV timing line: {timing_line!r}")
        start = m.group('start')
        end = m.group('end')
        payload = list(lines[1:])
        # Trim trailing empty lines from payload
        while payload and payload[-1].strip() == '':
            payload.pop()
        return cls(start, end, payload)
