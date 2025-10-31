
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        # Store a default error message that can be overridden if needed
        self.default_error_msg = "Failed to fetch data."

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of formatted error screen lines
        '''
        # Get current time in the requested timezone
        try:
            tz = ZoneInfo(timezone)
            current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            # Fallback if the timezone is invalid
            current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        lines: List[str] = []

        # Header
        lines.append("=== ERROR ===")
        lines.append(f"Plan: {plan}")
        lines.append(f"Timezone: {timezone}")
        lines.append(f"Time: {current_time}")
        lines.append("")

        # Main error message
        lines.append(self.default_error_msg)
        lines.append("")

        # Suggested actions
        lines.append("Please check your network connection and try again.")
        lines.append(
            "If the issue persists, contact support at support@example.com.")
        lines.append("")

        # Footer
        lines.append("Thank you for using our service.")

        return lines
