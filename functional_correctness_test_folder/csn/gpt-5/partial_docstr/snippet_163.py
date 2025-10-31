import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        if not isinstance(text, str):
            raise TypeError("text must be a string")
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        # Normalize lines: strip line endings
        norm = [("" if s is None else str(s)).rstrip("\r\n") for s in lines]
        # Skip leading empty lines
        i = 0
        while i < len(norm) and norm[i].strip() == "":
            i += 1
        if i >= len(norm):
            return False
        if norm[i].strip() != "STYLE":
            return False
        # A STYLE block should have at least the header and can have zero or more CSS lines
        return True

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        raw_lines = [("" if s is None else str(s)) for s in lines]
        if not cls.is_valid(raw_lines):
            raise ValueError("Invalid WebVTT STYLE block lines")
        formatted = cls.format_lines(raw_lines)
        text = "\n".join(formatted)
        return cls(text)

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        # Normalize to strings without CR/LF
        norm = [("" if s is None else str(s)).rstrip("\r\n") for s in lines]

        # Remove leading empty lines
        while norm and norm[0].strip() == "":
            norm.pop(0)

        if not norm:
            return ["STYLE", ""]

        # Ensure first non-empty is exactly "STYLE"
        if norm[0].strip() != "STYLE":
            # If the first line contains extra spaces around, normalize to exact "STYLE"
            norm[0] = "STYLE"
        else:
            norm[0] = "STYLE"

        # Strip trailing whitespace on all subsequent lines (keep internal spaces)
        for i in range(1, len(norm)):
            norm[i] = norm[i].rstrip()

        # Remove trailing empty lines, then ensure a single empty line terminator
        while len(norm) > 1 and norm[-1].strip() == "":
            norm.pop()
        norm.append("")

        return norm
