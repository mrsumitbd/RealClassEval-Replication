
import re
import typing


class SRTCueBlock:
    TIME_PATTERN = re.compile(
        r'^\s*(\d{2}:\d{2}:\d{2},\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2},\d{3})\s*$'
    )

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        self.index = index
        self.start = start
        self.end = end
        self.payload = list(payload)

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        """
        Validate the lines for a match of a cue time block.
        :param lines: the lines to be validated
        :returns: true for a matching cue time block
        """
        if not lines or len(lines) < 3:
            return False

        # Index line must be digits only
        if not lines[0].strip().isdigit():
            return False

        # Time line must match the pattern
        if not cls.TIME_PATTERN.match(lines[1]):
            return False

        # Payload must contain at least one non-empty line
        payload_lines = [l for l in lines[2:] if l.strip() != '']
        if not payload_lines:
            return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        """
        Construct an SRTCueBlock from a sequence of lines.
        Assumes that the lines are already validated.
        """
        index = lines[0].strip()
        time_match = cls.TIME_PATTERN.match(lines[1])
        if not time_match:
            raise ValueError("Invalid time format in cue block")

        start, end = time_match.group(1), time_match.group(2)

        # Payload: all lines after the time line until a blank line or end
        payload = []
        for line in lines[2:]:
            if line.strip() == '':
                break
            payload.append(line.rstrip())

        return cls(index, start, end, payload)
