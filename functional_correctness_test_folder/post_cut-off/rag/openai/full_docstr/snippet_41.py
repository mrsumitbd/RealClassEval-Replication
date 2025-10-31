
import datetime
from typing import List
try:
    import pytz
except ImportError:  # pragma: no cover
    pytz = None


class HeaderManager:
    """Manager for header layout and formatting."""

    def __init__(self) -> None:
        """Initialize header manager."""
        self._sparkle = "✨"

    def _get_current_time(self, timezone: str) -> str:
        """Return the current time formatted for the given timezone."""
        now = datetime.datetime.utcnow()
        if pytz:
            try:
                tz = pytz.timezone(timezone)
                now = now.replace(tzinfo=pytz.utc).astimezone(tz)
            except Exception:  # pragma: no cover
                # Fallback to UTC if timezone is invalid
                now = now.replace(tzinfo=pytz.utc)
        return now.strftime("%Y-%m-%d %H:%M:%S %Z")

    def create_header(self, plan: str = "pro", timezone: str = "Europe/Warsaw") -> List[str]:
        """Create stylized header with sparkles.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of formatted header lines
        """
        current_time = self._get_current_time(timezone)
        border = f"{self._sparkle * 30}"
        header_lines = [
            border,
            f"{self._sparkle}  Plan: {plan}  {self._sparkle}",
            f"{self._sparkle}  Timezone: {timezone}  {self._sparkle}",
            f"{self._sparkle}  Current Time: {current_time}  {self._sparkle}",
            border,
        ]
        return header_lines
