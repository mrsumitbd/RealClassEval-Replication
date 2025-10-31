import datetime as _dt
from typing import List

try:
    from zoneinfo import ZoneInfo as _ZoneInfo  # Python 3.9+
except Exception:  # pragma: no cover
    _ZoneInfo = None


class HeaderManager:
    """Manager for header layout and formatting."""

    def __init__(self) -> None:
        """Initialize header manager."""
        self._min_inner_width = 38
        self._sparkles = ["✦", "✧", "✨", "❇", "⋆", "⚡", "✶", "✺"]
        self._box = {
            "tl": "┏",
            "tr": "┓",
            "bl": "┗",
            "br": "┛",
            "h": "━",
            "v": "┃",
            "mid_l": "┣",
            "mid_r": "┫",
        }

    def create_header(self, plan: str = "pro", timezone: str = "Europe/Warsaw") -> List[str]:
        """Create stylized header with sparkles.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted header lines
        """
        plan = (plan or "").strip().lower()
        pretty_plan = self._pretty_plan(plan)

        tz_label, tz_name, now_str = self._format_time(timezone)

        # Core content lines
        title_spark_l, title_spark_r = self._pick_sparkles(pretty_plan)
        title = f"{title_spark_l} {pretty_plan} {title_spark_r}"
        line_plan = f"Plan: {pretty_plan}"
        line_tz = f"Timezone: {tz_label}{f' ({tz_name})' if tz_name else ''}"
        line_now = f"Local time: {now_str}{f' {tz_name}' if tz_name else ''}"

        inner_width = max(
            self._min_inner_width,
            len(title),
            len(line_plan),
            len(line_tz),
            len(line_now),
        )

        top = self._box["tl"] + \
            (self._box["h"] * (inner_width + 2)) + self._box["tr"]
        sep = self._box["mid_l"] + \
            (self._box["h"] * (inner_width + 2)) + self._box["mid_r"]
        bot = self._box["bl"] + \
            (self._box["h"] * (inner_width + 2)) + self._box["br"]

        # Sparkle bar (deterministic pattern)
        sparkle_bar = self._sparkle_bar(inner_width + 2)

        lines = [
            sparkle_bar,
            top,
            self._frame_line(title, inner_width),
            sep,
            self._frame_line(line_plan, inner_width),
            self._frame_line(line_tz, inner_width),
            self._frame_line(line_now, inner_width),
            bot,
            sparkle_bar,
        ]
        return lines

    def _frame_line(self, text: str, width: int) -> str:
        pad_left, pad_right = self._center_padding(text, width)
        return f'{self._box["v"]} {" " * pad_left}{text}{" " * pad_right} {self._box["v"]}'

    @staticmethod
    def _center_padding(text: str, width: int) -> (int, int):
        diff = max(0, width - len(text))
        left = diff // 2
        right = diff - left
        return left, right

    def _sparkle_bar(self, width: int) -> str:
        # Repeat sparkles with spaces for a soft separator
        pattern = " ".join(self._sparkles)
        # Ensure at least exact width
        out = (pattern * ((width // len(pattern)) + 2))[:width]
        return out

    def _pick_sparkles(self, seed_text: str) -> (str, str):
        if not seed_text:
            return self._sparkles[2], self._sparkles[0]
        s = sum(ord(c) for c in seed_text)
        a = self._sparkles[s % len(self._sparkles)]
        b = self._sparkles[(s + 3) % len(self._sparkles)]
        return a, b

    @staticmethod
    def _pretty_plan(plan: str) -> str:
        mapping = {
            "free": "Free",
            "basic": "Basic",
            "starter": "Starter",
            "pro": "Pro",
            "team": "Team",
            "business": "Business",
            "enterprise": "Enterprise",
            "plus": "Plus",
        }
        pretty = mapping.get(plan, (plan or "Unknown").title())
        icon_map = {
            "Free": "🪙",
            "Basic": "🎯",
            "Starter": "🌱",
            "Pro": "⭐",
            "Team": "👥",
            "Business": "🏢",
            "Enterprise": "🚀",
            "Plus": "➕",
            "Unknown": "❓",
        }
        return f'{icon_map.get(pretty, "✨")} {pretty}'

    @staticmethod
    def _format_time(timezone: str) -> (str, str, str):
        tz_used = timezone or "UTC"
        tz_name = ""
        if _ZoneInfo is not None:
            try:
                tzinfo = _ZoneInfo(tz_used)
            except Exception:
                tzinfo = _dt.timezone.utc
                tz_used = "UTC"
        else:  # Fallback
            tzinfo = _dt.timezone.utc
            tz_used = "UTC"
        now = _dt.datetime.now(tz=tzinfo)
        tz_name = now.tzname() or ""
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")
        return tz_used, tz_name, now_str
