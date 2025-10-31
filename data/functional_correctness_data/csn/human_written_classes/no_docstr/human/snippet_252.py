import io

class _WarningStream(io.StringIO):

    def write(self, text: str) -> int:
        matched = _REPORT_RE.search(text)
        if matched:
            line = matched.group('line')
            level_text = matched.group('level').capitalize()
            message = matched.group('message').rstrip('\r\n')
            text = f'line {line}: {level_text}: {message}\n'
        return super().write(text)

    def __str__(self) -> str:
        return self.getvalue().strip()