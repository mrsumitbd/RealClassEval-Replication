
import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        self.text = text.strip()

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        return len(lines) > 0 and lines[0].strip().startswith('::')

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        return cls('\n'.join(lines))

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        return [line.strip() for line in lines]
