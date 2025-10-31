
import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        # Remove leading/trailing empty lines
        content = [line.strip('\r\n') for line in lines if line.strip('\r\n')]
        if not content:
            return False
        # First non-empty line must be "STYLE"
        if content[0].strip().upper() != "STYLE":
            return False
        # There must be at least one line after "STYLE"
        if len(content) < 2:
            return False
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        lines = list(lines)
        if not cls.is_valid(lines):
            raise ValueError("Invalid WebVTT style block")
        # Remove leading/trailing empty lines
        content = [line.rstrip('\r\n') for line in lines]
        # Find the first "STYLE" line
        start = 0
        while start < len(content) and content[start].strip() == '':
            start += 1
        # The rest is the style block
        text = '\n'.join(content[start:])
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        # Remove leading/trailing empty lines
        content = [line.rstrip('\r\n') for line in lines]
        while content and content[0].strip() == '':
            content.pop(0)
        while content and content[-1].strip() == '':
            content.pop()
        return content
