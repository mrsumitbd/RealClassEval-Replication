
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        if lines[0].strip() != "NOTE":
            return False
        # A valid comment block is at least one line: "NOTE"
        # It may have more lines (the comment text)
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid WebVTT comment block")
        # The first line is "NOTE", the rest is the comment text
        comment_lines = lines[1:]
        text = "\n".join(comment_lines)
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        # lines is the comment text (may be multiline string)
        result = ["NOTE"]
        if lines:
            result.extend(lines.splitlines())
        return result
