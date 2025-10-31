class HeaderManager:
    """Manager for header layout and formatting."""

    def __init__(self) -> None:
        """Initialize header manager."""
        self.default_width = 64
        self.box = {
            'tl': '┏',
            'tr': '┓',
            'bl': '┗',
            'br': '┛',
            'v': '┃',
            'h': '━',
        }
        self.sparkle_pattern = ' ✦  ✧  ✨  ✧ '
        self.datetime_format = '%Y-%m-%d %H:%M %Z'

    def _safe_timezone(self, timezone: str):
        try:
            from zoneinfo import ZoneInfo
            return ZoneInfo(timezone)
        except Exception:
            from datetime import timezone as dt_tz
            return dt_tz.utc

    def _compute_width(self, lines: list[str]) -> int:
        content_width = max(len(line) for line in lines) if lines else 0
        return max(self.default_width, content_width + 8)

    def _belt(self, interior: int) -> str:
        s = (self.sparkle_pattern *
             ((interior // len(self.sparkle_pattern)) + 2))[:interior]
        return s

    def _box_line(self, content: str, total_width: int) -> str:
        interior = total_width - 2
        return f"{self.box['v']}{content.center(interior)}{self.box['v']}"

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        """Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        """
        from datetime import datetime

        plan_str = (str(plan).strip() or 'pro').upper()
        tzinfo = self._safe_timezone(timezone)
        now = datetime.now(tzinfo)
        time_str = now.strftime(self.datetime_format)

        title = f"[ {plan_str} PLAN ]"
        time_line = f"{timezone} • {time_str}"

        width = self._compute_width([title, time_line])
        interior = width - 2

        top = f"{self.box['tl']}{self.box['h'] * interior}{self.box['tr']}"
        belt = f"{self.box['v']}{self._belt(interior)}{self.box['v']}"
        title_line = self._box_line(title, width)
        time_info_line = self._box_line(time_line, width)
        bottom = f"{self.box['bl']}{self.box['h'] * interior}{self.box['br']}"

        return [top, belt, title_line, time_info_line, belt, bottom]
