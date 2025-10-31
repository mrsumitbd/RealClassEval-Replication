from typing import List
from datetime import datetime


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.error_title = "Data Fetch Error"
        self.error_message = "An error occurred while fetching the data. Please try again later."
        self.support_message = "If the problem persists, contact support."
        self.support_email = "support@example.com"

    def format_error_screen(self, plan: str = 'pro', timezone: str = 'Europe/Warsaw') -> List[str]:
        '''Format error screen for failed data fetch.
        Args:
            plan: Current plan name
            timezone: Display timezone
        Returns:
            List of formatted error screen lines
        '''
        try:
            import pytz
            now = datetime.now(pytz.timezone(timezone))
        except Exception:
            now = datetime.utcnow()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        lines = [
            f"=== {self.error_title} ===",
            "",
            self.error_message,
            "",
            f"Plan: {plan}",
            f"Time: {timestamp}",
            "",
            self.support_message,
            f"Email: {self.support_email}"
        ]
        return lines
