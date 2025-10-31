from typing import List, Dict
from datetime import datetime, timezone as dt_timezone

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover
    ZoneInfo = None  # type: ignore


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self._title = "Data Fetch Error"
        self._component = "ErrorDisplayComponent"
        self._support_by_plan: Dict[str, str] = {
            "free": "https://support.example.com/community",
            "pro": "support-pro@example.com",
            "business": "support-business@example.com",
            "enterprise": "support-enterprise@example.com",
        }

    def _format_timestamp(self, tz_name: str) -> str:
        if ZoneInfo:
            try:
                tz = ZoneInfo(tz_name)
                now = datetime.now(tz)
                return now.strftime("%Y-%m-%d %H:%M:%S %Z")
            except Exception:
                pass
        now = datetime.now(dt_timezone.utc)
        return now.strftime("%Y-%m-%d %H:%M:%S UTC")

    def _support_contact(self, plan: str) -> str:
        key = (plan or "").strip().lower()
        return self._support_by_plan.get(key, "https://support.example.com")

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        ts = self._format_timestamp(timezone)
        plan_disp = (plan or "unknown").strip()
        contact = self._support_contact(plan_disp)

        lines: List[str] = []
        lines.append("=== " + self._title + " ===")
        lines.append(f"Component: {self._component}")
        lines.append(f"Plan: {plan_disp}")
        lines.append(f"Timezone: {timezone}")
        lines.append(f"Timestamp: {ts}")
        lines.append("")
        lines.append("We couldn't retrieve the requested data.")
        lines.append("")
        lines.append("What you can try:")
        lines.append("- Check your internet connection.")
        lines.append("- Verify API credentials and permissions.")
        lines.append("- Retry the operation in a few moments.")
        lines.append("- If the issue persists, contact support.")
        lines.append("")
        lines.append("Support:")
        lines.append(f"- {contact}")
        return lines
