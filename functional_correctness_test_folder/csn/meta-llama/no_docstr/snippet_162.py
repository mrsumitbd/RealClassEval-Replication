
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        return len(lines) > 0 and all(line.strip().startswith('NOTE') or (i > 0 and line.strip() == '') for i, line in enumerate(lines))

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        text = '\n'.join(line.strip() for line in lines if line.strip() != '')
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        formatted_lines = ['NOTE']
        for line in lines.split('\n'):
            if line.strip() != '':
                formatted_lines.append(line.strip())
        if len(formatted_lines) == 1:
            formatted_lines.append('')
        return formatted_lines
