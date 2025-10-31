
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
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        error_screen_lines = [
            f'Error fetching data for {plan} plan at {current_time}.',
            'Please check your connection and try again.',
            'If the issue persists, contact support.'
        ]
        return error_screen_lines
