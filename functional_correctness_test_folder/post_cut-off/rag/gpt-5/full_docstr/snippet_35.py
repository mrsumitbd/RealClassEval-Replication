from typing import List
from datetime import datetime
from uuid import uuid4

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - fallback for very old Python
    ZoneInfo = None  # type: ignore


class ErrorDisplayComponent:
    """Error display component for handling error states."""

    def __init__(self) -> None:
        """Initialize error display component."""
        self.support_email = "support@example.com"
        self.docs_url = "https://docs.example.com/troubleshooting/data-fetch"
        self.status_url = "https://status.example.com"
        self.contact_url = "https://support.example.com"
        self.free_plans = {"free", "basic", "trial", "community"}
        self.paid_plans = {"pro", "team", "business", "enterprise", "plus"}

    def format_error_screen(self, plan: str = "pro", timezone: str = "Europe/Warsaw") -> List[str]:
        """Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        """
        plan_norm = (plan or "").strip().lower()
        plan_disp = plan_norm.upper() if plan_norm else "UNKNOWN"

        tz_note = None
        now_str = ""
        if ZoneInfo is not None:
            try:
                tz = ZoneInfo(timezone)
            except Exception:
                tz = ZoneInfo("UTC")
                tz_note = f"Note: Unknown timezone '{timezone}', falling back to UTC."
        else:
            tz = None
            tz_note = f"Note: zoneinfo not available; showing times in UTC."
        now = datetime.utcnow() if tz is None else datetime.now(tz)
        if tz is None:
            now_str = now.strftime("%Y-%m-%d %H:%M:%S UTC")
        else:
            tz_abbr = now.tzname() or timezone
            now_str = f"{now.strftime('%Y-%m-%d %H:%M:%S')} {tz_abbr}"

        corr_id = uuid4().hex[:12].upper()

        title = "✖ Data fetch failed"
        sep = "-" * len(title)

        lines: List[str] = []
        lines.append(title)
        lines.append(sep)
        lines.append(f"Plan: {plan_disp}")
        lines.append(f"Local time ({timezone}): {now_str}")
        if tz_note:
            lines.append(tz_note)
        lines.append("")
        lines.append("What happened:")
        lines.append(
            "  We couldn't retrieve the requested data from the server.")
        lines.append("")
        lines.append("Common causes:")
        lines.append("  • Temporary network issue or DNS failure")
        lines.append("  • Expired or invalid credentials")
        lines.append("  • API rate limit reached")
        lines.append("  • Service outage or scheduled maintenance")
        if plan_norm in self.free_plans:
            lines.append("  • Free-tier concurrency/throughput limits")
        lines.append("")
        lines.append("Try this:")
        lines.append("  1) Retry the request in a few seconds")
        lines.append(f"  2) Check service status: {self.status_url}")
        lines.append(
            "  3) Verify your API key, permissions, and organization access")
        lines.append(
            "  4) Ensure proxy/firewall allows outbound requests to the API")
        if plan_norm in self.free_plans:
            lines.append(
                "  5) Consider upgrading for higher limits and priority support")
        lines.append("")
        lines.append("Diagnostics:")
        lines.append(f"  Correlation-ID: {corr_id}")
        lines.append(f"  Timezone: {timezone}")
        lines.append(f"  Plan tier: {plan_disp}")
        lines.append("")
        if plan_norm in self.paid_plans:
            lines.append(
                f"Need help? Contact support: {self.support_email} or {self.contact_url}")
        else:
            lines.append(f"Need help? See docs: {self.docs_url}")
            lines.append(f"Upgrade options: {self.contact_url}")
        return lines
