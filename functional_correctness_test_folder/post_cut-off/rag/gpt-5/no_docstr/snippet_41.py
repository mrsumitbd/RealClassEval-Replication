from __future__ import annotations

from datetime import datetime, timezone as dt_timezone

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    try:
        from backports.zoneinfo import ZoneInfo  # type: ignore
    except Exception:  # pragma: no cover
        ZoneInfo = None  # type: ignore


class HeaderManager:
    """Manager for header layout and formatting."""

    def __init__(self) -> None:
        """Initialize header manager."""
        self.width = 72
        self.border_char = "-"
        self.side_border = "|"
        self.corner_left = "+"
        self.corner_right = "+"
        self.sparkle = "✨"
        self.plan_badge = {
            "free": "☆",
            "basic": "◇",
            "team": "◆",
            "pro": "★",
            "business": "✦",
            "enterprise": "✪",
        }

    def _zoneinfo(self, tz_name: str):
        if ZoneInfo is None:
            return dt_timezone.utc, "UTC"
        try:
            tz = ZoneInfo(tz_name)
            return tz, tz_name
        except Exception:
            return dt_timezone.utc, "UTC"

    def _frame(self, text: str) -> str:
        inner_width = self.width - 4
        if inner_width < 0:
            inner_width = 0
        clipped = text[:inner_width] if len(text) > inner_width else text
        return f"{self.side_border} {clipped.center(inner_width)} {self.side_border}"

    def _hline(self, char: str | None = None, with_corners: bool = True) -> str:
        ch = char or self.border_char
        if with_corners:
            return f"{self.corner_left}{ch * (self.width - 2)}{self.corner_right}"
        return f"{self.side_border}{ch * (self.width - 2)}{self.side_border}"

    def create_header(self, plan: str = "pro", timezone: str = "Europe/Warsaw") -> list[str]:
        """Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        """
        tz, tz_label = self._zoneinfo(timezone)
        now = datetime.now(tz)
        ts = now.strftime("%Y-%m-%d %H:%M")
        tz_abbr = now.tzname() or tz_label

        plan_key = (plan or "free").strip().lower()
        badge = self.plan_badge.get(plan_key, "•")
        plan_disp = plan_key.upper()

        lines: list[str] = []
        lines.append(self._hline("="))
        title = f"{self.sparkle} Plan: {plan_disp} {badge} {self.sparkle}"
        lines.append(self._frame(title))
        lines.append(self._hline("-"))
        lines.append(self._frame(f"Local time: {ts} {tz_abbr}"))
        lines.append(self._frame(f"Timezone: {tz_label}"))
        lines.append(self._hline("="))
        return lines
