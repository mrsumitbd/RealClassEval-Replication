class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        '''Initialize header manager.'''
        self.min_width = 48
        self.border_char = '═'
        self.side_char = '║'
        self.corner_top_left = '╔'
        self.corner_top_right = '╗'
        self.corner_bottom_left = '╚'
        self.corner_bottom_right = '╝'
        self.sparkle = '✨'
        self.separator_char = '─'

    def _center(self, text: str, width: int) -> str:
        if len(text) >= width:
            return text[:width]
        pad_total = width - len(text)
        left = pad_total // 2
        right = pad_total - left
        return (' ' * left) + text + (' ' * right)

    def _build_box(self, lines: list[str]) -> list[str]:
        inner_width = max(self.min_width, max((len(line)
                          for line in lines), default=0))
        top = f"{self.corner_top_left}{self.border_char * (inner_width + 2)}{self.corner_top_right}"
        bottom = f"{self.corner_bottom_left}{self.border_char * (inner_width + 2)}{self.corner_bottom_right}"
        boxed = [top]
        for line in lines:
            centered = self._center(line, inner_width)
            boxed.append(f"{self.side_char} {centered} {self.side_char}")
        boxed.append(bottom)
        return boxed

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        from datetime import datetime
        try:
            from zoneinfo import ZoneInfo  # type: ignore
        except Exception:
            ZoneInfo = None  # type: ignore

        tz_label = timezone
        dt_fmt = "%Y-%m-%d %H:%M:%S"
        now_str = ""
        try:
            if ZoneInfo is not None:
                tz = ZoneInfo(timezone)  # type: ignore
                now = datetime.now(tz)
                now_str = now.strftime(dt_fmt)
            else:
                now = datetime.utcnow()
                now_str = now.strftime(dt_fmt) + " UTC"
                tz_label = "UTC"
        except Exception:
            now = datetime.utcnow()
            now_str = now.strftime(dt_fmt) + " UTC"
            tz_label = "UTC"

        plan_display = str(plan).strip() or "unknown"
        plan_display = plan_display.upper()

        title = f"{self.sparkle} Plan: {plan_display} {self.sparkle}"
        time_line = f"Local time: {now_str} ({tz_label})"

        # Decorative separator with sparkles
        sep_len = max(self.min_width - 8, 12)
        left = self.separator_char * (sep_len // 2)
        right = self.separator_char * (sep_len - len(left))
        separator = f"{left} {self.sparkle} {right}"

        lines = [
            title,
            separator,
            time_line,
        ]

        return self._build_box(lines)
