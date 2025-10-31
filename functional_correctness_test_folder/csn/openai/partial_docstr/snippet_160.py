
import typing
import re
from datetime import timedelta


class SBVCueBlock:
    '''Representation of a cue timing block.'''
    _TIMESTAMP_RE = re.compile(
        r'^\s*(\d+:\d{2}:\d{2}\.\d{2})\s*,\s*(\d+:\d{2}:\d{2}\.\d{2})\s*$')

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = list(payload)

    @staticmethod
    def _parse_timestamp(ts: str) -> float:
        """Convert hh:mm:ss.xx to seconds."""
        h, m, s = ts.split(':')
        sec, frac = s.split('.')
        return (
            int(h) * 3600
            + int(m) * 60
            + int(sec)
            + int(frac) / 100
        )

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        first = lines[0]
        m = cls._TIMESTAMP_RE.match(first)
        if not m:
            return False
        start_ts, end_ts = m.group(1), m.group(2)
        try:
            start_sec = cls._parse_timestamp(start_ts)
            end_sec = cls._parse_timestamp(end_ts)
        except Exception:
            return False
        if start_sec >= end_sec:
            return False
        # payload must exist (at least one line after the timestamp line)
        if len(lines) < 2:
            return False
        # allow empty payload lines? require at least one non-empty line
        payload_lines = [l for l in lines[1:] if l.strip() != '']
        return len(payload_lines) > 0

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        """
        Create a `SBVCueBlock` from lines of text.
        :param lines: the lines of text
        :returns: `SBVCueBlock` instance
        """
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBV cue block")
        first = lines[0]
        m = cls._TIMESTAMP_RE.match(first)
        start_ts, end_ts = m.group(1), m.group(2)
        # payload lines are all lines after the first until a blank line or end
        payload = []
        for line in lines[1:]:
            if line.strip() == '':
                break
            payload.append(line.rstrip('\n'))
        return cls(start_ts, end_ts, payload)
