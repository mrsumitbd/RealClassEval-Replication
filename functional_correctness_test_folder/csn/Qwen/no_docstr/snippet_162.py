
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        return len(lines) == 1 and lines[0].startswith('NOTE ')

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        lines = list(lines)
        if cls.is_valid(lines):
            return cls(lines[0][5:].strip())
        raise ValueError("Invalid WebVTT comment block")

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        return [f"NOTE {lines}"]
