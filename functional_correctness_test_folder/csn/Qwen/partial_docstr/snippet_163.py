
import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        return lines[0].strip() == 'STYLE'

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid WebVTT Style Block")
        return cls('\n'.join(lines[1:]))

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        if not lines or lines[0].strip() != 'STYLE':
            raise ValueError("Invalid WebVTT Style Block")
        return lines
