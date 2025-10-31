from typing import List


class ErrorDisplayComponent:
    """Error display component for handling error states."""

    def __init__(self) -> None:
        """Initialize error display component."""
        self._plan_advice = {
            "free": "You are on the Free plan; rate limits may apply. Consider upgrading to Pro.",
            "pro": "You are on the Pro plan; if the issue persists, contact support.",
            "business": "You are on the Business plan; if the issue persists, contact support.",
            "enterprise": "You are on the Enterprise plan; contact your account team or support.",
        }
        self._generic_advice = "If the problem continues, contact support."

    def format_error_screen(self, plan: str = "pro", timezone: str = "Europe/Warsaw") -> List[str]:
        """Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        """
        normalized_plan = (plan or "").strip().lower()
        plan_label = normalized_plan.upper() if normalized_plan else "UNKNOWN"
        plan_advice = self._plan_advice.get(
            normalized_plan, self._generic_advice)

        lines = [
            "ERROR",
            "Failed to fetch data.",
            "",
            f"Plan: {plan_label}",
            f"Timezone: {timezone}",
            "",
            "Troubleshooting:",
            "- Check your internet connection.",
            "- Verify API credentials and permissions.",
            "- Ensure the data source is reachable.",
            "- Retry in a few minutes.",
            "",
            plan_advice,
            "Support: support@example.com",
        ]
        return lines
