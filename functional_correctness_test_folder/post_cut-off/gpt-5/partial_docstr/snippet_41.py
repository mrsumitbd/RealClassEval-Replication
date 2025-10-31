from __future__ import annotations

from datetime import datetime, timezone as dt_timezone, timedelta
from typing import List

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


class HeaderManager:
    '''Manager for header layout and formatting.'''

    def __init__(self) -> None:
        self.title = "✨ Service Dashboard ✨"
        self.min_width = 48
        self.padding = 2

    def _safe_timezone(self, tz_name: str):
        if ZoneInfo is None:
            return dt_timezone.utc, "UTC"
        try:
            return ZoneInfo(tz_name), tz_name
        except Exception:
            return dt_timezone.utc, "UTC"

    def _offset_str(self, dt: datetime) -> str:
        offset = dt.utcoffset() or timedelta(0)
        total_minutes = int(offset.total_seconds() // 60)
        sign = "+" if total_minutes >= 0 else "-"
        total_minutes = abs(total_minutes)
        hours, minutes = divmod(total_minutes, 60)
        return f"UTC{sign}{hours:02d}:{minutes:02d}"

    def _center(self, text: str, width: int) -> str:
        if len(text) >= width:
            return text
        pad_total = width - len(text)
        left = pad_total // 2
        right = pad_total - left
        return (" " * left) + text + (" " * right)

    def create_header(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> list[str]:
        '''Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        '''
        plan_str = (plan or "").strip() or "free"
        tz_obj, tz_label = self._safe_timezone(timezone)
        now = datetime.now(tz_obj)
        offset = self._offset_str(now)
        time_str = now.strftime("%Y-%m-%d %H:%M")
        info_line_1 = f"Plan: {plan_str.upper()}"
        info_line_2 = f"Timezone: {tz_label} • {offset} • {time_str}"

        content_width = max(len(self.title), len(
            info_line_1), len(info_line_2))
        inner_width = max(self.min_width, content_width + self.padding * 2)

        top = "╭" + ("─" * inner_width) + "╮"
        bottom = "╰" + ("─" * inner_width) + "╯"
        sep = "├" + ("─" * inner_width) + "┤"

        lines: List[str] = [
            top,
            "│" + self._center(self.title, inner_width) + "│",
            sep,
            "│" + self._center(info_line_1, inner_width) + "│",
            "│" + self._center(info_line_2, inner_width) + "│",
            bottom,
        ]
        return lines
