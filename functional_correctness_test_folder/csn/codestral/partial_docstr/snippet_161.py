
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

        start, end = lines[1].split('-->')
        if not cls._is_valid_time(start.strip()) or not cls._is_valid_time(end.strip()):
            return False

        return True

    @classmethod
    def _is_valid_time(cls, time_str: str) -> bool:
        parts = time_str.split(':')
        if len(parts) != 3:
            return False

        if not all(part.isdigit() for part in parts):
            return False

        hours, minutes, seconds = parts
        if not (0 <= int(hours) <= 99):
            return False

        if not (0 <= int(minutes) <= 59):
            return False

        if not (0 <= int(seconds.split(',')[0]) <= 59):
            return False

        if len(seconds.split(',')) == 2 and not (0 <= int(seconds.split(',')[1]) <= 999):
            return False

        return True

    @classmethod
    def from_lines(cls, lines: typing.Sequence[str]) -> 'SRTCueBlock':
        if not cls.is_valid(lines):
            raise ValueError("Invalid lines for SRTCueBlock")

        index = lines[0].strip()
        start, end = lines[1].split('-->')
        start = start.strip()
        end = end.strip()
        payload = lines[2:]

        return cls(index, start, end, payload)
