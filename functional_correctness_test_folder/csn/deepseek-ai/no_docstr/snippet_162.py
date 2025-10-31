
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 2:
            return False
        if not lines[0].strip() == "NOTE":
            return False
        if not lines[-1].strip() == "":
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        if not cls.is_valid(list(lines)):
            raise ValueError("Invalid WebVTT comment block format")
        text = "\n".join(line.strip() for line in list(lines)[1:-1])
        return cls(text)

    @staticmethod
    def format_lines(text: str) -> typing.List[str]:
        lines = ["NOTE"]
        if text:
            lines.extend(text.split("\n"))
        lines.append("")
        return lines
