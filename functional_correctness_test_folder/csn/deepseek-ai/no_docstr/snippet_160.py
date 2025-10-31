
import typing


class SBVCueBlock:

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 2:
            return False
        first_line = lines[0].strip()
        if not (first_line.startswith('[') and first_line.endswith(']')):
            return False
        time_parts = first_line[1:-1].split(' --> ')
        if len(time_parts) != 2:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBV cue block format")
        first_line = lines[0].strip()
        time_parts = first_line[1:-1].split(' --> ')
        start, end = time_parts[0], time_parts[1]
        payload = [line.strip() for line in lines[1:] if line.strip()]
        return cls(start, end, payload)
