
import typing
import re


class SRTCueBlock:
    _time_re = re.compile(r'^\d{2}:\d{2}:\d{2},\d{3}$')
    _time_range_re = re.compile(
        r'^(?P<start>\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(?P<end>\d{2}:\d{2}:\d{2},\d{3})$')

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        self.index = index
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate that the given lines represent a correct SRT cue block.
        """
        if not lines or len(lines) < 3:
            return False

        # 1st line: numeric index
        if not lines[0].isdigit():
            return False

        # 2nd line: time range
        match = cls._time_range_re.match(lines[1])
        if not match:
            return False

        # Validate start and end times
        if not (cls._time_re.match(match.group('start')) and cls._time_re.match(match.group('end'))):
            return False

        # At least one payload line
        if len(lines) == 3 and lines[2] == '':
            return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        """
        Parse a sequence of lines into an SRTCueBlock instance.
        Raises ValueError if the lines are not a valid block.
        """
        if not cls.is_valid(lines):
            raise ValueError(
                "Provided lines do not form a valid SRT cue block")

        index = lines[0]
        time_line = lines[1]
        match = cls._time_range_re.match(time_line)
        start = match.group('start')
        end = match.group('end')
        payload = lines[2:]  # may contain multiple lines

        return cls(index, start, end, payload)
