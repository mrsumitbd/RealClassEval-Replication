import typing


class WebVTTCommentBlock:
    def __init__(self, text: str):
        self.text = text if text is not None else ""

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        first = lines[0].rstrip("\r\n")
        return first.startswith("NOTE")

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTCommentBlock':
        raw_lines = [str(l).rstrip("\r\n") for l in lines]
        if not cls.is_valid(raw_lines):
            raise ValueError("Invalid WebVTT comment block")

        first = raw_lines[0]
        # Extract inline text after NOTE
        inline = first[4:]
        if inline.startswith(" "):
            inline = inline[1:]
        # Collect subsequent lines until first empty line (blank line ends NOTE block)
        rest: typing.List[str] = []
        for line in raw_lines[1:]:
            if line == "":
                break
            rest.append(line)
        parts: typing.List[str] = []
        if inline != "":
            parts.append(inline)
        parts.extend(rest)
        text = "\n".join(parts)
        return cls(text)

    @staticmethod
    def format_lines(lines: str) -> typing.List[str]:
        text = "" if lines is None else str(lines)
        # Normalize newlines
        parts = text.splitlines()
        out: typing.List[str] = []
        if not parts:
            out.append("NOTE")
            out.append("")
            return out
        if len(parts) == 1:
            if parts[0] == "":
                out.append("NOTE")
            else:
                out.append("NOTE " + parts[0])
            out.append("")
            return out
        # Multi-line: "NOTE" on its own line, then the text lines
        out.append("NOTE")
        out.extend(parts)
        out.append("")
        return out
