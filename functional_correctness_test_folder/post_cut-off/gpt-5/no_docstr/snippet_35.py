from typing import List
from datetime import datetime, timezone as _timezone

try:
    from zoneinfo import ZoneInfo  # Python 3.9+
except Exception:
    ZoneInfo = None  # Fallback if not available


class ErrorDisplayComponent:
    def __init__(self) -> None:
        self._title = "=== Application Error ==="
        self._generic_message = "An unexpected error occurred. Please try again."
        self._support_by_plan = {
            "free": "Need help? Upgrade to Pro for priority support: https://example.com/upgrade",
            "pro": "Priority support: support@example.com",
            "enterprise": "Your dedicated support team has been notified.",
        }
        self._valid_plans = set(self._support_by_plan.keys())

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        normalized_plan = (plan or "").strip().lower()
        if normalized_plan not in self._valid_plans:
            normalized_plan = "free"

        tz_label = timezone
        dt: datetime
        if ZoneInfo is not None:
            try:
                tzinfo = ZoneInfo(timezone)
                dt = datetime.now(tzinfo)
            except Exception:
                tz_label = "UTC"
                dt = datetime.now(_timezone.utc)
        else:
            tz_label = "UTC"
            dt = datetime.now(_timezone.utc)

        timestamp = dt.isoformat(timespec="seconds")

        lines: List[str] = [
            self._title,
            f"Plan: {normalized_plan.capitalize()}",
            f"Timestamp ({tz_label}): {timestamp}",
            self._generic_message,
            self._support_by_plan[normalized_plan],
            "If the issue persists, please try again later.",
        ]
        return lines
