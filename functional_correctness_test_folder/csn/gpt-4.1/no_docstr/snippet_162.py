
import typing


class WebVTTCommentBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if len(lines) < 2:
            return False
        if not lines[0].strip().lower() == "note":
            return False
        # A valid comment block ends with an empty line or is at the end of file
        # But for this method, just check it starts with NOTE
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid WebVTT comment block")
        # Remove the first line ("NOTE")
        comment_lines = lines[1:]
        # Remove trailing empty lines
        while comment_lines and comment_lines[-1].strip() == "":
            comment_lines.pop()
        text = "\n".join(comment_lines)
        return cls(text)

    @staticmethod
    def format_lines(text: str) -> typing.List[str]:
        result = ["NOTE"]
        if text:
            result.extend(text.splitlines())
        return result
