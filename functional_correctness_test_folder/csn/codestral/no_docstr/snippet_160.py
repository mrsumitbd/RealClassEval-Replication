
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
        if not lines[0].startswith('[') or not lines[0].endswith(']'):
            return False
        if not lines[-1].startswith('[') or not lines[-1].endswith(']'):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SBVCueBlock format")
        start = lines[0]
        end = lines[-1]
        payload = lines[1:-1]
        return cls(start, end, payload)
