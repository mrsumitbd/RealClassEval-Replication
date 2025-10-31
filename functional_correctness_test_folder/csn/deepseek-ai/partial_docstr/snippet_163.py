
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
        '''
        Create a `WebVTTStyleBlock` from lines of text.
        :param lines: the lines of text
        :returns: `WebVTTStyleBlock` instance
        '''
        lines_list = list(lines)
        if not cls.is_valid(lines_list):
            raise ValueError("Invalid WebVTT style block")
        text = "\n".join(lines_list)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        if not lines:
            return []
        formatted_lines = []
        for line in lines:
            stripped_line = line.strip()
            if stripped_line:
                formatted_lines.append(stripped_line)
        return formatted_lines
