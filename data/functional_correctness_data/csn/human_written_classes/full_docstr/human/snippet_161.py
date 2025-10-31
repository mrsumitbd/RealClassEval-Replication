import typing
import re

class SRTCueBlock:
    """Representation of a cue timing block."""
    CUE_TIMINGS_PATTERN = re.compile('\\s*(\\d+:\\d{2}:\\d{2},\\d{3})\\s*-->\\s*(\\d+:\\d{2}:\\d{2},\\d{3})')

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        """
        Initialize.

        :param start: start time
        :param end: end time
        :param payload: caption text
        """
        self.index = index
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate the lines for a match of a cue time block.

        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        """
        return bool(len(lines) >= 3 and lines[0].isdigit() and re.match(cls.CUE_TIMINGS_PATTERN, lines[1]))

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        """
        Create a `SRTCueBlock` from lines of text.

        :param lines: the lines of text
        :returns: `SRTCueBlock` instance
        """
        index = lines[0]
        match = re.match(cls.CUE_TIMINGS_PATTERN, lines[1])
        assert match is not None
        payload = lines[2:]
        return cls(index, match.group(1), match.group(2), payload)