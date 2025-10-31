
import typing
import re


class SBVCueBlock:
    """
    Represents a single cue block in the SBV subtitle format.

    A cue block consists of a start and end timestamp on the first line,
    followed by one or more lines of subtitle text.
    """

    _TIMESTAMP_RE = re.compile(
        r"""
        ^\s*
        (?P<hours>\d{1,2})?          # optional hours
        :(?P<minutes>\d{2})          # minutes
        :(?P<seconds>\d{2})          # seconds
        \.(?P<milliseconds>\d{3})    # milliseconds
        \s*$
        """,
        re.VERBOSE,
    )

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def _is_timestamp(cls, ts: str) -> bool:
        """Return True if ts matches the SBV timestamp format."""
        return bool(cls._TIMESTAMP_RE.match(ts))

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate that the given lines form a proper SBV cue block.

        A valid block must have at least two lines:
        * The first line contains a start and end timestamp separated by a comma.
        * Both timestamps must match the SBV format.
        """
        if not lines or len(lines) < 2:
            return False

        header = lines[0].strip()
        if ',' not in header:
            return False

        start, end = [part.strip() for part in header.split(',', 1)]
        if not (cls._is_timestamp(start) and cls._is_timestamp(end)):
            return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        """
        Parse a sequence of lines into an SBVCueBlock instance.

        Raises ValueError if the lines do not form a valid cue block.
        """
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBV cue block")

        header = lines[0].strip()
        start, end = [part.strip() for part in header.split(',', 1)]
        payload = [line.rstrip('\n') for line in lines[1:]]
        return cls(start, end, payload)

    def __repr__(self) -> str:
        payload_repr = '\\n'.join(self.payload)
        return f"SBVCueBlock(start={self.start!r}, end={self.end!r}, payload=[{payload_repr!r}])"
