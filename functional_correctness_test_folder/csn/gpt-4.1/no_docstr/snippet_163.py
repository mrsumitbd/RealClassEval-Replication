
import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        if lines[0].strip() != "STYLE":
            return False
        if len(lines) < 3:
            return False
        if lines[1].strip() != "":
            return False
        if lines[-1].strip() != "":
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid WebVTT STYLE block")
        # Extract lines between the empty line after STYLE and the last empty line
        style_lines = lines[2:-1]
        text = "\n".join(style_lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        # Remove leading/trailing empty lines
        while lines and lines[0].strip() == "":
            lines = lines[1:]
        while lines and lines[-1].strip() == "":
            lines = lines[:-1]
        return lines
