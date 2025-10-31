
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
        formatted_lines = cls.format_lines(list(lines))
        text = '\n'.join(formatted_lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        if not lines or lines[0].strip() != 'STYLE':
            return []
        return [line.strip() for line in lines if line.strip()]
