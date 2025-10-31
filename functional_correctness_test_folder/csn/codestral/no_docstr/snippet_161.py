
import typing


class SRTCueBlock:

    def __init__(self, index: str, start: str, end: str, payload: typing.Sequence[str]):
        self.index = index
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 3:
            return False
        if not lines[0].strip().isdigit():
            return False
        if '-->' not in lines[1]:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid SRT cue block")
        index = lines[0].strip()
        start, end = lines[1].split('-->')
        start = start.strip()
        end = end.strip()
        payload = lines[2:]
        return cls(index, start, end, payload)
