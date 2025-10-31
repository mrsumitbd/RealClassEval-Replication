
from datetime import datetime
import pytz
from typing import List


class ErrorDisplayComponent:
    """Error display component for handling error states."""

    def __init__(self) -> None:
        """Initialize error display component."""
        pass

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        """Format error screen for failed data fetch.

        Args:
            plan: Current plan name
            timezone: Display timezone

        Returns:
            List of formatted error screen lines
        """
        now = datetime.now(pytz.timezone(timezone))
        error_lines = [
            f'Error fetching data for {plan} plan',
            'Please check your connection and try again.',
            f'Current Time: {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}',
            'If the issue persists, contact support.'
        ]
        return error_lines
