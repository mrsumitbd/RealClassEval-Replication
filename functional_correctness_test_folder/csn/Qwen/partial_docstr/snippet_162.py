
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        return len(lines) > 0 and all(line.startswith('NOTE') for line in lines)

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        text = ' '.join(line[5:].strip()
                        for line in lines if line.startswith('NOTE'))
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        return [f'NOTE {line}' for line in lines.split('\n') if line.strip()]
