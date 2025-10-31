import typing


class WebVTTStyleBlock:

    def __init__(self, text: str):
        self.text = text

    @classmethod
    def is_valid(cls, lines: typing.Sequence[str]) -> bool:
        if not lines:
            return False
        # Find first non-empty line
        idx = 0
        n = len(lines)
        while idx < n and not lines[idx].strip():
            idx += 1
        if idx >= n:
            return False
        if lines[idx].strip() != "STYLE":
            return False
        # Ensure at least one non-empty content line after STYLE before the next blank separator
        idx += 1
        has_content = False
        while idx < n:
            s = lines[idx].rstrip("\r\n")
            if not s.strip():
                break
            has_content = True if s else has_content
            idx += 1
        return has_content

    @classmethod
    def from_lines(cls, lines: typing.Iterable[str]) -> 'WebVTTStyleBlock':
        buf = list(lines)
        if not cls.is_valid(buf):
            raise ValueError("Invalid WebVTT STYLE block")
        # Find header
        i = 0
        n = len(buf)
        while i < n and not buf[i].strip():
            i += 1
        # i now at STYLE
        i += 1
        # Collect until first blank line or end
        content: typing.List[str] = []
        while i < n:
            line = buf[i].rstrip("\r\n")
            if not line.strip():
                break
            content.append(line)
            i += 1
        formatted = cls.format_lines(content)
        return cls("\n".join(formatted))

    @staticmethod
    def format_lines(lines: typing.List[str]) -> typing.List[str]:
        # Normalize endings and trim leading/trailing empty lines
        normalized = [ln.rstrip("\r\n").rstrip() for ln in lines]
        # Remove leading empty lines
        start = 0
        while start < len(normalized) and not normalized[start].strip():
            start += 1
        # Remove trailing empty lines
        end = len(normalized) - 1
        while end >= start and not normalized[end].strip():
            end -= 1
        return normalized[start:end + 1] if start <= end else []
