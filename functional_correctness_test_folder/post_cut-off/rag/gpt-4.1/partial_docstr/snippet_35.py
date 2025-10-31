from typing import List
from datetime import datetime


class ErrorDisplayComponent:
    '''Error display component for handling error states.'''

    def __init__(self) -> None:
        '''Initialize error display component.'''
        self.last_error_time = None

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
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            time_str = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        except Exception:
            now = datetime.utcnow()
            time_str = now.strftime('%Y-%m-%d %H:%M:%S UTC')
        self.last_error_time = time_str
        lines = [
            "=== ERROR ===",
            f"Plan: {plan}",
            f"Time: {time_str}",
            "Failed to fetch data.",
            "Please check your connection or try again later.",
            "If the problem persists, contact support."
        ]
        return lines
