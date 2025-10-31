
import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        first_line = lines[0].strip()
        return first_line == "STYLE" or first_line.startswith("STYLE ")

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        lines_list = list(lines)
        if not cls.is_valid(lines_list):
            raise ValueError("Invalid WebVTT style block")
        text = "\n".join(lines_list[1:]) if len(lines_list) > 1 else ""
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        if not lines:
            return ["STYLE", ""]
        if lines[0].strip() != "STYLE":
            lines.insert(0, "STYLE")
        return lines
