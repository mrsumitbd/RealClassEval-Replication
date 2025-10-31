
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
        if not lines[1].strip().startswith("::cue"):
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':

        lines_list = list(lines)
        if not cls.is_valid(lines_list):
            raise ValueError("Invalid WebVTT Style Block")
        text = "\n".join(lines_list)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:

        formatted_lines = []
        for line in lines:
            formatted_lines.append(line.strip())
        return formatted_lines
