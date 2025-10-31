
import typing
import re


class SBVCueBlock:

    def __init__(self, start: str, end: str, payload: typing.Sequence[str]):
        self.start = start
        self.end = end
        self.payload = payload

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 3:
            return False
        if not re.match(r'^CUE\s+(\d{2}:\d{2}:\d{2}\.\d{2,3})$', lines[0]):
            return False
        if not re.match(r'^CUE\s+(\d{2}:\d{2}:\d{2}\.\d{2,3})$', lines[-1]):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SBVCueBlock':
        start_match = re.match(
            r'^CUE\s+(\d{2}:\d{2}:\d{2}\.\d{2,3})$', lines[0])
        end_match = re.match(
            r'^CUE\s+(\d{2}:\d{2}:\d{2}\.\d{2,3})$', lines[-1])
        if start_match and end_match:
            start = start_match.group(1)
            end = end_match.group(1)
            payload = lines[1:-1]
            return cls(start, end, payload)
        else:
            raise ValueError("Invalid SBV cue block")
